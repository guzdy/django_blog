from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail


class PostListView(ListView):
    # 使用一个特定的查询集（QuerySet）代替取回所有的对象。
    # 代替定义一个queryset属性，我们可以指定model = Post
    # 然后Django将会构建Post.objects.all() 查询集（QuerySet）给我们。
    queryset = Post.published.all()
    # 使用环境变量posts给查询结果。
    # 如果我们不指定任意的context_object_name默认的变量将会是object_list。
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    cd = None # cleaned data 验证后的数据
    # 。如果我们得到一个GET请求，一个空的表单必须显示，
    # 而如果我们得到一个POST请求，则表单需要提交和处理。
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url =request.build_absolute_url(
                post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(
                cd['name'], cd['email'], post.title
            )
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(
                post.title, post.url, cd['name'], cd['comments']
            )
            send_mail(subject, message, 'admin@guzdy.com', [cd['to']])
            sent = True

    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html',
                  {'post': post, 'form': form, 'sent': sent, 'cd': cd})

"""
def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'blog/post/list.html',
                  {'page': page, 'posts': posts})
"""

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year, publish__month=month,
                             publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})





