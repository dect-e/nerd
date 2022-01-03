from django.contrib import admin
from django.db.models import Q
from django.utils import timezone
from admin_auto_filters.filters import AutocompleteFilter

from .models import *

class EventActiveFilter(admin.SimpleListFilter):
    title = 'Active'
    parameter_name = 'active'

    def lookups(self, request, model_admin):
        return (
            ('True', 'Active'),
            ('False', 'Inactive'),
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            now = timezone.now()
            if self.value() == 'True':
                return queryset.filter(start__lte=now, end__gt=now)
            else:
                return queryset.filter(Q(start__gt=now) | Q(end__lte=now))
        return queryset

class EventAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'start',
        'end',
        'is_active',
    )
    list_filter = (
        'start',
        'end',
        EventActiveFilter,
    )
    search_fields = (
        'name',
    )

    @staticmethod
    def is_active(obj):
        return obj.is_active()

class OwnerFilter(AutocompleteFilter):
    title = 'Owner'
    field_name = 'owner'

class EventFilter(AutocompleteFilter):
    title = 'Event'
    field_name = 'event'

class CallgroupMemberAdminInline(admin.TabularInline):
    model = CallgroupMembership
    fk_name = 'callgroup'
    verbose_name = 'Callgroup Member'
    extra = 1

class CallgroupMembershipAdminInline(admin.TabularInline):
    model = CallgroupMembership
    fk_name = 'extension'
    extra = 1

class ExtensionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'number',
        'event',
        'extension_type',
        'owner',
    )
    list_filter = (
        'extension_type',
        EventFilter,
        OwnerFilter,
    )
    inlines = (
        CallgroupMemberAdminInline,
        CallgroupMembershipAdminInline,
    )

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            if not (isinstance(inline, CallgroupMemberAdminInline) and obj.extension_type != ExtensionType.CALLGROUP):
                yield inline.get_formset(request, obj), inline

class CallgroupMembershipAdmin(admin.ModelAdmin):
    list_display = (
        'extension',
        'callgroup',
        'accepted',
        'paused',
    )

admin.site.register(Event, EventAdmin)
admin.site.register(Extension, ExtensionAdmin)
admin.site.register(CallgroupMembership, CallgroupMembershipAdmin)
