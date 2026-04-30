from django.contrib import admin
from .models import CustomUser, ConfirmationCode

admin.site.register(CustomUser)
admin.site.register(ConfirmationCode)