from django.core.validators import MinValueValidator
from django.db import models
from mptt.models import TreeForeignKey, MPTTModel


class Position(models.Model):
    """Должность работника"""

    title = models.CharField("Должность", max_length=32)

    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"
        ordering = ['title']

    def __str__(self):
        return f"{self.title}"


class Employee(MPTTModel):
    """Работник"""

    first_name = models.CharField(
        "Имя",
        max_length=32,
    )
    second_name = models.CharField(
        "Фамилия",
        max_length=32,
    )
    patronymic = models.CharField(
        "Отчество",
        max_length=32,
    )
    slug = models.SlugField(
        "Slug",
        max_length=128,
        unique=True,
    )
    date_employment = models.DateTimeField(
        "Дата трудоустройства",
    )
    payment = models.IntegerField(
        "Зарплата",
        validators=[
            MinValueValidator(
                0,
                message="Заработная плата не может быть меньше нуля."
            )
        ],
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Должность",
        related_name='employees',
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Начальник",
        related_name='workers'
    )

    class MTTPMeta:
        ordering_insertion_by = ['first_name']
        verbose_name = "Работник"
        verbose_name_plural = "Работники"

    def __str__(self):
        return f"{self.second_name} {self.first_name} {self.patronymic}"

    def delete(self, using=None, keep_parents=False):
        if self.workers and self.parent:
            Employee.objects.filter(parent=self).update(parent=self.parent)
        super().delete(using, keep_parents)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.slug += f'-{self.pk}'
        super(Employee, self).save(*args, **kwargs)

