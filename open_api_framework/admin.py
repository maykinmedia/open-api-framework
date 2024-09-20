from importlib import import_module

from django.conf import settings
from django.contrib import admin

from sessionprofile.models import SessionProfile


@admin.register(SessionProfile)
class SessionProfileAdmin(admin.ModelAdmin):
    list_display = ["session_key", "user", "exists"]

    def __init__(self, model, admin_site):
        engine = import_module(settings.SESSION_ENGINE)
        self.SessionStore = engine.SessionStore
        super().__init__(model, admin_site)

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

    def expiration_time(self, obj):

        session = self.SessionStore(obj.session_key)

        if session.exists(obj.session_key):
            return session.get_expiry_date()
        return None

    def delete_model(self, request, obj):
        self.SessionStore(obj.session_key).flush()
        super().delete_model(request, obj)
