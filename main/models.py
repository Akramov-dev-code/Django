from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=255)
    age = models.PositiveBigIntegerField(default=5)
    is_active = models.BooleanField(default=True)
    birth_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
