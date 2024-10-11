from importlib import import_module

from django.conf import settings
from django.contrib import admin

from sessionprofile.models import SessionProfile


@admin.register(SessionProfile)
class SessionProfileAdmin(admin.ModelAdmin):
    list_display = ["session_key", "user", "exists"]

    @property
    def SessionStore(self):

        return import_module(settings.SESSION_ENGINE).SessionStore

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user=request.user)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    @admin.display(boolean=True)
    def exists(self, obj):
        return self.SessionStore().exists(obj.session_key)

    def delete_model(self, request, obj):
        self.SessionStore(obj.session_key).flush()
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):

        session_keys = list(queryset.values_list("session_key", flat=True))
        for session_key in session_keys:
            self.SessionStore(session_key).flush()

        super().delete_queryset(request, queryset)
