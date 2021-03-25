# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from datetime import date

from django.db import models


class Detail(models.Model):
    detail_pk = models.AutoField(primary_key=True)
    detail_name = models.CharField(max_length=100)
    cipher_detail = models.CharField(max_length=20)

    class Meta:
        db_table = 'detail'


class InterWorkshopRoutes(models.Model):
    routes_pk = models.AutoField(primary_key=True)
    detail_pk = models.ForeignKey(Detail, models.DO_NOTHING, db_column='detail_pk', blank=True, null=True)

    class Meta:
        db_table = 'inter_workshop_routes'


class LineOfRoute(models.Model):
    string_route_pk = models.AutoField(primary_key=True)
    workshop_sender_pk = models.ForeignKey('Workshop', models.DO_NOTHING, db_column='workshop_sender_pk', blank=True, null=True, related_name='line_sender')
    workshop_receiver_pk = models.ForeignKey('Workshop', models.DO_NOTHING, db_column='workshop_receiver_pk', blank=True, null=True, related_name='line_receiver')
    detail_pk = models.ForeignKey(Detail, models.DO_NOTHING, db_column='detail_pk', blank=True, null=True)
    details_amount = models.IntegerField()
    routes_pk = models.ForeignKey(InterWorkshopRoutes, models.DO_NOTHING, db_column='routes_pk', blank=True, null=True)

    class Meta:
        db_table = 'line_of_route'


class ProductionProgramByMonth(models.Model):
    production_program_pk = models.AutoField(primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField()
    creation_date = models.DateField()
    workshop_pk = models.ForeignKey('Workshop', models.DO_NOTHING, db_column='workshop_pk')

    class Meta:
        db_table = 'production_program_by_month'
        unique_together = (('production_program_pk', 'workshop_pk'),)


class ProductionProgramForTheQuarterByMonth(models.Model):
    production_program_quarter_pk = models.AutoField(primary_key=True)
    quarter_number = models.IntegerField()

    class Meta:
        db_table = 'production_program_for_the_quarter_by_month'


class ProductionProgramForTheQuarterByMonthLine(models.Model):
    line_pk = models.AutoField(primary_key=True)
    detail_pk = models.ForeignKey(Detail, models.DO_NOTHING, db_column='detail_pk')
    production_program_quarter_pk = models.ForeignKey(ProductionProgramForTheQuarterByMonth, models.DO_NOTHING, db_column='production_program_quarter_pk')
    amount = models.IntegerField(blank=True, null=True)
    month_number = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'production_program_for_the_quarter_by_month_line'
        unique_together = (('line_pk', 'detail_pk', 'production_program_quarter_pk'),)


class ProgramLine(models.Model):
    program_line_pk = models.AutoField(primary_key=True)
    amount = models.IntegerField()
    production_program_pk = models.ForeignKey(ProductionProgramByMonth, models.DO_NOTHING, db_column='production_program_pk')
    detail_pk = models.ForeignKey(Detail, models.DO_NOTHING, db_column='detail_pk')

    class Meta:
        db_table = 'program_line'
        unique_together = (('program_line_pk', 'production_program_pk', 'detail_pk'),)


class Report(models.Model):
    report_pk = models.AutoField(primary_key=True)
    # doc_num = models.CharField(max_length=20)
    doc_num = models.IntegerField()
    date = models.DateField(default=date.today)
    workshop_sender_pk = models.ForeignKey('Workshop', models.DO_NOTHING, db_column='workshop_sender_pk', blank=True, null=True, related_name='report_sender')
    workshop_receiver_pk = models.ForeignKey('Workshop', models.DO_NOTHING, db_column='workshop_receiver_pk', blank=True, null=True, related_name='report_receiver')

    class Meta:
        db_table = 'report'


class ReportLine(models.Model):
    report_line_pk = models.AutoField(primary_key=True)
    report_pk = models.ForeignKey(Report, models.DO_NOTHING, db_column='report_pk', blank=True, null=True)
    detail_pk = models.ForeignKey(Detail, models.DO_NOTHING, db_column='detail_pk', blank=True, null=True)
    produced = models.IntegerField(default=0)

    class Meta:
        db_table = 'report_line'


class UsingInstruction(models.Model):
    using_pk = models.AutoField(primary_key=True)
    detail_manufactured_pk = models.OneToOneField(Detail, models.DO_NOTHING, db_column='detail_manufactured_pk')

    class Meta:
        db_table = 'using_instruction'


class UsingLine(models.Model):
    using_line_pk = models.AutoField(primary_key=True)
    amount = models.IntegerField()
    detail_pk = models.ForeignKey(Detail, models.DO_NOTHING, db_column='detail_pk', blank=True, null=True)
    using_pk = models.ForeignKey(UsingInstruction, models.DO_NOTHING, db_column='using_pk', blank=True, null=True)

    class Meta:
        db_table = 'using_line'


class Vedomost(models.Model):
    vedomost_pk = models.AutoField(primary_key=True)
    doc_num = models.IntegerField()
    creation_date = models.DateField(blank=True, null=True, default=date.today)
    workshop_pk = models.ForeignKey('Workshop', models.DO_NOTHING, db_column='workshop_pk', blank=True, null=True)

    class Meta:
        db_table = 'vedomost'


class VedomostLine(models.Model):
    vedomost_line_pk = models.AutoField(primary_key=True)
    vedomost_pk = models.ForeignKey(Vedomost, models.DO_NOTHING, db_column='vedomost_pk', blank=True, null=True)
    amount = models.IntegerField(default=0)
    detail_pk = models.ForeignKey(Detail, models.DO_NOTHING, db_column='detail_pk', blank=True, null=True)

    class Meta:
        db_table = 'vedomost_line'


class Workshop(models.Model):
    workshop_pk = models.AutoField(primary_key=True)
    workshop_name = models.CharField(max_length=100)
    cipher_workshop = models.CharField(max_length=20)

    class Meta:
        db_table = 'workshop'
