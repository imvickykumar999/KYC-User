from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, LikeDislike, Profile
from .forms import PostForm, CommentForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

@login_required
def profile(request):
    return render(request, 'blog/profile.html', {'user': request.user})

def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts})

def index(request):
    return render(request, 'blog/index.html')

@login_required
def create_post(request):
    if not request.user.profile.is_kyc_user:
        return redirect('profile')
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html', {'form': form})

@login_required
def like_dislike_post(request, pk, is_like):
    post = get_object_or_404(Post, pk=pk)
    like_dislike, created = LikeDislike.objects.update_or_create(
        post=post, user=request.user,
        defaults={'is_like': is_like},
    )
    return redirect('post_detail', pk=post.pk)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    likes_count = post.likes_dislikes.filter(is_like=True).count()
    dislikes_count = post.likes_dislikes.filter(is_like=False).count()
    context = {
        'post': post,
        'likes_count': likes_count,
        'dislikes_count': dislikes_count,
    }
    return render(request, 'blog/post_detail.html', context)
