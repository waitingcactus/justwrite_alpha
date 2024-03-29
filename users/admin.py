from django.contrib import admin
from .models import User, Profile
from projects.models import Project
from forest.models import Tree, Forest


class ProjectInline(admin.TabularInline):
    model = Project
    extra = 1


class TreeInline(admin.TabularInline):
    model = Tree
    extra = 1


class MyUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    readonly_fields = ['password', 'date_joined', 'last_login']
    fieldsets = [
        (None, {'fields': ['username']}),
        (None, {'fields': ['email']}),
        (None, {'fields': ['password']}),
        (None, {'fields': ['date_joined']}),
        (None, {'fields': ['last_login']}),
        (None, {'fields': ['is_active']}),
        (None, {'fields': ['is_admin']}),
        (None, {'fields': ['is_staff']}),
        (None, {'fields': ['is_superuser']}),
    ]
    inlines = [ProjectInline]


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)


class ForestAdmin(admin.ModelAdmin):
    list_display = ('user',)
    inlines = [TreeInline]


admin.site.register(User, MyUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Forest, ForestAdmin)
