from django.contrib import admin
from .models import Poll, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1
    exclude = ('votes', 'passed_users')


class PollAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    exclude = ('date_added', 'passed_users',)


class ChoiceAdmin(admin.ModelAdmin):
    readonly_fields = ('votes', )


admin.site.register(Poll, PollAdmin)
admin.site.register(Choice, ChoiceAdmin)
