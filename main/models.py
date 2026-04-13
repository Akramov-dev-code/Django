from django.db import models

class Course(models.Model):
    DISCOUNT_TYPE_CHOICES = (
        ("flex", "Aniq summa"),
        ("percent", "Foizli")
    )

    title = models.CharField(max_length=255, verbose_name="Kurs nomi")
    price = models.PositiveIntegerField(default=0, verbose_name="Asl narxi")
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES, verbose_name="Chegirma turi")
    discount = models.PositiveIntegerField(default=0, verbose_name="Chegirma miqdori")
    
    # Frontend uchun qo'shimcha maydonlar
    icon_class = models.CharField(
        max_length=50, 
        default="fas fa-code", 
        help_text="FontAwesome klassi (masalan: fas fa-code)",
        verbose_name="Belgi (Icon)"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Kurs haqida qisqacha")

    def __str__(self):
        return self.title

    @property
    def final_price(self):
        """Yakuniy narxni hisoblash"""
        if self.discount > 0:
            if self.discount_type == "percent":
                return int(self.price - (self.price * self.discount / 100))
            return self.price - self.discount
        return self.price

    @property
    def discount_display(self):
        """Frontenddagi 'discount-pill' uchun matn generatsiya qilish"""
        if self.discount > 0:
            if self.discount_type == "percent":
                return f"{self.discount}% chegirma"
            return f"{self.discount} so'm chegirma"
        return None

    class Meta:
        verbose_name = "Kurs"
        verbose_name_plural = "Kurslar"


class Students(models.Model):
    name = models.CharField(max_length=255, verbose_name="F.I.SH",default="Abdulloh Akramov")
    phone = models.IntegerField(default=917524233, verbose_name="Phone Number")
    username = models.CharField(max_length=255,blank=True, null=True, verbose_name="Username")

    # related_name='students' bo'lgani ma'qul, chunki kurs ichidan studentlarni chaqirish oson bo'ladi
    courses = models.ManyToManyField("Course", related_name="students", blank=True, verbose_name="Kurslari")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Student: {self.name} - #{self.id}"
    
    def courses_count(self):
        return self.courses.count()
    
    class Meta:
        verbose_name = "O'quvchi"
        verbose_name_plural = "O'quvchilar"
        ordering = ["id"]