from django.http.response import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from django.urls.base import reverse
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView # to see details of every post
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin # since we cant use login required decorator on classes
from django.http import HttpResponseRedirect
from .models import Post
# http response import removed
# enter dummy lists and dictionaries to simulate a continuously changing template

def LikeView(request,pk):
    post=get_object_or_404(Post,id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post-detail',args=[str(pk)]))

def home_page(request):
    context={
        'posts': Post.objects.all()
    }
    return render(request,'blog/home.html',context)
class PostListView(ListView):
    model=Post
    template_name="blog/home.html"  # <appname>/<model>_<viewtype>.html
    context_object_name= 'posts'# to help recognize name of variable as posts
    ordering=['-date'] # to ensure newest posts come on top. Remove minus sign for reverse.
    paginate_by=5
class UserPostListView(ListView):
    model=Post
    template_name="blog/user_posts.html"  # <appname>/<model>_<viewtype>.html
    context_object_name= 'posts'# to help recognize name of variable as posts
    ordering=['-date'] # to ensure newest posts come on top. Remove minus sign for reverse.
    paginate_by=5

    def get_queryset(self):
        user=get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date')

class PostDetailView(DetailView):
     model=Post
     template_name="blog/post_detail.html"
     def get_context_data(self,*args, **kwargs):
         context=super(PostDetailView,self).get_context_data(**kwargs)
         stuff=get_object_or_404(Post,id=self.kwargs['pk'])
         total_likes=stuff.total_likes()#calls function in models.py
         context["total_likes"]=total_likes
         return context

class PostCreateView(LoginRequiredMixin,CreateView):
     model=Post
     fields=['title','content']
     template_name="blog/post_form.html"# here instead of normal syntax they expect model name as we will also create update form

     # since we need author for every post(without that we get error) we override the form
     def form_valid(self,form):
         form.instance.author=self.request.user
         return super().form_valid(form)
# order of arguments is important here
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
     model=Post
     fields=['title','content']
     template_name="blog/post_form.html"# here instead of normal syntax they expect model name as we will also create update form

     # since we need author for every post(without that we get error) we override the form
     def form_valid(self,form):
         form.instance.author=self.request.user
         return super().form_valid(form)
     def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
         return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
     model=Post
     template_name="blog/post_confirm_delete.html"
     success_url='/'
     def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
         return True
        return False

def about_page(request):
    return render(request,'blog/about.html',{'title': 'Very cool blog'})
