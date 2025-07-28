
# Register your models here.
from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, WalletAddres
from django.db import models
from django.forms import TextInput
from django import forms
from .models import Finance, KYC, RecentTransaction

class WalletAddresInline(admin.StackedInline):
    model = WalletAddres
    extra = 0
    max_num = 1

class FinancesInline(TabularInline):
    model = Finance
    extra = 0
    readonly_fields = ('total_balance',)
    can_delete = False
    show_change_link = True

class KYCInline(TabularInline):
    model = KYC
    extra = 0
    can_delete = False
    show_change_link = True
    fields = ('id_type', 'id_front_url', 'id_back_url', 'kyc_status')

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin, ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'account_type', 'country')
    list_display_links = ('email', 'first_name', 'last_name')
    list_filter = ('account_type', 'risk_tolerance', 'country')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number', 'country')
    ordering = ('email',)
    list_per_page = 25
    list_max_show_all = 100

    fieldsets = (
        ("Login Info", {
            'fields': ('email', 'password')
        }),
        ("Personal Info", {
            'fields': ('first_name', 'last_name', 'phone_number')
        }),
        ("Investment Details", {
            'fields': ('investment_goal', 'risk_tolerance', 'account_type', 'choose_trades')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    inlines = [FinancesInline, KYCInline]



class WalletAddresForm(forms.ModelForm):
    class Meta:
        model = WalletAddres
        fields = '__all__'
        widgets = {
            'btc': forms.TextInput(attrs={'placeholder': 'Enter BTC address', 'style': 'width: 400px;'}),
            'eth': forms.TextInput(attrs={'placeholder': 'Enter ETH address', 'style': 'width: 400px;'}),
            'usdt': forms.TextInput(attrs={'placeholder': 'Enter USDT address', 'style': 'width: 400px;'}),
        }


@admin.register(WalletAddres)
class WalletAddresAdmin(admin.ModelAdmin):
    form = WalletAddresForm
    list_display = ('btc', 'eth', 'usdt')
    actions = ['delete_selected']
    actions_on_top = True
    actions_on_bottom = True


@admin.register(Finance)
class FinancesAdmin(ModelAdmin):
    list_display = ('user_email', 'total_deposit', 'total_profit', 'total_balance_display')
    list_display_links = ('user_email',)
    search_fields = ('user__email',)
    list_filter = ('user__account_type',)
    list_per_page = 25
    list_max_show_all = 100

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'

    def total_balance_display(self, obj):
        return f"{obj.total_balance:.2f}"
    total_balance_display.short_description = 'Total Balance'

@admin.register(RecentTransaction)
class RecentTransactionAdmin(ModelAdmin):
    list_display = (
        'user_email','transaction_id', 'network', 'type', 'currency',
        'status', 'amount', 'date', 'time_since_created'
    )
    list_display_links = ('user_email', 'transaction_id')
    search_fields = ('user__email', 'transaction_id')
    list_filter = ('network', 'type', 'status')
    list_per_page = 25
    list_max_show_all = 100

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'

    def time_since_created(self, obj):
        return obj.time_since_created()
    time_since_created.short_description = 'Time Since'

@admin.register(KYC)
class KYCAdmin(ModelAdmin):
    list_display = ('user', 'id_type', 'kyc_status')
    list_filter = ('kyc_status', 'id_type')
    search_fields = ('user__email',)
    list_per_page = 25
