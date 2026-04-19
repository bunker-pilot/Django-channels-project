from django.contrib import admin
from .models import Category, Server, Channel
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display =["name"]


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ["name"]
