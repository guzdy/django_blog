from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Tag, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from .forms import EmailPostForm
from django.core.mail import send_mail
from django.db.models import Count
import markdown
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from .forms import CommentForm


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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # 父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量，
        # paginator 是 Paginator 的一个实例，
        # page_obj 是 Page 的一个实例，
        # is_paginated 是一个布尔变量，用于指示是否已分页。
        # 例如如果规定每页 10 个数据，而本身只有 5 个数据，其实就用不着分页，此时 is_paginated=False
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        # 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据，见下方。
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页导航条的模板变量更新到 context 中，注意 pagination_data 方法返回的也是一个字典。
        context.update(pagination_data)

        # 将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板。
        # 注意此时 context 字典中已有了显示分页导航条所需的数据。
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
            return {}

        # 当前页左边连续的页码号，初始值为空
        left = []

        # 当前页右边连续的页码号，初始值为空
        right = []

        # 标示第 1 页页码后是否需要显示省略号
        left_has_more = False

        # 标示最后一页页码前是否需要显示省略号
        right_has_more = False

        # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        first = False

        # 标示是否需要显示最后一页的页码号。
        # 需要此指示变量的理由和上面相同。
        last = False

        # 获得用户当前请求的页码号, 总页数
        page_number = page.number
        total_pages = paginator.num_pages

        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range = paginator.page_range

        # 如果用户请求的是第一页的数据
        if page_number == 1:
            right = page_range[page_number:page_number + 2]
            if right[-1] < total_pages - 1:
                right_has_more = True

            if right[-1] < total_pages:
                last = True

        # 如果用户请求的是最后一页的数据
        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (
                                                   page_number - 3) > 0 else 0: page_number - 1]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        else:
            right = page_range[page_number:page_number + 2]
            if right[-1] < total_pages - 1:
                right_has_more = True

            if right[-1] < total_pages:
                last = True
            left = page_range[(page_number - 3) if (
                                                   page_number - 3) > 0 else 0: page_number - 1]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data


class TagView(PostListView):
    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs.get('tag_slug'))
        # slug 是 tag 的参数， tag_slug 是 urls 里获得的参数
        return super().get_queryset().filter(tags__in=[self.tag])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'tag': self.tag})

        # 将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板。
        # 注意此时 context 字典中已有了显示分页导航条所需的数据。
        return context


class CategoryView(PostListView):
    def get_queryset(self):
        category = get_object_or_404(
            Category, slug=self.kwargs.get('category_slug'))
        # slug 是 tag 的参数， tag_slug 是 urls 里获得的参数
        return super().get_queryset().filter(category=category)


class ArchivesView(PostListView):
    def get_queryset(self):
        self.year = self.kwargs.get('year')
        self.month = self.kwargs.get('month')
        return super().get_queryset().filter(publish__year=self.year,
                                             publish__month=self.month)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'year': self.year, 'month': self.month})
        return context


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    cd = None  # cleaned data 验证后的数据
    # 如果我们得到一个GET请求，一个空的表单必须显示，
    # 而如果我们得到一个POST请求，则表单需要提交和处理。
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(
                cd['name'], cd['email'], post.title
            )
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(
                post.title, post_url, cd['name'], cd['comments']
            )
            send_mail(subject, message, 'luozhiyang229@163.com', [cd['to']])
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


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')

    post.increase_views()
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        # 'markdown.extensions.toc',
        # extensions 中的 toc 拓展不再是字符串 markdown.extensions.toc
        # ，而是 TocExtension 的实例。TocExtension 在实例化时其 slugify 参数
        # 可以接受一个函数作为参数，这个函数将被用于处理标题的锚点值。
        # Markdown 内置的处理方法不能处理中文标题，所以我们使用了 django.utils.text
        # 中的 slugify 方法，该方法可以很好地处理中文。
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)
    post.toc = md.toc

    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            new_comment.save()
            # 重定向到 post 的详情页
            return redirect(post)
    else:
        comment_form = CommentForm()

    # List  of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids).exclude(id=post.id)
    # 我们使用Count聚合函数来生成一个计算字段same_tags，该字段包含与查询到的所有 标签共享的标签数量。
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by(
        '-same_tags', '-publish')[:4]

    return render(request, 'blog/post/detail.html',
                  {'post': post, 'comments': comments,
                   'new_comment': new_comment, 'comment_form': comment_form,
                   'similar_posts': similar_posts})

