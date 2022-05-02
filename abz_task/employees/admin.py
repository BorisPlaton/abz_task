from django.contrib import admin

from employees.models import Employee, Position


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'second_name',
        'patronymic',
        'position',
        'payment',
        'view_boss',
    )
    list_display_links = (
        'first_name',
        'second_name',
        'patronymic',
    )
    search_fields = (
        'first_name',
    )
    ordering = (
        'first_name',
        'second_name',
        'patronymic',
    )

    def view_boss(self, obj):
        return obj.boss

    view_boss.empty_value_display = "Без начальник"
    view_boss.short_description = "Начальник"

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
