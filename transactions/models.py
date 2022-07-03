from django.db import models
from django.urls import reverse

# Create your models here.

TYPE_CHOICES = (
    ("CR", "Credit"),
    ("DB", "Debit"),
)


class Transaction(models.Model):
    description = models.CharField(max_length=60)
    amount = models.IntegerField()
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    date = models.DateField()
    notes = models.TextField(blank=True)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    last_updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse("transactions:transaction_details", args=(self.pk,))
