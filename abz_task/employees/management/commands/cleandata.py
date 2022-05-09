from django.core.management.base import BaseCommand

from employees.models import Position, Employee


class Command(BaseCommand):
    help = "Очищает данные таблицы из БД"

    def add_arguments(self, parser):
        parser.add_argument(
            '-e', '--employees',
            action='store_true',
            default=False,
            help="Выбирает таблицу с записями работников.",
        )

        parser.add_argument(
            '-p', '--positions',
            action='store_true',
            default=False,
            help="Выбирает таблицу с записями должностей.",
        )

    def handle(self, *args, **options):

        if options['employees']:
            self.stdout.write('Записи `employee` удалены')
            self.__delete_data_from(Employee)

        if options['positions']:
            self.stdout.write('Записи `position` удалены')
            self.__delete_data_from(Position)

        if not (options['employees'] or options['positions']):
            self.__delete_data_from(Employee)
            self.__delete_data_from(Position)
            self.stdout.write('Записи удалены')

    @staticmethod
    def __delete_data_from(table):
        """Удаляет все данные из таблицы `table`."""

        table.objects.all().delete()
