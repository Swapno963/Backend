from django.contrib import admin
from .models import CustomUser, UserProfile, SupplierProfile
from nested_admin import NestedModelAdmin, NestedTabularInline, NestedStackedInline
# Register your models here.


class UserProfileAdmin(NestedStackedInline):
	model = UserProfile
	extra = 1
	max_num = 1
	can_delete = False
	list_display = ['user', 'address']

class SupplierProfileAdmin(NestedStackedInline):
	model = SupplierProfile
	extra = 1
	max_num = 1
	can_delete = False
	list_display = ['user', 'address' ] 



@admin.register(CustomUser)
class CustomUserAdmin(NestedModelAdmin):
        
    list_display = ('id', 'name', 'phone', 'email', 'role', 'joined_date', 'is_active',)
    list_display_links = ('email', 'name',)
    readonly_fields = ('phone', 'last_login', 'joined_date',)
    ordering = ('-joined_date',)

    filter_horizontal = ()
    list_filter = ('role', 'is_active',)
    fieldsets = ()

    def get_inline_instances(self, request, obj=None):
        inlines = []
        if obj:
            if obj.role == 'supplier':
                inlines.append(SupplierProfileAdmin(self.model, self.admin_site))
            elif obj.role == 'customer':
                inlines.append(UserProfileAdmin(self.model, self.admin_site))
        return inlines