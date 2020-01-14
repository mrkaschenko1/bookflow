from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Profile, Avatar, ModRequest

# Register your models here.

# admin.site.register(Profile)
# admin.site.register(Avatar)
admin.site.unregister(Group)
admin.site.unregister(User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'is_active']
    fields = ('is_active',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ModRequest)
class ModRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'accepted']
    list_filter = ('accepted',)
    ordering = ('accepted',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

# admin.site.register(ModRequest)
