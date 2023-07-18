from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .forms import SignupForm
from .models import User


# class Admin(UserAdmin):
#     add_form = SignupForm

#     model = User
#     list_display = ["username", "nickname", "is_staff", "is_active"]
#     list_filter = ["username"]
#     fieldsets = [
#         (None, {"fields": ["username", "password"]}),
#         ("Nickname", {"fields": ["nickname"]}),
#         ("Permissions", {"fields": ["is_staff"]}),
#     ]

#     add_fieldsets = [
#         (None, {"classes": ["wide"], "fields": ["username", "nickname", "password1", "password2"]})
#     ]

#     search_fields = ["username"]
#     ordering = ["username"]
#     filter_horizontal = []

admin.site.register(User)
# admin.site.register(User, Admin)
# admin.site.unregister(Group)