from django.http import HttpResponse
from django.template import loader
from app.models import Asset
from datetime import datetime


def sitemap_style(request):
    template = loader.get_template('./main-sitemap.xsl')
    return HttpResponse(template.render({}, request), content_type='text/xml')


def sitemap_index(request):
    sm = [
        "https://demask.io/asset-sitemap.xml",
    ]
    template = loader.get_template('./sitemap_index.xml')
    return HttpResponse(template.render({
        "sitemaps": sm
    }, request), content_type='text/xml')


def sitemap_detail(request, flag):
    template = loader.get_template('./sitemap.xml')
    if flag == "asset":
        ds = list(map(
            lambda x: {
                "location": "https://enshunt.com/{}".format(x.item_id),
                "priority": 0.8,
                "updated": datetime.now(),
                "changefreq": "daily"
            },
            Asset.objects.all()
        ))
    else:
        ds = []
    return HttpResponse(template.render({
        "dataset": ds
    }, request), content_type='text/xml')
