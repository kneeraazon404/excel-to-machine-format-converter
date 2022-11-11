from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    full_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class StoreNumber(models.Model):
    store_number = models.CharField(max_length=100)

    def __str__(self):
        return self.store_number

    class Meta:
        verbose_name_plural = "Store Numbers"


class MarketId(models.Model):
    market_id = models.CharField(max_length=100)

    def __str__(self):
        return self.market_id

    class Meta:
        verbose_name_plural = "Market IDs"


class TerminalId(models.Model):
    terminal_id = models.CharField(max_length=100)

    def __str__(self):
        return self.terminal_id

    class Meta:
        verbose_name_plural = "Terminal IDs"


class BrandName(models.Model):
    brand_name = models.CharField(max_length=100)

    def __str__(self):
        return self.brand_name

    class Meta:
        verbose_name_plural = "Brand Names"


class Store(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_constraint=False,
    )
    brand_name = models.ForeignKey(
        BrandName,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        db_constraint=False,
    )
    market_id = models.ForeignKey(
        MarketId,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        db_constraint=False,
    )
    store_number = models.ForeignKey(
        StoreNumber,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        db_constraint=False,
    )
    terminal_id = models.ForeignKey(
        TerminalId,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        db_constraint=False,
    )
    uploaded_file = models.FileField(
        upload_to="uploads/",
    )
    converted_file = models.FileField(
        upload_to="converted_files/", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.brand_name

    class Meta:
        verbose_name_plural = "Stores"
