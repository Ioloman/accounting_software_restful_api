from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from api_app.models import Detail, Report, ReportLine
from api_app.serializers import DetailSerializer, ReportSerializer, ReportLineSerializer


@api_view(['GET'])
def api_root(request, format=None):
    """Добро пожаловать в API.
    Пока что оно устроено следующим образом.
    Сверху страницы есть навигационная панель для простой навигации в браузере.
    Краткая справка по HTTP методам:
    GET - получить
    POST - создать
    DELETE - удалить
    PUT - изменить полностью
    PATCH - изменить 1 или несколько значений.
    Устройство API на примере рапортов:
    GET /api/reports/ - список рапортов
    POST /api/reports/ - создать рапорт
    DELETE /api/reports/1/ - удалить рапорт
    PUT /api/reports/1/ - изменить рапорт (обязательно указывать все значения кроме первичного ключа и доп. словарей)
    PATCH /api/reports/1/ - изменить рапорт (можно 1 значение).
    СЛЕШ / ПОСЛЕ ССЫЛКИ ОБЯЗАТЕЛЬНО
    url при создании и редактировании не нужен.
    Заголовок Content-Type: application/json
    Тип отправляемых данных - JSON объект.
    В заголовке Allow можно увидеть список разрешенных методов на данном URL (то есть Read-Only или нет)"""
    return Response({
        'Рапорта': reverse('api:report-list', request=request, format=format),
        'Строки рапортов': reverse('api:report-line-list', request=request, format=format),
        'Детали': reverse('api:detail-list', request=request, format=format),
    })


class DetailList(generics.ListAPIView):
    """
    Read-Only. Список деталей.
    """
    queryset = Detail.objects.all()
    serializer_class = DetailSerializer


class DetailDetail(generics.RetrieveAPIView):
    queryset = Detail.objects.all()
    serializer_class = DetailSerializer


class ReportList(generics.ListCreateAPIView):
    """
    Список рапортов. В графе report_lines подробный список строк. Подобные параметры напрямую менять нельзя.
    При создании и изменении они тоже не нужны.
    А работать со строками нужно через /api/report_lines/ используя ключи, тут только смотреть.
    url при создании и редактировании не нужен.
    """
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class ReportDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    url и вложенные массивы и объекты при редактировании не нужны.
    """
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class ReportLineList(generics.ListCreateAPIView):
    queryset = ReportLine.objects.all()
    serializer_class = ReportLineSerializer


class ReportLineDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReportLine.objects.all()
    serializer_class = ReportLineSerializer
