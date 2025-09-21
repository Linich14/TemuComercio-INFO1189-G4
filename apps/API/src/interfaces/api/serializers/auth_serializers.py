from rest_framework import serializers
from datetime import datetime

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate_email(self, value):
        return value.lower().strip()

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    rut = serializers.CharField(max_length=12, required=False, allow_blank=True)
    birth_date = serializers.DateTimeField(required=False, allow_null=True)
    
    def validate_email(self, value):
        return value.lower().strip()
    
    def validate_first_name(self, value):
        return value.strip()
    
    def validate_last_name(self, value):
        return value.strip()
    
    def validate_rut(self, value):
        if value:
            # Limpiar RUT
            return value.replace('.', '').replace('-', '').upper()
        return value