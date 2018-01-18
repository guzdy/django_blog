from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, unique=True)

    # Category.objects.all() 显示数据人性化
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=70)
    # slug: 这个字段将会在URLs中使用。slug就是一个短标签，
    # 该标签只包含字母，数字，下划线或连接线。
    # 我们将通过使用slug字段给我们的blog帖子构建漂亮的，友好的URLs。
    # 我们给该字段添加了unique_for_date参数，
    # 这样我们就可以使用日期和帖子的slug来为所有帖子构建URLs。
    # 在相同的日期中Django会阻止多篇帖子拥有相同的slug。
    slug = models.SlugField(max_length=250, unique=True)
    # related_name属性指定了从User到Post的反向关系名
    author = models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    # 因为我们在这儿使用了auto_now_add，当一个对象被创建的时候这个字段会自动保存当前日期。
    created = models.DateTimeField(auto_now_add=True)
    # 更新保存一个对象的时候这个字段将会自动更新到当前日期。
    updated = models.DateTimeField(auto_now=True)
    # 我们使用了一个choices参数，这样这个字段的值只能是给予的选择参数中的某一个值。
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = models.Manager()  # the default manager，一定要设置，不然 PublishedManager 成为默认 manager
    published = PublishedManager()  # custom manager ; Post.published.filter(title__startswith='Who')

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    views = models.PositiveIntegerField(default=0)

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    class Meta:
        ordering = ('-publish', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created', )

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)
