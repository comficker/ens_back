from django.http import HttpResponse
from django.template import loader
from app.models import Asset, Report
from datetime import datetime


def sitemap_style(request):
    template = loader.get_template('./main-sitemap.xsl')
    return HttpResponse(template.render({}, request), content_type='text/xml')


def sitemap_index(request):
    reports = Report.objects.values("created").distinct()
    sm = []
    for item in reports:
        sm.append("https://enshunt.com/{}-sitemap.xml".format(item["created"].strftime('%Y-%m-%d')))
    template = loader.get_template('./sitemap_index.xml')
    return HttpResponse(template.render({
        "sitemaps": sm
    }, request), content_type='text/xml')


def sitemap_detail(request, flag):
    template = loader.get_template('./sitemap.xml')
    date = datetime.strptime(flag, "%Y-%m-%d").date()
    ds = list(map(
        lambda x: {
            "location": "https://enshunt.com/{}-{}.eth".format(x.id, x.name),
            "priority": 0.8,
            "updated": datetime.now(),
            "changefreq": "daily"
        },
        Asset.objects.filter(
            mint_date__day=date.day,
            mint_date__month=date.month,
            mint_date__year=date.year
        )
    ))
    return HttpResponse(template.render({
        "dataset": ds
    }, request), content_type='text/xml')
