import random

import faker.providers
import pytz as pytz
from faker import Faker
from django.core.management.base import BaseCommand

from employees.models import Position, Employee


class Provider(faker.providers.BaseProvider):

    def position(self):
        return random.choice(list(Position.objects.all()))

    def employee(self):
        try:
            # Возвращаем ничего в 1/10 случаев, чтоб созданный пользователь
            # был вверху иерархии работников
            if not random.randint(0, 9):
                return None
            return random.choice(list(Employee.objects.all()))
        except IndexError:
            pass


class Command(BaseCommand):
    help = "Наполняет БД данными. По умолчанию, Создаёт 10 должностей и 50 работников."

    def add_arguments(self, parser):
        parser.add_argument(
            '-e', '--employees',
            type=int,
            nargs='?',
            const=5,
            default=5,
            help="Количество сотрудников.",
        )

        parser.add_argument(
            '-p', '--positions',
            type=int,
            nargs='?',
            const=5,
            default=5,
            help="Количество должностей.",
        )

    def handle(self, *args, **options):
        self._create_fake_positions(options['positions'])
        self._create_fake_employees(options['employees'])

        self.stdout.write('Записи созданы')

    @staticmethod
    def _create_fake_positions(categories_amount):
        """
        Создание категорий.

        :param categories_amount: Количество новых записей.
        """

        fake = Faker(['ru_RU'])
        for _ in range(categories_amount):
            Position.objects.create(title=fake.unique.job())

    @staticmethod
    def _create_fake_employees(employees_amount):
        """
        Создание работников.

        :param employees_amount: Количество новых записей.
        """

        fake = Faker(['ru_RU'])
        fake.add_provider(Provider)

        for _ in range(employees_amount):
            Employee.objects.create(
                first_name=fake.first_name(),
                second_name=fake.last_name(),
                patronymic=fake.middle_name(),
                date_employment=fake.date_time_this_decade(tzinfo=pytz.UTC),
                payment=fake.random_int(min=100, max=1200),
                position=fake.position(),
                parent=fake.employee(),
            )
