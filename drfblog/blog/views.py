from .models import Blog, Comment
from .forms import EmailPostForm, CommentForm
from django.shortcuts import render
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from .models import Blog
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm
from django.core.mail import send_mail
from taggit.models import Tag


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Blog, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    return render(request,'blog/post/detail.html',{'post': post})


def post_list(request):
    posts = Blog.published.all()
    return render(request,'blog/post/list.html', {'posts': posts})


def post_list(request, tag_slug=None):
    object_list = Blog.published.all()
    tag = None 
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 4)
    page = request.GET.get('page')
    try:
         posts = paginator.page(page)
    except PageNotAnInteger:
 
        posts = paginator.page(1)
    except EmptyPage:

        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/post/list.html',{'page': page,'posts': posts})

def post_share(request, post_id):
    post = get_object_or_404(Blog, id=post_id,status='published')
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post': post,'form': form})





def post_share(request, post_id):
    
    post = get_object_or_404(Blog, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        
        form = EmailPostForm(request.POST)
        if form.is_valid():
            
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                       f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s "
            send_mail(subject, message, 'akshit107.rejoice@gmail.com',
                      [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                     'form': form,
                                                     'sent':sent})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Blog, slug=post,
            status='published',
            publish__year=year,
            publish__month=month,
            publish__day=day)
 
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request,
                'blog/post/detail.html',
                {'post': post,
                'comments': comments,
                'new_comment': new_comment,
                'comment_form': comment_form})