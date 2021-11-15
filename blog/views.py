from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse

def home(request):

    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):

    template_name = 'blog/home.html'
    model = Post
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10

class PostDetailView(DetailView):

    #<app>/<model>_<viewtype>.html default template route
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.kwargs['pk'])
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    # <app>/<model>_<viewtype>.html viewtype = form
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class CommentCreateView(LoginRequiredMixin, CreateView):
    # <app>/<model>_<viewtype>.html viewtype = form
    model = Comment
    fields = ['content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.filter(id=self.kwargs['pk']).first()3
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.filter(id=self.kwargs['pk'])
        return context

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    # <app>/<model>_<viewtype>.html viewtype = form
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class CommentDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):

    model = Comment

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False

    def get_success_url(self):
        return reverse('post-detail', args=[self.kwargs['post_pk']])

class CommentUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    # <app>/<model>_<viewtype>.html viewtype = form
    model = Comment
    fields = ['content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):

    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class UserPostListView(ListView):

    template_name = 'blog/user_posts.html'
    model = Post
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

def about(request):
    return render(request, 'blog/about.html', {'title': 'About page'})

