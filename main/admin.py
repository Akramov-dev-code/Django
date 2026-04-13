from django.contrib import admin
from main.models import Students, Course

admin.site.register(Students)


class CourseAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "price", "discount", "discount_type", "final_price"]
    list_display_links = ["title", "id"]
    list_filter = ["price"] 
    search_fields = ["title"]

admin.site.register(Course, CourseAdmin)