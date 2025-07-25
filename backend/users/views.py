from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

from .serializers import (
    PhoneNumberSerializer,
    PhoneTokenSerializer,
    UserProfileSerializer,
    ActivateInviteSerializer,
)
from .models import PhoneToken
from .tasks import send_sms_verification_code

User = get_user_model()


class SendVerificationCodeView(generics.CreateAPIView):
    serializer_class = PhoneNumberSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data["phone"]

        send_sms_verification_code.delay(phone)

        return Response(
            {"detail": "Verification code request accepted"},
            status=status.HTTP_202_ACCEPTED,
        )


class VerifyCodeView(generics.CreateAPIView):
    serializer_class = PhoneTokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data["phone"]
        entered_code = serializer.validated_data["token"]

        phone_token, _ = PhoneToken.objects.update_or_create(
            phone=phone,
            defaults={
                "token": entered_code,
                "is_verified": True,
            },
        )

        user, created = User.objects.get_or_create(phone=phone)

        if created and not user.invite_code:
            user.invite_code = self._generate_invite_code()
            user.save()

        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "phone": str(user.phone),
                "is_new_user": created,
                "invite_code": user.invite_code,
            }
        )

    def _generate_invite_code(self):
        import random
        import string

        return "".join(random.choices(string.ascii_uppercase + string.digits, k=6))


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        if "activated_invite" in request.data:
            if request.user.activated_invite:
                return Response(
                    {"error": "You already activated an invite code"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = ActivateInviteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            invite_code = serializer.validated_data["invite_code"]
            if invite_code == request.user.invite_code:
                return Response(
                    {"error": "You cannot use your own invite code"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            request.user.activated_invite = invite_code
            request.user.save()
            return Response(
                {"success": "Invite code activated"}, status=status.HTTP_200_OK
            )

        return Response(
            {"error": "Only invite code activation is allowed"},
            status=status.HTTP_400_BAD_REQUEST,
        )
