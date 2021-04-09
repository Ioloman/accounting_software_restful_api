import datetime
import math
import random
import string

from django.db.models import QuerySet, When, Case, IntegerField
from django.shortcuts import redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from api_app.models import Detail, Report, ReportLine, Vedomost, VedomostLine, Workshop, UsingInstruction, \
    ProductionProgramByMonth
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
        'Сводный учет': reverse('api:accounting', request=request, format=format),
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
    Возможен поиск, фильтрация по названию, шифру.
    А также по списку первичных ключей, например:
    /api/workshops/?workshop_pks=1,2,5,15
    Но результаты неотсортированы!
    """
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['workshop_name', 'cipher_workshop']
    filterset_fields = ['workshop_name', 'cipher_workshop']

    def filter_queryset(self, queryset: QuerySet[Workshop]):
        if self.request.query_params.get('workshop_pks'):
            workshop_pks = self.request.query_params.get('workshop_pks').split(',')
            return queryset.filter(workshop_pk__in=map(int, workshop_pks))
        else:
            return super().filter_queryset(queryset)


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


def split_details(details, request):
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
        try:
            # последняя ведомость инвентаризации
            vedomost: Vedomost = Vedomost.objects.filter(
                creation_date__lte=date,
                workshop_pk=workshop_pk
            ).latest()
        except Vedomost.DoesNotExist:
            return Response({'error': f'No vedomosts were found before {date}', 'leftovers': [], 'stuck': []})
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
        for detail in details:
            detail['amount'] = 0 if detail['amount'] < 0 else detail['amount']
        return Response({
            'leftovers': details,
            'stuck': outcome_details,
            'error': None
        })


class Accounting(APIView):
    """
    Сводный учет. Если deviation > 0, то это переработка.
    Необходим параметр workshop_pk, start_date или end_date опциональные например:
    /api/accounting/?start_date=2021-03-15&workshop_pk=2
    /api/accounting/?workshop_pk=2
    /api/accounting/?end_date=2021-02-22&workshop_pk=2
    /api/accounting/?start_date=2021-01-15&workshop_pk=2&end_date=2021-02-22
    """
    def get(self, request, format=None):
        if not request.GET.get('workshop_pk'):
            return Response({
                'error': 'Url param workshop_pk is required',
                'accounting': []}
            )

        if request.GET.get('start_date'):
            start_date = datetime.date.fromisoformat(request.GET.get('start_date'))
        else:
            start_date = datetime.date.min
        if request.GET.get('end_date'):
            end_date = datetime.date.fromisoformat(request.GET.get('end_date'))
        else:
            end_date = datetime.date.max
        if (end_date - start_date).days + 1 <= 0:
            return Response({
                'error': 'Dates are invalid',
                'accounting': []}
            )
        workshop_pk = request.GET.get('workshop_pk')

        report_lines: QuerySet[ReportLine] = ReportLine.objects.filter(
            report_pk__workshop_sender_pk=workshop_pk,
            report_pk__date__lte=end_date, report_pk__date__gte=start_date
        ).order_by('report_pk__date')
        programs: QuerySet[ProductionProgramByMonth] = ProductionProgramByMonth.objects.filter(
            workshop_pk=workshop_pk, start_date__lte=end_date, end_date__gte=start_date
        ).order_by('start_date')

        details = {}
        for line in report_lines:
            if line.produced:
                if line.detail_pk.detail_pk in details:
                    details[line.detail_pk.detail_pk]['actual_amount'] += line.produced
                else:
                    data = DetailSerializer(instance=line.detail_pk, context={'request': request}).data
                    data['actual_amount'] = line.produced
                    data['planned_amount'] = 0
                    details[line.detail_pk.detail_pk] = data

        for program in programs:
            left_border = max(start_date, program.start_date)
            right_border = min(end_date, program.end_date)
            coefficient = ((right_border - left_border).days + 1) / ((program.end_date - program.start_date).days + 1)
            for line in program.programline_set.all():
                if line.amount:
                    if line.detail_pk.detail_pk in details:
                        details[line.detail_pk.detail_pk]['planned_amount'] += round(line.amount * coefficient)
                    else:
                        data = DetailSerializer(instance=line.detail_pk, context={'request': request}).data
                        data['planned_amount'] = round(line.amount * coefficient)
                        data['actual_amount'] = 0
                        details[line.detail_pk.detail_pk] = data

        details = list(details.values())
        for detail in details:
            detail['deviation'] = detail['actual_amount'] - detail['planned_amount']

        return Response({
            'error': None,
            'accounting': details}
        )


class CreateVedomost(APIView):
    def get(self, request, format=None):
        date = datetime.date.fromisoformat(request.GET.get('date'))
        child_amount = request.GET.get('child_amount')
        teen_amount = request.GET.get('teen_amount')
        adult_amount = request.GET.get('adult_amount')
        workshop_pk = request.GET.get('workshop_pk')
        vedomost = Vedomost.objects.create(doc_num=random.randint(1000, 10000), creation_date=date, workshop_pk=Workshop.objects.get(workshop_pk=workshop_pk))
        
        if child_amount:
            for line in UsingInstruction.objects.get(detail_manufactured_pk__detail_name='Велосипед детский').usingline_set.all():
                VedomostLine.objects.create(vedomost_pk=vedomost, amount=child_amount * line.amount, detail_pk=line.detail_pk)
                
        if teen_amount:
            for line in UsingInstruction.objects.get(detail_manufactured_pk__detail_name='Велосипед подростковый').usingline_set.all():
                VedomostLine.objects.create(vedomost_pk=vedomost, amount=teen_amount * line.amount, detail_pk=line.detail_pk)
                
        if adult_amount:
            for line in UsingInstruction.objects.get(detail_manufactured_pk__detail_name='Велосипед взрослый').usingline_set.all():
                VedomostLine.objects.create(vedomost_pk=vedomost, amount=adult_amount * line.amount, detail_pk=line.detail_pk)

        return Response({'status': 'success'})


class BigDataFill(APIView):
    """
    Шаблоны:
    Детали - ?type=details&amount=1000&name_length=9
    Доки - ?type=reports&start_date=2021-02-01&end_date=2021-04-20&interval=2&workshop_pk=2
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        type_ = request.GET.get('type', 'reports')
        if type_ == 'reports' or type_ == 'vedomosts':
            start_date = datetime.date.fromisoformat(request.GET.get('start_date'))
            end_date = datetime.date.fromisoformat(request.GET.get('end_date'))
            interval = int(request.GET.get('interval', 1))
            workshop_pk = int(request.GET.get('workshop_pk'))
            lines_from = int(request.GET.get('lines_from', 5))
            lines_to = int(request.GET.get('lines_to', 5))
            if type_ == 'reports':
                objects = []
                for num, date in enumerate((start_date + datetime.timedelta(i) for i in range(0, (end_date - start_date).days + 1, interval))):
                    objects.append(Report(doc_num=num + 1, date=date, workshop_sender_pk_id=workshop_pk))
                    if len(objects) > 50:
                        Report.objects.bulk_create(objects)
                        objects.clear()
                else:
                    Report.objects.bulk_create(objects)
                    objects.clear()

                detail = Detail.objects.all()[0]
                for report in Report.objects.all():
                    objects.extend([
                        ReportLine(report_pk=report, detail_pk=detail, workshop_receiver_pk_id=workshop_pk, produced=5)
                        for _ in range(random.randint(lines_from, lines_to))
                    ])
                    if len(objects) > 50:
                        ReportLine.objects.bulk_create(objects)
                        objects.clear()
                else:
                    ReportLine.objects.bulk_create(objects)
                    objects.clear()
            elif type_ == 'vedomosts':
                objects = []
                for num, date in enumerate((start_date + datetime.timedelta(i) for i in range(0, (end_date - start_date).days + 1, interval))):
                    objects.append(Vedomost(doc_num=num + 1, creation_date=date, workshop_pk_id=workshop_pk))
                    if len(objects) > 50:
                        Vedomost.objects.bulk_create(objects)
                        objects.clear()
                else:
                    Vedomost.objects.bulk_create(objects)
                    objects.clear()

                detail = Detail.objects.all()[0]
                for vedomost in Vedomost.objects.all():
                    objects.extend([
                        VedomostLine(vedomost_pk=vedomost, detail_pk=detail, amount=5)
                        for _ in range(random.randint(lines_from, lines_to))
                    ])
                    if len(objects) > 50:
                        VedomostLine.objects.bulk_create(objects)
                        objects.clear()
                else:
                    VedomostLine.objects.bulk_create(objects)
                    objects.clear()
        elif type_ == 'details':
            amount = int(request.GET.get('amount', 100))
            name_length = int(request.GET.get('name_length', 10))
            details = []
            for i in range(amount):
                details.append(Detail(
                    detail_name=''.join(random.choices(string.ascii_letters, k=name_length)),
                    cipher_detail=''.join(random.choices(string.digits, k=name_length))
                ))
                if len(details) > 50:
                    Detail.objects.bulk_create(details)
                    details.clear()
            else:
                Detail.objects.bulk_create(details)
                details.clear()
        elif type_ == 'clear_all':
            Report.objects.all().delete()
            Vedomost.objects.all().delete()
            Detail.objects.all().delete()
        elif type_ == 'clear_details':
            Detail.objects.all().delete()
        elif type_ == 'clear_reports':
            Report.objects.all().delete()
        elif type_ == 'clear_vedomosts':
            Vedomost.objects.all().delete()
        return Response({'status': 'success'})

                
        
                
            
            








