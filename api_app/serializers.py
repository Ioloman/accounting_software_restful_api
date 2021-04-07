from rest_framework import serializers
from .models import Detail, Report, ReportLine, VedomostLine, Vedomost, Workshop


class DetailSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:detail-detail')

    class Meta:
        model = Detail
        fields = ['url', 'detail_pk', 'detail_name', 'cipher_detail']


class WorkshopSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:workshop-detail')

    class Meta:
        model = Workshop
        fields = ['url', 'workshop_pk', 'workshop_name', 'cipher_workshop']


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

    def update(self, instance: Report, validated_data):
        instance.doc_num = validated_data.get('doc_num', instance.doc_num)
        instance.date = validated_data.get('date', instance.date)
        instance.workshop_sender_pk = validated_data.get('workshop_sender_pk', instance.workshop_sender_pk)
        instance.save()

        new_lines = self.initial_data.get('report_lines', [])
        old_lines = instance.reportline_set.all()
        old_lines = [dict(ReportLineSerializer(instance=line, context={'request': self.context['request']}).data) for line in old_lines]

        to_delete = []
        to_change = []
        to_create = []

        for old_line in old_lines:
            for new_line in new_lines:
                if old_line['report_line_pk'] == new_line['report_line_pk']:
                    break
            else:
                to_delete.append(old_line)
        for delete in to_delete:
            old_lines.remove(delete)

        for new_line in new_lines:
            for old_line in old_lines:
                if old_line['report_line_pk'] == new_line['report_line_pk']:
                    break
            else:
                to_create.append(new_line)
        for create in to_create:
            new_lines.remove(create)

        for new_line in new_lines:
            for old_line in old_lines:
                if old_line['report_line_pk'] == new_line['report_line_pk']:
                    if old_line == new_line:
                        break
            else:
                to_change.append(new_line)

        for delete in to_delete:
            ReportLine.objects.get(report_line_pk=delete['report_line_pk']).delete()

        for create in to_create:
            serialized_line = ReportLineSerializer(data=create)
            if serialized_line.is_valid():
                serialized_line.save()

        for change in to_change:
            line: ReportLine = ReportLine.objects.get(report_line_pk=change['report_line_pk'])
            serialized_line = ReportLineSerializer(line, data=change)
            if serialized_line.is_valid():
                serialized_line.save()

        return instance

    class Meta:
        model = Report
        fields = ['url', 'report_pk', 'doc_num', 'date', 'workshop_sender_pk', 'report_lines']


class VedomostLineSerializer(serializers.ModelSerializer):
    detail = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='api:vedomost-line-detail')

    def get_detail(self, obj):
        data = DetailSerializer(instance=obj.detail_pk, context={'request': self.context['request']}).data
        data.pop('detail_pk')
        return data

    class Meta:
        model = VedomostLine
        fields = ['url', 'vedomost_line_pk', 'vedomost_pk', 'detail_pk', 'amount', 'detail']


class VedomostSerializer(serializers.ModelSerializer):
    vedomost_lines = VedomostLineSerializer(read_only=True, many=True, allow_null=True, source='vedomostline_set', required=False)
    url = serializers.HyperlinkedIdentityField(view_name='api:vedomost-detail')

    def update(self, instance: Vedomost, validated_data):
        instance.doc_num = validated_data.get('doc_num', instance.doc_num)
        instance.creation_date = validated_data.get('creation_date', instance.creation_date)
        instance.workshop_pk = validated_data.get('workshop_pk', instance.workshop_pk)
        instance.save()

        new_lines = self.initial_data.get('vedomost_lines', [])
        old_lines = instance.vedomostline_set.all()
        old_lines = [dict(VedomostLineSerializer(instance=line, context={'request': self.context['request']}).data) for line in old_lines]

        to_delete = []
        to_change = []
        to_create = []

        for old_line in old_lines:
            for new_line in new_lines:
                if old_line['vedomost_line_pk'] == new_line['vedomost_line_pk']:
                    break
            else:
                to_delete.append(old_line)
        for delete in to_delete:
            old_lines.remove(delete)

        for new_line in new_lines:
            for old_line in old_lines:
                if old_line['vedomost_line_pk'] == new_line['vedomost_line_pk']:
                    break
            else:
                to_create.append(new_line)
        for create in to_create:
            new_lines.remove(create)

        for new_line in new_lines:
            for old_line in old_lines:
                if old_line['vedomost_line_pk'] == new_line['vedomost_line_pk']:
                    if old_line == new_line:
                        break
            else:
                to_change.append(new_line)

        for delete in to_delete:
            VedomostLine.objects.get(vedomost_line_pk=delete['vedomost_line_pk']).delete()

        for create in to_create:
            serialized_line = VedomostLineSerializer(data=create)
            if serialized_line.is_valid():
                serialized_line.save()

        for change in to_change:
            line: VedomostLine = VedomostLine.objects.get(vedomost_line_pk=change['vedomost_line_pk'])
            serialized_line = VedomostLineSerializer(line, data=change)
            if serialized_line.is_valid():
                serialized_line.save()

        return instance

    class Meta:
        model = Vedomost
        fields = ['url', 'vedomost_pk', 'doc_num', 'creation_date', 'workshop_pk', 'vedomost_lines']
