from django.contrib import admin
from .models import Menu, ServiceLocation,Card,Favourite
from nested_admin import NestedModelAdmin, NestedTabularInline, NestedStackedInline
# Register your models here.

@admin.register(Favourite)
class AdminFavourite(admin.ModelAdmin):
	list_display = ['id', 'user', 'card']


admin.site.register(Menu)
# admin.site.register(Card)


class AdminMenu(NestedStackedInline):
	model = Menu
	extra = 2
	max_num = 7
	can_delete = True
	list_display = ['id', 'menu_id', 'name', 'card']



@admin.register(Card)
class AdminCard(NestedModelAdmin):
	list_display = ['id', 'card_id', 'title', 'price', 'duration', 'service_location', 'is_feature', 'is_active']
	list_editable = ['is_feature', 'is_active']
	list_filter = ['is_active', 'is_feature', 'service_location']
	search_fields = ['title', 'service_location', 'card_id']
	list_per_page = 10

	inlines = [AdminMenu]






admin.site.register(ServiceLocation)



