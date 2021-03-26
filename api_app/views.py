from rest_framework import generics
from api_app.models import Detail, Report, ReportLine
from api_app.serializers import DetailSerializer, ReportSerializer, ReportLineSerializer


class DetailList(generics.ListAPIView):
    queryset = Detail.objects.all()
    serializer_class = DetailSerializer


class DetailDetail(generics.RetrieveAPIView):
    queryset = Detail.objects.all()
    serializer_class = DetailSerializer


class ReportList(generics.ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class ReportDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class ReportLineList(generics.ListCreateAPIView):
    queryset = ReportLine.objects.all()
    serializer_class = ReportLineSerializer


class ReportLineDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReportLine.objects.all()
    serializer_class = ReportLineSerializer
