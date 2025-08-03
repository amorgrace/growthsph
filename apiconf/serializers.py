from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import WalletAddres, Finance, RecentTransaction, KYC, BankAccount
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer



User = get_user_model()

class CustomUserCreateSerializer(DjoserUserCreateSerializer):
    re_password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )
    id = serializers.CharField(source='public_id', read_only=True)

    class Meta(DjoserUserCreateSerializer.Meta):
        model = User
        fields = (
            "id",
            "email",
            "password",
            "re_password",
            "first_name",
            "last_name",
            "phone_number",
            "investment_goal",
            "risk_tolerance",
            "account_type",
            "choose_trades",
            "country",
        )
        extra_kwargs = {
            'password': {'write_only': True},
            're_password': {'write_only': True},
        }

    def validate(self, attrs):
        """Validate password and re_password, then remove re_password."""
        if attrs.get('password') != attrs.get('re_password'):
            raise serializers.ValidationError({"re_password": "Passwords do not match."})
        
        # Remove re_password before passing to parent validate
        attrs = attrs.copy()
        attrs.pop('re_password', None)
        
        # Call Djoser's validate method
        return super().validate(attrs)

    def create(self, validated_data):
        """Create a new user, ensuring re_password is not passed."""
        # Remove re_password (should already be gone, but ensure it)
        validated_data = validated_data.copy()
        validated_data.pop('re_password', None)
        
        # Explicitly define fields for create_user
        user_data = {
            'email': validated_data.get('email'),
            'first_name': validated_data.get('first_name', ''),
            'last_name': validated_data.get('last_name', ''),
            'phone_number': validated_data.get('phone_number', ''),
            'investment_goal': validated_data.get('investment_goal', ''),
            'risk_tolerance': validated_data.get('risk_tolerance', ''),
            'account_type': validated_data.get('account_type', ''),
            'choose_trades': validated_data.get('choose_trades', False),
            'country': validated_data.get('country', ''),
        }
        user = User.objects.create_user(
            password=validated_data.get('password'),
            **user_data
        )
        return user



class CustomUserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='public_id', read_only=True)
    class Meta:
        model = User
        exclude = ("is_active", "is_staff", "is_superuser", "password", "groups", "user_permissions")

class WalletAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletAddres
        fields = ['btc', 'eth', 'usdt']


class FinancesSerializers(serializers.ModelSerializer):
    total_balance = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)

    class Meta:
        model = Finance
        fields = [
            'total_deposit', 'total_profit', 'total_balance'
        ]


class RecentTransactionSerializer(serializers.ModelSerializer):
    time_since_created = serializers.SerializerMethodField()
    id = serializers.CharField(source='public_id', read_only=True)

    class Meta:
        model = RecentTransaction
        fields = [
            'id',
            'transaction_id',
            'network',
            'type',
            'currency',
            'status',
            'amount',
            'date',
            'time_since_created',
        ]
        read_only_fields = ['transaction_id', 'date', 'time_since_created']

    def get_time_since_created(self, obj):
        return obj.time_since_created()
    

class KYCSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYC
        fields = ['user', 'id_type', 'id_front_url', 'id_back_url', 'kyc_status']
        read_only_fields = ['user', 'kyc_status']

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['user', 'account_name', 'bank_name', 'account_number', 'routing_number', 'wallet_address', 'network']
        read_only_fields = ['user']

    def validate(self, data):
        bank_fields = ['account_name', 'bank_name', 'account_number', 'routing_number']
        crypto_fields = ['wallet_address', 'network']

        has_bank = any(data.get(field) for field in bank_fields)
        has_crypto = any(data.get(field) for field in crypto_fields)

        if not has_bank and not has_crypto:
            raise serializers.ValidationError("You must provide either bank details or crypto details.")

        return data
