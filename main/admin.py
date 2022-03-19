from django.contrib import admin

from .models import *


class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


class AccessAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'value', 'file')
    list_display_links = ('id', 'name', 'value', 'file')
    search_fields = ('name', 'value', 'file')


class UserAccessAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'access')


class UserKeysAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'public_key', 'private_key')


class UserAdminAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'user')
    list_display_links = ('id', 'file', 'user')
    search_fields = ('id', 'file', 'user')


admin.site.register(File, FileAdmin)
admin.site.register(Access, AccessAdmin)
admin.site.register(UserAccess, UserAccessAdmin)
admin.site.register(UserKeys, UserKeysAdmin)
admin.site.register(UserAdmin, UserAdminAdmin)
