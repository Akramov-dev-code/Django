from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=255)
    age = models.PositiveBigIntegerField(default=5)
    is_active = models.BooleanField(default=True)
    birth_date = models.DateField(null=True, blank=True)
    
    courses = models.ManyToManyField("main.Course", related_name="courses", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Student : {self.name} - # {self.id}"
    
        
    class Meta:
        verbose_name = "O'quvchi"
        verbose_name_plural = "O'quvchilar"
        ordering = ["id"]
    
    
class Course(models.Model):
    title = models.CharField(max_length=255)
    price = models.PositiveIntegerField(default=0)
    discount_type_choices = (
        ("flex", "Aniq summa"),
        ("percent", "Foizli")
    )
    discount_type = models.CharField(max_length=10, choices=discount_type_choices)
    discount = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    def final_price(self):
        if self.discount:
            if self.discount_type == "percent":
                return self.price - (self.price / 100 * self.discount)
            return self.price - self.discount
        
        return self.price