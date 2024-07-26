from django.contrib import admin

# Regifster your models here.
from .models import Members

admin.site.register(Members)