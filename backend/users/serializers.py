from rest_framework import serializers
from phonenumbers import parse, format_number, PhoneNumberFormat
from phonenumbers.phonenumberutil import NumberParseException, is_valid_number
from django.utils import timezone

from .models import User, PhoneToken


class PhoneNumberSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def validate_phone(self, value):
        try:
            phone = parse(value, None)

            if not is_valid_number(phone):
                raise serializers.ValidationError("Invalid phone number")

            return format_number(phone, PhoneNumberFormat.E164)

        except NumberParseException:
            raise serializers.ValidationError("Invalid phone number format")


class PhoneTokenSerializer(serializers.Serializer):
    phone = serializers.CharField()
    token = serializers.CharField(max_length=4)

    def validate(self, data):
        phone_token, created = PhoneToken.objects.update_or_create(
            phone=data["phone"],
            defaults={
                "token": data["token"],
                "is_verified": True,
                "created_at": timezone.now(),
            },
        )

        return data


class UserProfileSerializer(serializers.ModelSerializer):
    referred_users = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["phone", "invite_code", "activated_invite", "referred_users"]
        read_only_fields = ["phone", "invite_code"]

    def get_referred_users(self, obj):
        return list(obj.get_referred_users().values_list("phone", flat=True))


class ActivateInviteSerializer(serializers.Serializer):
    invite_code = serializers.CharField(max_length=6)

    def validate_invite_code(self, value):
        if not User.objects.filter(invite_code=value).exists():
            raise serializers.ValidationError("Invalid invite code")

        if self.context["request"].user.invite_code == value:
            raise serializers.ValidationError("You cannot use your own invite code")

        return value
