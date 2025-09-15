from django.contrib import admin
from .models import User, LoginAttempt, Token, AccessTokenBlacklist

admin.site.register(User)
admin.site.register(LoginAttempt)
admin.site.register(Token)
admin.site.register(AccessTokenBlacklist)
