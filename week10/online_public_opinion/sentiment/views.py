from django.shortcuts import render
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Avg

from .models import Product, ProductCommentSentiment as ProductComment


def index(request):
    """
    首页
    """
    comments = ProductComment.objects
    comments_count, sentiment_avg, plus, minus = helper_func(comments)

    context = {
        'comments_count': comments_count,
        'sentiment_avg': sentiment_avg,
        'plus': plus,
        'minus': minus
    }
    return render(request, 'index.html', context=context)


def product_view(request):
    """
    产品页
    """
    product = Product.objects.order_by('create_datetime')
    context = {
        'products': product,
    }
    return render(request, 'products.html', context=context)


def comment_view(request):
    """
    评论页
    """
    args = request.GET
    offset = settings.PAGE_OFFSET

    product_id = int(args.get('product', 0))
    page = int(args.get('page', 1))
    q = args.get('q')
    start_date = args.get('start')
    end_date = args.get('end')

    product = Product.objects.filter(id=product_id).first()
    if not product:
        # 没有查询到产品，就默认数据库中的第一条
        product = Product.objects.first()

    conditions = {'product_id': product.id}
    if q:
        conditions['comment__contains'] = q
    if start_date:
        conditions['comment_datetime__gte'] = start_date
    if end_date:
        conditions['comment_datetime__lte'] = end_date

    comments = ProductComment.objects.filter(**conditions)
    paginator = Paginator(comments.order_by('id'), offset)
    page_obj = paginator.get_page(page)

    comments_count, sentiment_avg, plus, minus = helper_func(comments)

    context = {
        'page_obj': page_obj,
        'product': product,
        'comments_count': comments_count,
        'sentiment_avg': sentiment_avg,
        'plus': plus,
        'minus': minus,
    }
    return render(request, 'comments.html', context=context)


def helper_func(comments):
    comments_count = comments.count()
    sentiment_avg = comments.aggregate(Avg('sentiment'))['sentiment__avg']
    sentiment_avg = '{:.2f}'.format(sentiment_avg or 0)
    plus = comments.values('sentiment').filter(sentiment__gte=0.5).count()
    minus = comments.values('sentiment').filter(sentiment__lt=0.5).count()
    return comments_count, sentiment_avg, plus, minus

