from rest_framework import serializers
from .models import Detail, Report, ReportLine


class DetailSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:detail-detail')

    class Meta:
        model = Detail
        fields = ['url', 'detail_pk', 'detail_name', 'cipher_detail']


class ReportLineSerializer(serializers.ModelSerializer):
    detail = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='api:report-line-detail')

    def get_detail(self, obj):
        data = DetailSerializer(instance=obj.detail_pk, context={'request': self.context['request']}).data
        data.pop('detail_pk')
        return data

    class Meta:
        model = ReportLine
        fields = ['url', 'report_line_pk', 'report_pk', 'detail_pk', 'produced', 'detail', 'workshop_receiver_pk']


class ReportSerializer(serializers.ModelSerializer):
    report_lines = ReportLineSerializer(read_only=True, many=True, allow_null=True, source='reportline_set', required=False)
    url = serializers.HyperlinkedIdentityField(view_name='api:report-detail')

    class Meta:
        model = Report
        fields = ['url', 'report_pk', 'doc_num', 'date', 'workshop_sender_pk', 'report_lines']
