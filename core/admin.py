from django.contrib import admin
from core.models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('tag', 'date', 'content','post_id', 'photo' )
    search_fields = ('tag', 'date', 'post_id')
    
admin.site.register(Post,PostAdmin)
