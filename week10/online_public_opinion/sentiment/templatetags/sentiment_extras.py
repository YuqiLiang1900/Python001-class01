from django import template
from django.conf import settings

register = template.Library()


@register.filter
def compute_no(value, page):
    """计算表格序号"""
    offset = settings.PAGE_OFFSET
    return value + ((page - 1) * offset)


@register.filter
def format_sentiment(value):
    """解决情感打分太低，使用科学计数法的问题"""
    return f'{value: .4f}'


