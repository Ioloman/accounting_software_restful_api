import datetime

from django.db.models import QuerySet
from django.shortcuts import redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from api_app.models import Detail, Report, ReportLine, Vedomost, VedomostLine, Workshop, UsingInstruction
from api_app.serializers import DetailSerializer, ReportSerializer, ReportLineSerializer, VedomostSerializer, \
    VedomostLineSerializer, WorkshopSerializer


def redirect_view(request):
    return redirect('api:root')


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
    Также на некоторых (а может и на всех) будет кнопка Filters. Это значит данные можно фильтровать с помощью параметров.
    Например GET /api/report-lines/?report_pk=1 вернет список строк, принадлежащих рапорт с ключем 1.
    Такие параметры отличаются, от данных, которые нужно передать, например, при создании объекта методом POST.
    Они ставятся в конец url. А данные, для создания объекта передаются в теле запроса.
    Но в нормальных библиотеках для запросов это все автоматизировано и париться особо не нужно, просто передавать как разные аргументы.
    url при создании и редактировании не нужен.
    Возможно добавлений любых фильтров из разряда фильтрации, сортировки и поиска по Вашему запросу.
    Заголовок Content-Type: application/json
    Тип отправляемых данных - JSON объект.
    В заголовке Allow можно увидеть список разрешенных методов на данном URL (то есть Read-Only или нет)"""
    return Response({
        'Рапорта': reverse('api:report-list', request=request, format=format),
        'Строки рапортов': reverse('api:report-line-list', request=request, format=format),
        'Ведомости': reverse('api:vedomost-list', request=request, format=format),
        'Строки ведомостей': reverse('api:vedomost-line-list', request=request, format=format),
        'Детали': reverse('api:detail-list', request=request, format=format),
        'Цеха': reverse('api:workshop-list', request=request, format=format),
        'Остатки': reverse('api:leftovers', request=request, format=format),
    })


class DetailList(generics.ListAPIView):
    """
    Read-Only. Список деталей. Создавать через админку.
    Возможен поиск.
    """
    queryset = Detail.objects.all()
    serializer_class = DetailSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['detail_name']


class DetailDetail(generics.RetrieveAPIView):
    """
    Read-Only. Просмотр деталей. Создавать через админку.
    """
    queryset = Detail.objects.all()
    serializer_class = DetailSerializer


class WorkshopList(generics.ListAPIView):
    """
    Read-Only. Список цехов. Создавать через админку.
    Возможен поиск.
    """
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['workshop_name', 'cipher_workshop']
    filterset_fields = ['workshop_name', 'cipher_workshop']


class WorkshopDetail(generics.RetrieveAPIView):
    """
    Read-Only. Просмотр цехов. Создавать через админку.
    """
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer


class ReportList(generics.ListCreateAPIView):
    """
    Список рапортов. В графе report_lines подробный список строк. Подобные параметры напрямую менять нельзя.
    При создании и изменении они тоже не нужны.
    А работать со строками нужно через /api/report_lines/ используя ключи, тут только смотреть.
    url при создании и редактировании не нужен.
    Фильтрация по дате: /api/reports/?ordering=-date  -- в порядке убывания.
    """
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['date']
    ordering = ['-date']


class ReportDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Просмотр и действия с рапортом.
    url и вложенные массивы и объекты при редактировании не нужны.
    """
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class ReportLineList(generics.ListCreateAPIView):
    """
    Список всех строк рапортов.
    Фильтрация по рапорту: /api/report-lines/?report_pk=1
    """
    queryset = ReportLine.objects.all()
    serializer_class = ReportLineSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['report_pk']


class ReportLineDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Просмотр и редактирование строки рапорта.
    """
    queryset = ReportLine.objects.all()
    serializer_class = ReportLineSerializer


class VedomostList(generics.ListCreateAPIView):
    """
    Список ведомостей. В графе vedomost_lines подробный список строк. Подобные параметры напрямую менять нельзя.
    При создании и изменении они тоже не нужны.
    А работать со строками нужно через /api/vedomost_lines/ используя ключи, тут только смотреть.
    url при создании и редактировании не нужен.
    Фильтрация по дате: /api/reports/?ordering=-creation_date  -- в порядке убывания.
    """
    queryset = Vedomost.objects.all()
    serializer_class = VedomostSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['creation_date']
    ordering = ['-creation_date']


class VedomostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Просмотр ведомости.
    url и вложенные массивы и объекты при редактировании не нужны.
    """
    queryset = Vedomost.objects.all()
    serializer_class = VedomostSerializer


class VedomostLineList(generics.ListCreateAPIView):
    """
    Список всех строк ведомостей.
    Фильтрация по ведомости: /api/vedomost-lines/?vedomost_pk=1
    """
    queryset = VedomostLine.objects.all()
    serializer_class = VedomostLineSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['vedomost_pk']


class VedomostLineDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Просмотр и редактирование строки ведомости.
    """
    queryset = VedomostLine.objects.all()
    serializer_class = VedomostLineSerializer


def split_details(details: list[dict], request):
    details = details.copy()
    details_to_add = []
    details_to_remove = []
    for detail in details:
        try:
            instruction = UsingInstruction.objects.get(detail_manufactured_pk__detail_pk=detail['detail_pk'])
            for using_line in instruction.usingline_set.all():
                data = DetailSerializer(instance=using_line.detail_pk, context={'request': request}).data
                data['amount'] = using_line.amount * detail['amount']
                details_to_add.append(data)
            details_to_remove.append(detail)
        except UsingInstruction.DoesNotExist:
            pass
    for detail in details_to_remove:
        details.remove(detail)
    details.extend(details_to_add)
    return details


class Leftovers(APIView):
    """
    Остатки. Необходимы параметры date и workshop_pk, например:
    /api/leftovers/?date=2021-02-20&workshop_pk=2
    """
    def get(self, request, format=None):
        if not request.GET.get('date') or not request.GET.get('workshop_pk'):
            return Response({'error': 'Url params date and workshop_pk are required', 'leftovers': [], 'stuck': []})
        date = datetime.date.fromisoformat(request.GET.get('date'))
        workshop_pk = request.GET.get('workshop_pk')
        # последняя ведомость инвентаризации
        vedomost: Vedomost = Vedomost.objects.filter(
            creation_date__lte=date,
            workshop_pk=workshop_pk
        ).latest()
        # входные партии
        income_lines: QuerySet[ReportLine] = ReportLine.objects.filter(
            workshop_receiver_pk__workshop_pk=workshop_pk,
            report_pk__date__lte=date,
            report_pk__date__gte=vedomost.creation_date
        )
        # выходные партии
        outcome_lines: QuerySet[ReportLine] = ReportLine.objects.filter(
            report_pk__workshop_sender_pk__workshop_pk=workshop_pk,
            report_pk__date__lte=date,
            report_pk__date__gte=vedomost.creation_date
        )
        # словарь для расчета остатков
        details = {}
        # записываем данные инвентаризации
        for vedomost_line in vedomost.vedomostline_set.all():
            if vedomost_line.amount:
                data = DetailSerializer(instance=vedomost_line.detail_pk, context={'request': request}).data
                data['amount'] = vedomost_line.amount
                details[vedomost_line.detail_pk.detail_pk] = data
        # прибавляем входные партии
        for line in income_lines:
            if line.produced:
                if line.detail_pk.detail_pk in details:
                    details[line.detail_pk.detail_pk]['amount'] += line.produced
                else:
                    data = DetailSerializer(instance=line.detail_pk, context={'request': request}).data
                    data['amount'] = line.produced
                    details[line.detail_pk.detail_pk] = data
        # преобразуем выходные партии в удобный формат
        outcome_details = []
        for line in outcome_lines:
            if line.produced:
                data = DetailSerializer(instance=line.detail_pk, context={'request': request}).data
                data['amount'] = line.produced
                outcome_details.append(data)
        # вычитаем выходные
        while outcome_details:
            # отнимаем вышедшие детали
            for detail in outcome_details:
                if details.get(detail['detail_pk']):
                    subtrahend = min(detail['amount'], details.get(detail['detail_pk'])['amount'])
                    details.get(detail['detail_pk'])['amount'] -= subtrahend
                    detail['amount'] -= subtrahend
            # очищаем у которых количество на нуле
            outcome_details = list(filter(lambda d: d['amount'] != 0, outcome_details))
            for key in list(filter(lambda k: details[k]['amount'] == 0, details)):
                del details[key]
            # разбиваем
            new_outcome_details = split_details(outcome_details, request)
            if new_outcome_details == outcome_details:
                break
            else:
                outcome_details = new_outcome_details
        details = list(details.values())
        return Response({
            'leftovers': details,
            'stuck': outcome_details,
            'error': None
        })






