# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)
    create_datetime = models.DateTimeField(blank=True, null=True)
    update_datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product'
        ordering = ['id']


class ProductComment(models.Model):
    username = models.CharField(max_length=255, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    comment_datetime = models.DateTimeField(blank=True, null=True)
    create_datetime = models.DateTimeField(blank=True, null=True)
    update_datetime = models.DateTimeField(blank=True, null=True)
    product = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_comment'


class ProductCommentSentiment(models.Model):
    username = models.CharField(max_length=255, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    comment_datetime = models.DateTimeField(blank=True, null=True)
    create_datetime = models.DateTimeField(blank=True, null=True)
    update_datetime = models.DateTimeField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    sentiment = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_comment_sentiment'
