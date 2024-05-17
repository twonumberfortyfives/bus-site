import pathlib
import uuid

from django.db import models
from django.utils.text import slugify

from app import settings


class Facility(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'facilities'

    def __str__(self):
        return self.name


def bus_image_path(instance: "Bus", filename: str) -> pathlib.Path:
    file_name = f"{slugify(instance.info)}-{uuid.uuid4()}" + pathlib.Path(filename).suffix  # random uuid for img
    return pathlib.Path("upload/buses/") / pathlib.Path(file_name)  # path where will storage all files


class Bus(models.Model):
    info = models.CharField(max_length=255, null=True)
    num_seats = models.IntegerField()
    facilities = models.ManyToManyField("Facility", related_name="buses")
    image = models.ImageField(null=True, upload_to=bus_image_path)

    class Meta:
        verbose_name_plural = "buses"

    @property
    def is_small(self):
        return self.num_seats <= 25

    def __str__(self):
        return f"Bus: {self.info} (id = ({self.id})) Seats: {self.num_seats}"


class Trip(models.Model):
    source = models.CharField(max_length=63)
    destination = models.CharField(max_length=63)
    departure = models.DateTimeField()
    bus = models.ForeignKey("Bus", on_delete=models.CASCADE, related_name="trips")

    class Meta:
        indexes = [
            models.Index(fields=["source", "destination"]),  # создает таблицы по заданым полям и соеденяет их индексами для быстрого поиска по этим полям
            models.Index(fields=["departure"])
        ]

    def __str__(self):
        return f"{self.source} - {self.destination} ({self.departure})"


class Ticket(models.Model):
    seat = models.IntegerField()
    trip = models.ForeignKey("Trip", on_delete=models.CASCADE, related_name="tickets")
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="tickets")

    class Meta:
        # constraints = [
        #     UniqueConstraint(fields=["seat", "trip"], name="unique_ticket_seat_trip")  # вариации полей который должны быть уникальны
        # ]
        unique_together = ("seat", "trip")
        ordering = ["seat"]

    def __str__(self):
        return f"{self.seat} - (seat: {self.seat})"

    @staticmethod
    def validate_seat(seat: int, num_seats: int, error_to_raise):
        if not (1 <= seat <= num_seats):
            raise error_to_raise(
                {
                    "seat": f"Seat must be in range [1, {num_seats}], not {seat}"
                }
            )

    def clean(self):  # валидирует поля перед отправления данных в базу. В данном случае поля поля на билетах и в автобусе
        # if not (1 <= self.seat <= self.trip.bus.num_seats):
        #     raise ValueError({
        #         "seat": f"seat must be in range [1, {self.trip.bus.num_seats}, not {self.seat}]"
        #     })
        Ticket.validate_seat(self.seat, self.trip.bus.num_seats, ValueError)

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
    ):  # по идеии данная функция вызывается перед сохранением обьекта как раз таки для валидации
        self.clean_fields()
        return super(Ticket, self).save(force_insert, force_update, using, update_fields)


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.created_at)
