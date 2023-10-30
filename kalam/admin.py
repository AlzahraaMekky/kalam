from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Coffee)
admin.site.register(CoffeeSesion)
admin.site.register(Booking)
admin.site.register(Testimonial)