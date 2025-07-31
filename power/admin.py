from django.contrib import admin
from .models import Service, CaseStudy
# from .models import ESGResource



class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "service_type", "display_order")
    list_editable = ("display_order",)
    prepopulated_fields = {"slug": ("title",)}


class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ("title", "client_type", "location", "installation_date")
    list_filter = ("client_type", "service")
    search_fields = ("title", "client_name", "location")
    readonly_fields = ("energy_savings", "savings_percentage")

    fieldsets = (
        (
            "Client Details",
            {"fields": ("title", "client_name", "client_type", "location")},
        ),
        (
            "Project Details",
            {
                "fields": (
                    "service",
                    "installation_date",
                    "system_capacity",
                    "project_cost",
                )
            },
        ),
        ("Energy Metrics", {"fields": ("previous_consumption", "current_consumption")}),
        (
            "Results",
            {"fields": ("energy_savings", "savings_percentage", "testimonial")},
        ),
        ("Media", {"fields": ("featured_image",)}),
    )


# class ESGResourceAdmin(admin.ModelAdmin):
#     list_display = ("title", "resource_type", "published_date", "is_featured")
#     list_filter = ("resource_type", "is_featured")
#     list_editable = ("is_featured",)


admin.site.register(Service, ServiceAdmin)
admin.site.register(CaseStudy, CaseStudyAdmin)
# admin.site.register(ESGResource, ESGResourceAdmin)


# power/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import ServiceRequest, AdminLog


class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "service_display",
        "email",
        "phone",
        "submitted_at",
        "is_completed",
    )
    list_filter = ("service", "is_completed", "submitted_at")
    search_fields = ("name", "email", "phone")
    list_editable = ("is_completed",)
    actions = ["mark_as_completed"]

    def service_display(self, obj):
        return obj.get_service_display()

    service_display.short_description = "Service"

    def mark_as_completed(self, request, queryset):
        queryset.update(is_completed=True)

    mark_as_completed.short_description = "Mark selected requests as completed"


class AdminLogAdmin(admin.ModelAdmin):
    list_display = ("admin_user", "action_display", "timestamp", "ip_address")
    list_filter = ("action", "timestamp")
    readonly_fields = ("admin_user", "action", "details", "timestamp", "ip_address")

    def action_display(self, obj):
        return obj.get_action_display()

    action_display.short_description = "Action"

    def has_add_permission(self, request):
        return False


admin.site.register(ServiceRequest, ServiceRequestAdmin)
admin.site.register(AdminLog, AdminLogAdmin)



