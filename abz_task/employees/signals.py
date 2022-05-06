import os

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from employees.models import Employee
from employees.services.services import change_employee_photo


@receiver(pre_save, sender=Employee, dispatch_uid='delete_previous_photos')
def delete_previous_photo(sender, instance: Employee, **kwargs):
    """Удаление старого фото пользователя"""

    try:
        old_photo = Employee.objects.get(pk=instance.pk).employee_photo
        old_photo_path = old_photo.path
        new_photo = instance.employee_photo
    except Employee.DoesNotExist:
        return
    else:
        # Если прошлое фото не является стандартным, тогда удаляем его.
        if old_photo != Employee._meta.get_field('employee_photo').default and old_photo != new_photo:
            os.remove(old_photo_path)


@receiver(post_save, sender=Employee, dispatch_uid='resize_loaded_employee_photo')
def resize_loaded_employee_photo(sender, instance: Employee, **kwargs):
    """Обрезает загруженное фото пользователя"""

    change_employee_photo(instance.employee_photo)
