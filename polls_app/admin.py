from django.contrib import admin
from .models import Poll, Choice


class ChoiceAdmin(admin.ModelAdmin):
    readonly_fields = ('votes', )


admin.site.register(Poll)
admin.site.register(Choice, ChoiceAdmin)
