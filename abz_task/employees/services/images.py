from PIL import Image


class ProfilePhoto:
    """Класс `ProfilePhoto`, что предоставляет возможность изменения размеров изображения."""

    def __init__(self, img_path: str):
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

    def save(self, path: str = None) -> None:
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
