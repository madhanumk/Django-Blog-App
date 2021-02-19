from django.shortcuts import render
from django.views import generic
from .models import Post, Post_Category, Tag
from django.views.generic import TemplateView


  
class HomeView(generic.ListView): 
    model = Post 
    context_object_name = 'posts'
    template_name="home.html"
    paginate_by = 6


class CategoryList(generic.ListView): 
    model = Post_Category
    context_object_name = 'categories'
    template_name="post/categories.html"


class CategoryView(generic.ListView): 
    context_object_name = 'posts'
    template_name="post/post_category_list.html"
    paginate_by = 10

    def get_queryset(self):  
        queryset=Post.objects.filter(post_category__name__iexact=self.kwargs['category'],publish=True)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryView, self).get_context_data(*args, **kwargs)
        context['title'] = self.kwargs['category']
        return context


class TagView(generic.ListView): 
    context_object_name = 'posts'
    template_name="post/post_tag_filter_list.html"
    paginate_by = 10

    def get_queryset(self):  
        queryset=Post.objects.filter(tag__name__iexact=self.kwargs['tag'],publish=True)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(TagView, self).get_context_data(*args, **kwargs)
        context['title'] = self.kwargs['tag']
        return context


class BlogView(generic.ListView): 
    context_object_name = 'post'
    template_name="post/blog.html"


    def get(self, request, *args, **kwargs):

        self.object = Post.objects.get(slug=self.kwargs['slug'])
        return super().get(request, *args, **kwargs)

        
    def get_queryset(self):
        return self.object

    def get_context_data(self, *args, **kwargs):
        context = super(BlogView, self).get_context_data(*args, **kwargs)
        context['categories'] = Post_Category.objects.all()
        context['related_posts']= Post.objects.filter(post_category=self.object.post_category,publish=True).exclude(slug=self.kwargs['slug'])
        return context



def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response