from django.contrib import admin
from .models import Post, Category, Tag


class PostAdmin(admin.ModelAdmin):
    # list_display属性允许你在设置一些你想要在管理对象列表页面显示的模型（model）字段。
    # 侧边栏允许你根据list_filter属性中指定的字段来过滤返回结果
    # search_fields属性定义了一个搜索字段列, 一个搜索框也应用在页面中
    # 搜索框的下方，有个可以通过时间层快速导航的栏，该栏通过定义date_hierarchy属性出现。 
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title', )}
    raw_id_fields = ('author', )
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']

admin.site.register(Post, PostAdmin)


admin.site.register(Category)
admin.site.register(Tag)
