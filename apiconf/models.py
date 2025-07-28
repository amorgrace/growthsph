from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    INVESTMENT_GOAL_CHOICES = [
        ('select_your_primary_goal', 'Select Your Primary Goal'),
        ('retirement_planning', 'Retirement Planning'),
        ('wealth_building', 'Wealth Building'),
        ('education_funding', 'Education Funding'),
        ('home_purchase', 'Home Purchase'),
        ('general_investing', 'General Investing'),
    ]

    investment_goal = models.CharField(
        max_length=50, 
        choices=INVESTMENT_GOAL_CHOICES, 
        default='select_your_primary_goal'
    )

    RISK_TOLERANCE_CHOICES = [
        ('select_your_risk_tolerance', 'Select Your Risk Tolerance'),
        ('conservative_low_risk', 'Conservative - Low Risk'),
        ('moderate_balanced_risk', 'Moderate - Balance Risk'),
        ('aggressive_high_risk', 'Aggressive - High Risk'),
    ]

    risk_tolerance = models.CharField(
        max_length=50,
        choices=RISK_TOLERANCE_CHOICES,
        default='select_your_risk_tolerance',
    )

    ACCOUNT_TYPE_CHOICES = [
        ('choose_account_type', 'Choose Account Type'),
        ('starter_plan', 'Starter Plan'),
        ('silver_plan', 'Silver Plan'),
        ('gold_plan', 'Gold Plan'),
    ]

    account_type = models.CharField(
        max_length=50,
        choices=ACCOUNT_TYPE_CHOICES,
        default='choose_account_type'
    )

    CHOOSE_TRADES_CHOICES = [
        ('crypto', 'Crypto'),
        ('crude', 'Crude'),
        ('gold', 'Gold'),
        ('stock', 'Stock'),
        ('cfd', 'CFD'),
        ('fx', 'FX'),
    ]

    choose_trades = models.CharField(
        max_length=20,
        choices=CHOOSE_TRADES_CHOICES,
    )

    def __str__(self):
        return self.email



class WalletAddres(models.Model):
    btc = models.CharField(max_length=100, blank=True)
    eth = models.CharField(max_length=100, blank=True)
    usdt = models.CharField(max_length=100, blank=True)


class Finance(models.Model):
    total_deposit = models.DecimalField(default=0, decimal_places=2, max_digits=15)
    total_profit = models.DecimalField(default=0, decimal_places=2, max_digits=15)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='finances')

    @property
    def total_balance(self):
        return self.total_deposit + self.total_profit
    
    def __str__(self):
        return f"{self.user.email} | Balance: {self.total_balance:.2f} | Deposit: {self.total_deposit:.2f} | Profit: {self.total_profit:.2f}"


class RecentTransaction(models.Model):
    NETWORK_CHOICES = [
        ('bitcoin', 'Bitcoin'),
        ('ethereum', 'Ethereum'),
        ('solana', 'Solana'),
        ('tron', 'TRC'),
        ('cardono', 'Cardono'),
    ]

    CURRENCY_CHOICES = [
        ('btc', 'BTC'),
        ('eth', 'ETH'),
        ('sol', 'SOL'),
        ('trc20', 'TRC20'),
        ('crd', 'CRD'),
    ]


    TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('failed', 'Failed'),
    ]

    transaction_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='transactions')
    network = models.CharField(max_length=10, choices=NETWORK_CHOICES, default='bitcoin')
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default='btc')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='deposit')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    amount = models.DecimalField(max_digits=18, decimal_places=8)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.network} - {self.type} - {self.amount}"

    def time_since_created(self):
        from django.utils.timesince import timesince
        return timesince(self.date) + " ago"
    

class KYC(models.Model):

    DOCUMENT_TYPE_CHOICES = [
        ('passport', 'Passport'),
        ('drivers_license', "Driver's license"),
        ('national_id', 'National ID'),
    ]

    KYC_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_review', 'In Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    id_type = models.CharField(
        max_length=20,
        choices=DOCUMENT_TYPE_CHOICES,
        default='passport'
    )
    id_front_url = models.URLField(blank=True, null=True)
    id_back_url = models.URLField(blank=True, null=True)
    kyc_status = models.CharField(
        max_length=20,
        choices=KYC_STATUS_CHOICES,
        default='in_review'
    )