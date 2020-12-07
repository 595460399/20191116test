from django.conf.urls import url

from . import views

urlpatterns = [
    # 结算订单
    url(r'^orders/settlement/$', views.OrderSettlementView.as_view(), name='settlement'),
    # 提交订单
    url(r'^orders/commit/$', views.OrderCommitView.as_view()),
    # 提交订单成功
    url(r'^orders/success/$', views.OrderSuccessView.as_view()),
    # 评价商品
    url(r'^orders/comment/$', views.OrderCommentView.as_view()),
    #展示评价信息
    url(r'^comments/(?P<sku_id>\d+)/$', views.GoodsCommentView.as_view()),
]
