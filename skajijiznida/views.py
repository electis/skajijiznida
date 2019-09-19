import os
from django.views.generic import View
from django.shortcuts import render, redirect
from skajijiznida import models


class MainView(View):

    def get(self, request):
        host = request.get_host()
        path_list = [p for p in request.path.split('/') if p]
        print(host, path_list, request.META.get('HTTP_USER_AGENT'), request.META.get('REMOTE_ADDR'), sep=' ~ ')
        context = {}
        context['new'] = models.Article.objects.filter(published=False).order_by('-date')
        context['published'] = models.Article.objects.filter(published=True).order_by('-date')
        return render(request, 'index.html', context)

    def post(self, request):
        common = models.Common.objects.first()
        article_list = models.Article.objects.all().order_by('-date')
        files = {}
        for value, name in models.sections:
            files[value] = open(os.path.join(models.html_path, f'{value}_render.html'), 'w+', encoding='utf8')
        for article in article_list:
            header = article.header
            text = article.text.replace('\r', '<br>')
            date = article.date.strftime('%d%m%Y')
            date_formated = article.date.strftime('%d/%m/%Y')
            pict_main = article.pict
            html = common.template_start.format(
                header=header, date_formated=date_formated, date=date, pict_main=pict_main.url, text=text)
            for pict in article.image_set.all():
                html += common.template_list.format(pict=pict.pict.url, date=date, header=header)
            if article.video:
                html += common.template_video.format(pict=article.video.url, date=date)
            html += common.template_end
            article.ready = html
            article.published = True
            article.save()
            print(html, file=files[article.section])
        for file in files.values():
            file.close()
        return redirect('/')

