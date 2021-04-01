from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from importImage.models import Image


class BasicView(TemplateView):
    template_name = 'importImage/main.html'


def file_upload_view(request):
    # print(request.FILES)
    if request.method == 'POST':
        my_file = request.FILES.get('file')
        Image.objects.create(upload=my_file)
        return HttpResponse('')
    return JsonResponse(
        {
            'post':'false'
        }
    )