from django.contrib import admin
from .models import TransactionHistory

@admin.register(TransactionHistory)
class TransactionHistoryAdmin(admin.ModelAdmin):
    list_display = ('account', 'amount', 'balance_after', 'description', 'inout_type', 'transaction_method', 'transaction_datetime', 'created_at')
    list_filter = ('inout_type', 'transaction_method', 'transaction_datetime')
    search_fields = ('description', 'account__account_number')
    date_hierarchy = 'transaction_datetime'
    ordering = ('-transaction_datetime',)
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('account', 'amount', 'balance_after', 'description')
        }),
        ('거래 정보', {
            'fields': ('inout_type', 'transaction_method', 'transaction_datetime')
        }),
    )
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['account'].label = '계좌'
        form.base_fields['amount'].label = '거래금액'
        form.base_fields['balance_after'].label = '거래후 잔액'
        form.base_fields['description'].label = '설명'
        form.base_fields['inout_type'].label = '입출금 구분'
        form.base_fields['transaction_method'].label = '거래 방법'
        form.base_fields['transaction_datetime'].label = '거래 일시'
        
        # 필수 필드 지정
        form.base_fields['account'].required = True
        form.base_fields['amount'].required = True
        form.base_fields['balance_after'].required = True
        form.base_fields['description'].required = True
        form.base_fields['inout_type'].required = True
        form.base_fields['transaction_method'].required = True
        form.base_fields['transaction_datetime'].required = True
        
        return form
        
    def has_add_permission(self, request):
        return True
        
    def has_change_permission(self, request, obj=None):
        return True
        
    def has_delete_permission(self, request, obj=None):
        return True 