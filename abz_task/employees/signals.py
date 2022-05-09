import os

from django.db.models.signals import pre_save, post_save, post_delete, pre_delete
from django.dispatch import receiver

from employees.models import Employee
import employees.services.images as im


@receiver(pre_save, sender=Employee, dispatch_uid='delete_previous_photos')
def delete_previous_photo(sender, instance: Employee, **kwargs):
    """Удаление старого фото пользователя"""

    im.delete_photo(instance)


@receiver(post_save, sender=Employee, dispatch_uid='resize_loaded_employee_photo')
def resize_loaded_employee_photo(sender, instance: Employee, **kwargs):
    """Обрезает загруженное фото пользователя"""

    im.change_employee_photo(instance.employee_photo)


@receiver(pre_delete, sender=Employee, dispatch_uid='delete_old_photo')
def delete_old_photo(sender, instance: Employee, **kwargs):
    """Удаление фото пользователя при удалении его экземпляра"""

    default_photo = Employee._meta.get_field('employee_photo').default
    current_photo = instance.employee_photo
    current_photo_path = current_photo.path

    # Если текущая фотография не является стандартной, тогда удаляем её.
    if default_photo != current_photo:
        os.remove(current_photo_path)


@receiver(post_delete, sender=Employee, dispatch_uid='rebuild_tree')
def rebuild_employee_tree(sender, instance: Employee, **kwargs):
    """Перестраивает дерево работников модели `Employee` после удаление записи"""

    sender.objects.rebuild()
