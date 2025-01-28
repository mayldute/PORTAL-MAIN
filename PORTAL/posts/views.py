from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import *
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .tasks import notify_about_new_post
from django.core.cache import cache

class PostsList(ListView):
    model = Post
    ordering = ['-create_time']
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()
    
    def get_object(self, *args, **kwargs):
      obj = cache.get(f'post-{self.kwargs["pk"]}', None) 

      if not obj:
         obj = super().get_object(queryset=self.queryset)
         cache.set(f'post-{self.kwargs["pk"]}', obj)

      return obj
    
class PostSearch(ListView):
    model = Post
    ordering = ['-create_time']
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(data=self.request.GET, queryset=queryset)
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class CreatePost(LoginRequiredMixin, CreateView, PermissionRequiredMixin):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    
    def form_valid(self, form):
        post = form.save(commit=False)
        user = self.request.user
        author = Author.objects.filter(user=user).first()
        
        if not author:
            author = Author.objects.create(user=user)

        post.author = author
        
        if 'news' in self.request.path:
            post.type = 'NW'
        elif 'articles' in self.request.path:
            post.type = 'AR'
            
        post.save()

        category = self.request.POST.getlist('category')
        post.category.set(category)
        
        notify_about_new_post.delay(post.id, category)

        return super().form_valid(form)
    
class UpdatePost(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    permission_required = ('news.change_p`ost')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    
    def form_valid(self, form):
        post = form.save(commit=False)
        category_updated = False
        current_category = list(post.category.all())
        new_category = form.cleaned_data.get('category')

        if set(current_category) != set(new_category):
            category_updated = True
                
        if category_updated:
            post.category.set(new_category)

        post.save()
        return super().form_valid(form)
    
class DeletePost(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts')
    
