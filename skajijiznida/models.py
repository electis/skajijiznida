import os
from datetime import datetime
from pytils import translit
from django.db import models
from django.utils.safestring import mark_safe

sections = (('taxi', 'Социальные проекты'), ('othere', 'Профилактические проекты'))
html_path = os.path.join('..', 'public_html')

def get_image_path(self, filename):
    date = self.art_date()
    return os.path.join(date.strftime('%d%m%Y') , translit.translify(filename))


class Article(models.Model):
    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "1 Статьи"
    date = models.DateField(default=datetime.now, verbose_name="Дата события")
    section = models.CharField(max_length=16, default='taxi', choices=sections, verbose_name="Раздел сайта")
    header = models.CharField(max_length=128, default='', verbose_name="Заголовок статьи")
    text = models.TextField(default='', verbose_name="Текст статьи")
    pict = models.ImageField(upload_to=get_image_path, null=True, blank=True, verbose_name="Основная картинка")
    video = models.FileField(upload_to=get_image_path, null=True, blank=True, verbose_name="Видеофайл")
    published = models.BooleanField(default=False, verbose_name="Опубликовано")
    ready = models.TextField(default='', verbose_name="Отрендеренный HTML", blank=True)

    def __str__(self):
        return f'{self.header}'

    def art_date(self):
        return self.date

    def image200_tag(self):
        return mark_safe(f'<img src="/images/{self.pict}" height="200px" />')
    image200_tag.short_description = 'Image200'

    def image50_tag(self):
        return mark_safe(f'<img src="/images/{self.pict}" height="50px" />')
    image50_tag.short_description = 'Image50'


class Image(models.Model):
    class Meta:
        verbose_name = "Изображение статьи"
        verbose_name_plural = "2 Изображения статей"
    article = models.ForeignKey(Article, default=None, null=True, on_delete=models.CASCADE, verbose_name="Статья")
    pict = models.ImageField(upload_to=get_image_path, null=True, verbose_name="Картинка")
    order = models.IntegerField(default=10, verbose_name="Порядок вывода")

    def __str__(self):
        return f'{self.article} - {self.pict.name}'

    def art_date(self):
        return self.article.date

    def image200_tag(self):
        return mark_safe(f'<img src="/images/{self.pict}" height="200px" />')
    image200_tag.short_description = 'Image200'

    def image50_tag(self):
        return mark_safe(f'<img src="/images/{self.pict}" height="50px" />')
    image50_tag.short_description = 'Image50'


class Common(models.Model):
    class Meta:
        verbose_name = "Настройки"
        verbose_name_plural = "Настройки"
    template_start = models.TextField(default='', blank=True, verbose_name="Шаблон статьи основной")
    template_list = models.TextField(default='', blank=True, verbose_name="Шаблон статьи фотоотчёт")
    template_video = models.TextField(default='', blank=True, verbose_name="Шаблон статьи видеофайл")
    template_end = models.TextField(default='', blank=True, verbose_name="Шаблон статьи окончание")
    images = models.CharField(
        max_length=128, default='images', blank=True, verbose_name="Путь к папкам с изображениями")

    def __str__(self):
        return 'Настройки'
