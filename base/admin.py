from django.contrib import admin
from .models import User, Organization, StorageSites, Approve


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'organization')


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class StorageSitesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class ApproveAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'type')

admin.site.register(User, UserAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(StorageSites, StorageSitesAdmin)
admin.site.register(Approve, ApproveAdmin)
