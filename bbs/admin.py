from django.contrib import admin

# Register your models here.
from bbs.models import  BBS, Category

class BBS_admin(admin.ModelAdmin):
    list_display = ('title', 'summary', 'author', 'view_count', 'created_time', )
    list_filter = ('created_time', )


admin.site.register(BBS, BBS_admin)
admin.site.register(Category, )



