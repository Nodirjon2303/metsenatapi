from rest_framework import serializers


def validate_phone_number(phone_number):
    if (phone_number[0] == '+' and phone_number[:4] == '+998' and len(phone_number) == 13) or (
            phone_number[:3] == '998' and len(phone_number) == 12) or len(phone_number) == 9:
        return phone_number
    else:
        raise serializers.ValidationError({"phone": "Please check phone number"})
