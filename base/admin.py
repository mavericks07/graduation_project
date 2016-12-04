from django.contrib import admin
from .models import User, Organization, StorageSites


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'organization')


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class StorageSitesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(User, UserAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(StorageSites, StorageSitesAdmin)