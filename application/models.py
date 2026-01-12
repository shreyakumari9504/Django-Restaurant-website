from django.db import models
from django.utils import timezone


# =========================
# 🍽️ TABLE BOOKING MODEL
# =========================
class enquiry_table(models.Model):

    STATUS_CHOICES = (
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
    )

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    people = models.PositiveIntegerField(default=1)

    subject = models.CharField(
        max_length=200,
        default="Table Booking"
    )

    message = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='booked'
    )

    # ✅ SINGLE DATE FIELD (NO created_at CONFUSION)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} | {self.date.strftime('%d-%m-%Y %H:%M')}"


# =========================
# 📩 CONTACT / ENQUIRY MODEL
# =========================
class enquiry_table_1(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    subject = models.CharField(max_length=200)
    message = models.TextField()

    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} | {self.subject}"
