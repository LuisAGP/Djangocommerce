from django.contrib import admin
from .models import Profile, User, ValidateEmail

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    pass

class ProfileAdmin(admin.ModelAdmin):
    pass

class ValidateEmailAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(ValidateEmail, ValidateEmailAdmin)
