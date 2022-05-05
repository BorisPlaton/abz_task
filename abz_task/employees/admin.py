from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from employees.models import Employee, Position


@admin.register(Employee)
class EmployeeAdmin(MPTTModelAdmin):
    exclude = (
        'slug',
    )
    list_display = (
        'first_name',
        'second_name',
        'patronymic',
        'position',
        'payment',
        'view_parent',
    )
    list_display_links = (
        'first_name',
        'second_name',
        'patronymic',
    )
    search_fields = (
        'first_name',
        'second_name',
        'patronymic',
    )

    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return self.readonly_fields
        return self.readonly_fields + ('slug',)

    def view_parent(self, obj):
        return obj.parent

    view_parent.empty_value_display = "Без начальник"
    view_parent.short_description = "Начальник"

    def delete_queryset(self, request, queryset):
        for obj in queryset.all():
            obj.delete()


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = (
        'title',
    )
    ordering = (
        'title',
    )
