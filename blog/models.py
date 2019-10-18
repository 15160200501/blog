from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import markdown
from django.utils.html import strip_tags
# Create your models here.
class Category(models.Model):
    """
    django要求模型必须继承models.Models类
    Category只需要一个简单的分类名name就可以了
    CharField指定了分类名name的数据类型，CharField是字符型
    CharField的max_length参数指定其最大长度，超过这个长度的分类名就不能被存入数据库
    当然django还为我们提供了多种其他的数据类型，如日期时间类型DateTimeField、整数类型InterField等等
    django内置的全部类型可查看文档
    https://docs.djangoproject.com/en/2.2/ref/models/fields/#field-types
    """
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Tag(models.Model):
    """
    标签Tag也比较简单，和Category一样
    再次强调一定要继承models.Model类
    """
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Post(models.Model):
    """
    文章的数据库表稍微复杂一点，主要涉及的字段更多
    """
    #文章标题
    title = models.CharField('标题',max_length=70)

    #存储比较短的字符串可以使用CharField，但对于文章的正文来说可能会是一大段文本，因此使用TextField来存储大段文本
    body = models.TextField('正文')

    #这两个列分别表示文章的创建时间和最后一次修改时间，存储时间的字段用DataTimeField类型
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('修改时间')

    #文章摘要，可以没有文章摘要，但默认情况下CharField要求我们必须存入数据，否则就会报错
    excerpt = models.CharField('摘要', max_length=200, blank=True)

    #同时你对ForeignKey，ManyToManyField不了解，请看教程中的解释，参考官方文档：
    # https://docs.djangoproject.com/en/2.2/topics/db/models/#relationships
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)

    #因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和Category类似
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.excerpt =strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)

    #自定义get_absolute_url方法
    #记得从django.urls中导入reverse函数
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
