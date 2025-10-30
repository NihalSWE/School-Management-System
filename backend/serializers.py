# In backend/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Users as Profile  # <-- We rename 'Users' to 'Profile' here for clarity
from django.contrib.auth.hashers import make_password

# SERIALIZER 1: For Django's built-in 'auth.User'
class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Use create_user to handle hashing
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

# SERIALIZER 2: For your legacy 'Users' table (now called Profile)
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile # <-- Points to your 'Users' model
        # List all fields from your 'Users' model
        fields = [
            'id', 'usertype', 'name', 'email', 'mobile', 'address',
            'gender', 'fname', 'mname', 'religion', 'id_no', 'dob',
            'role', 'join_date', 'designation_id', 'salary', 'status',
            'password' 
        ]
        extra_kwargs = {
            'password': {'write_only': True} # Good to keep this
        }
    
    # We still keep your original password hashing logic for this model
    def create(self, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)