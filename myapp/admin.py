from django.contrib import admin
from myapp.models import *

admin.site.register(user_info)
admin.site.register(Train)
admin.site.register(Seat)
admin.site.register(Ticket)
# Register your models here.
