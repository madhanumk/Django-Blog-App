from django.db import models
from django.contrib.auth.models import User
from .slugify import unique_slug_generator
from django.dispatch import receiver

# Create your models here.


class Post_Category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='Post Category'
        verbose_name_plural='Post Category'

class Tag(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    title=models.CharField(max_length=100)
    slug = models.SlugField(max_length=255,unique=True, null=True, blank=True)
    keyword=models.CharField(max_length=300,null=True)
    post_content = models.TextField()
    posted_on = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(User,on_delete=models.CASCADE)    
    post_category = models.ForeignKey(Post_Category,on_delete=models.CASCADE,null=True)
    tag = models.ManyToManyField(Tag,blank=True)
    featured_image=models.ImageField(upload_to="featured_image", default='featured_image/default_image/featured_img_for_post.jpg')
    publish=models.BooleanField()

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.title

    def comment_count(self):
        return Comment.objects.filter(post=self.id).count()

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete = models.CASCADE)
    comment_user = models.CharField(max_length = 50)
    comment_content = models.TextField()
    commented_on = models.DateTimeField(auto_now_add=True)
    show=models.BooleanField()

    def __str__(self):
        return self.comment_content

    class Meta:
        ordering = ['-commented_on']


#To Create Slug
@receiver(models.signals.pre_save, sender=Post)
def auto_slug_generator(sender, instance, **kwargs):
    """
    Creates a slug if there is no slug.
    """
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

