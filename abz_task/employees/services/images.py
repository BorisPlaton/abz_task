import os

from PIL import Image

from employees.models import Employee


class ProfilePhoto:
    """Класс `ProfilePhoto`, что предоставляет возможность изменения размеров изображения."""

    def __init__(self, img_path: str):
        """
        Инициализация класса.

        :param img_path: Абсолютный путь к изображению.
        """
        self.photo_path = img_path
        self.photo = Image.open(self.photo_path)

    def get_square_photo(self, height: int = 250) -> None:
        """
        Делает фото квадратным.

        :param height: Высота нового изображения.
        """

        # Соотношение размеров исходного фото и ожидаемого
        delta = self.height // height

        self.photo = self.photo.resize((self.width // delta, self.height // delta))
        self.center_crop_image((height, height))

    def center_crop_image(self, size: tuple[int, int] = (250, 250)) -> None:
        """
        Обрезает фото по центру.

        :param size: Размер нового изображения.
        """

        self.photo = self.photo.crop(self.center_box_of_image(size))

    def center_box_of_image(self, size: tuple[int, int]) -> tuple[int, int, int, int]:
        """
        Возвращает координаты верхней левой, нижней правой границы
        от центра фото.

        :param size: Размер области от центра фото.
        """

        x_center = self.photo.width // 2
        half_height = size[0] // 2
        x1 = x_center - half_height
        x2 = x_center + half_height

        y_center = self.photo.height // 2
        half_width = size[1] // 2
        y1 = y_center - half_width
        y2 = y_center + half_width

        return x1, y1, x2, y2

    def save_photo(self, path: str = None) -> None:
        """
        Сохраняет изображение.

        :param path: Путь, по которому сохраняется фото.
        """

        if not path:
            path = self.photo_path
        self.photo.save(path)

    @property
    def height(self) -> int:
        return self.photo.height

    @property
    def width(self) -> int:
        return self.photo.width


def delete_photo(employee: Employee) -> bool:
    """
    Удаляет фотографию работника экземпляра класса `Employee`.

    Возвращает True, если модель фото было удалено, иначе False.

    :param employee: экземпляр класса `Employee`.
    """

    try:
        old_photo = Employee.objects.get(pk=employee.pk).employee_photo
        old_photo_path = old_photo.path
        new_photo = employee.employee_photo
    except Employee.DoesNotExist:
        pass
    else:
        # Если прошлое фото не является стандартным, тогда удаляем его.
        if old_photo != Employee._meta.get_field('employee_photo').default and old_photo != new_photo:
            os.remove(old_photo_path)
            return True

    return False


def change_employee_photo(employee_photo: str) -> None:
    """
    Урезает загруженную фотографию работника до разрешенных размеров.

    :param employee_photo: Название фотографии.
    """

    # Меняем только загруженные фотографии
    if employee_photo != Employee._meta.get_field('employee_photo').default:
        profile_pic = ProfilePhoto(employee_photo.path)
        profile_pic.get_square_photo()
        profile_pic.save_photo()
