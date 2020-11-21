from django.contrib.auth import get_user_model
User = get_user_model()

from rest_framework import serializers

from apps.accounts.utils import check_passwords
from apps.accounts.utils import STATUS_ERROR

class AccountRUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'uuid',
            'email',
            'phone_number',
            'first_name',
            'last_name',
        )
        extra_kwargs = {
            'uuid': {
                'read_only': True,
            },
        }


    def update(self, instance, validated_data):
        ''' UPDATE USER '''

        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)

        instance.save()

        return instance

    def validate(self, attrs):
        user = self.context['request'].user
        instance_uuid = self.instance.uuid

        if not  (instance_uuid == user.uuid or user.is_staff):
            raise serializers.ValidationError('It\s not your account or you are not \'Admin\'.')

        return attrs

class AccountCreateSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        write_only=True,
    )
    password2 = serializers.CharField(
        write_only=True,
    )

    class Meta:
        model = User
        fields = (
            'uuid',
            'email',
            'phone_number',
            'first_name',
            'last_name',
            'password1',
            'password2'
        )
        extra_kwargs = {
            'uuid': {
                'read_only': True,
            },
        }

    def create(self, validated_data):
        ''' CREATE USER '''

        email = validated_data.get('email', None)
        first_name = validated_data.get('first_name', None)
        last_name = validated_data.get('last_name', None)
        phone_number = validated_data.get('phone_number', None)
        password1 = validated_data.get('password1', None)
        password2 = validated_data.get('password2', None)

        check_data = check_passwords(password1, password2) # Check if 2 passwords are valid
        if check_data['status'] == STATUS_ERROR:
            raise serializers.ValidationError(check_data['errors'])

        password = check_data['password']
        
        user = User.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            password=password,
        )

        return user
        


class ChangePasswordSerializer(serializers.ModelSerializer): 
    password = serializers.CharField(write_only=True, required=True) 
    password2 = serializers.CharField(write_only=True, required=True) 
    old_password = serializers.CharField(write_only=True, required=True) 
    class Meta: 
        model = User 
        fields = ('old_password', 'password', 'password2') 
    
    def validate(self, attrs): 
        if attrs['password'] != attrs['password2']: 
            raise serializers.ValidationError({"password": "Password fields didn't match."}) 
        return attrs 
    
    def validate_old_password(self, value): 
        user = self.context['request'].user 
        if not user.check_password(value):
             raise serializers.ValidationError({"old_password": "Old password is not correct"}) 
        
        return value 
    
    def update(self, instance, validated_data): 
        instance.set_password(validated_data['password']) 
        instance.save() 
        return instance