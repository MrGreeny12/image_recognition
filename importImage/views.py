from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from config import settings
from importImage.models import Image
from importImage.scripts.image_recognition import ImageRecognition


class BasicView(TemplateView):
    template_name = 'importImage/main.html'


def file_upload_view(request):

    if request.method == 'POST':
        my_file = request.FILES.get('file')
        Image.objects.create(upload=my_file)
        file_path = settings.MEDIA_URL + 'images/' + my_file
        image = ImageRecognition(file_path)
        height = image.take_metadata()[0]
        width = image.take_metadata()[1]
        colour = image.average_colour()
        count_coins = image.count_circles()
        return JsonResponse({
            'Высота изображения' : height,
            'Ширина изображения' : width,
            'Средний цвет изображения' : colour,
            'Количество монет на изображении' : count_coins,
            'Общая сумма монет на изображении' : 'Вычислить не удалось'
        }
        )
    return JsonResponse(
        {
            'post':'false'
        }
    )