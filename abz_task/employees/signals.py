from django.db.models.signals import pre_delete
from django.dispatch import receiver

from employees.models import Employee


@receiver(pre_delete, sender=Employee, dispatch_uid="changing_boss")
def change_workers_boss(sender, instance, using, **kwargs):
    """
    Меняет начальника у подопечных.

    У подопечных экземпляра класса Employee, если такие есть, меняется начальник
    при его удалении на начальника удаленного начальника. Если такого нет, то
    устанавливается значение None.
    """

    pass

