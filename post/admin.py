from django.contrib import admin
from .models import Post_Category, Tag, Post, Comment
from django_summernote.admin import SummernoteModelAdmin
from django_summernote.widgets import SummernoteWidget
from django.db import models

# Register your models here.

@admin.register(Post_Category)
class TagAdminModel(admin.ModelAdmin):
    list_display=['name']

@admin.register(Tag)
class TagAdminModel(admin.ModelAdmin):
    list_display=['name']


@admin.register(Comment)
class CommentAdminModel(admin.ModelAdmin):
    list_display=['comment_user']

#Change as TabularInline if you are not comfortable with stakedinline
class CommentInline(admin.StackedInline):
    model = Comment
    extra=0
    formfield_overrides = {models.TextField: {'widget': SummernoteWidget}}


def make_published(modeladmin, request, queryset):
    queryset.update(publish=True)
make_published.short_description = "Mark selected posts as Published"


def make_unpublished(modeladmin, request, queryset):
    queryset.update(publish=False)
make_unpublished.short_description = "Mark selected posts as Unpublished"



@admin.register(Post)
class PostAdminModel(SummernoteModelAdmin):
    list_display=['title','posted_by','posted_on','publish','comment_count']
    inlines=[CommentInline,]
    list_filter=['post_category','tag','posted_by']
    search_fields= ['title']
    filter_horizontal = ('tag',)
    date_hierarchy = 'posted_on'
    actions = [make_published,make_unpublished]

    def save_model(self, request, obj, form, change):
        if not change:  
            obj.posted_by = request.user
        
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("posted_by", )
        form = super(PostAdminModel, self).get_form(request, obj, **kwargs)
        return form

    def get_queryset(self, request):         
          
        if request.user.is_superuser:
            return Post.objects.all()
        elif request.user.groups.filter(name='Blogger').exists():
            return Post.objects.filter(posted_by=request.user)


          

   