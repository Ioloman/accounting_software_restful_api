from rest_framework import serializers
from .models import Detail, Report, ReportLine


class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detail
        fields = '__all__'


class ReportLineSerializer(serializers.ModelSerializer):
    detail = serializers.SerializerMethodField()

    def get_detail(self, obj):
        data = DetailSerializer(instance=obj.detail_pk).data
        data.pop('detail_pk')
        return data

    class Meta:
        model = ReportLine
        fields = ['report_line_pk', 'report_pk', 'detail_pk', 'produced', 'detail', 'workshop_receiver_pk']


class ReportSerializer(serializers.ModelSerializer):
    report_lines = ReportLineSerializer(read_only=True, many=True, allow_null=True, source='reportline_set', required=False)

    class Meta:
        model = Report
        fields = ['report_pk', 'doc_num', 'date', 'workshop_sender_pk', 'report_lines']
