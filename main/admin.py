from django.contrib import admin

from .models import *


class FolderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


class AccessAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'value', 'folder')
    list_display_links = ('id', 'name', 'value', 'folder')
    search_fields = ('name', 'value', 'folder')


class UserAccessAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'access')


class UserKeysAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'public_key', 'private_key')


class UserAdminAdmin(admin.ModelAdmin):
    list_display = ('id', 'folder', 'user')
    list_display_links = ('id', 'folder', 'user')
    search_fields = ('id', 'folder', 'user')


admin.site.register(Folder, FolderAdmin)
admin.site.register(Access, AccessAdmin)
admin.site.register(UserAccess, UserAccessAdmin)
admin.site.register(UserKeys, UserKeysAdmin)
admin.site.register(UserAdmin, UserAdminAdmin)
