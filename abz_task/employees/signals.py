import os

from django.db.models.signals import pre_save
from django.dispatch import receiver

from employees.models import Employee


@receiver(pre_save, sender=Employee, dispatch_uid='delete_previous_photos')
def delete_previous_photo(sender, instance: Employee, **kwargs):
    """Удаление старого фото пользователя"""

    try:
        old_photo = Employee.objects.get(pk=instance.pk).employee_photo
        old_photo_path = old_photo.path
        new_photo = instance.employee_photo
        default_photo = Employee._meta.get_field('employee_photo').default
    except Employee.DoesNotExist:
        return
    else:
        # Если прошлое фото поменялось и не является стандартным,
        # тогда удаляем его.
        if old_photo != default_photo and old_photo != new_photo:
            os.remove(old_photo_path)
