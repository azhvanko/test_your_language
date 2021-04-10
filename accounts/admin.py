from django.contrib import admin

from accounts.models import ActivationLink


class ActivationLinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',)
    list_display_links = ('user',)
    search_fields = ('user__username',)


admin.site.register(ActivationLink, ActivationLinkAdmin)
