from django.core.validators import MinValueValidator
from django.db import models


class Position(models.Model):
    """Должность работника"""

    title = models.CharField("Должность", max_length=32)

    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"
        ordering = ('title',)

    def __str__(self):
        return f"{self.pk} - {self.title}"


class Employee(models.Model):
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
        verbose_name="Должность",
        related_name='employees',
    )
    boss = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Начальник",
        related_name='workers'
    )

    class Meta:
        verbose_name = "Работник"
        verbose_name_plural = "Работники"

    def __str__(self):
        return f"{self.pk} - {self.second_name} {self.first_name} {self.patronymic}"
