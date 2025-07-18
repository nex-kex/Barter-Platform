from django.db import models

from users.models import User


class Ad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ads", verbose_name="Создатель")
    title = models.CharField(max_length=60, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    image_url = models.ImageField(upload_to="ads/", blank=True, null=True, verbose_name="Изображение")
    category = models.CharField(max_length=20, verbose_name="Категория")
    condition = models.CharField(
        max_length=11,
        choices=[
            ("new", "новый"),
            ("used", "б/у"),
            ("display", "витринный"),
            ("discounted", "уцененный"),
            ("refurbished", "восстановленный"),
            ("incomplete", "недоукомплектованный"),
            ("expiring", "заканчивается срок годности"),
            ("returned", "продается повторно"),
            ("other", "другое"),
        ],
        verbose_name="Состояние",
    )
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["created_at"]


class ExchangeProposal(models.Model):
    ad_sender = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="sending", verbose_name="Отправление")
    ad_receiver = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="receiving", verbose_name="Получение")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    status = models.CharField(
        max_length=8,
        choices=[("waiting", "ожидает"), ("accepted", "принята"), ("declined", "отклонена")],
        default="waiting",
        verbose_name="Статус",
    )
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Предложение номер {self.pk}"

    class Meta:
        verbose_name = "Предложение"
        verbose_name_plural = "Предложения"
        ordering = ["created_at"]
