from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from cryptoapp.views import NumberDataViewSet , CustomAuthToken, NumberDataBySiteAndPairAPIView, TradingPairListView

router = DefaultRouter()
router.register(r'numberdata', NumberDataViewSet)

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
    path('dashboardprice2/', dashboard_Price_view, name='dashboardprice2'),
    path('dashboardprice2/<int:item_id>', dashboard_price2_detail, name='dashboard_price2_detail'),
    path('run_custom_command/', run_custom_command, name='run_custom_command'),
    path('run_custom_command2/', run_custom_command_cena, name='run_custom_command2'),
    path('upload_trade_pairs', upload_trade_pairs, name='create_trade_pair'),
    path('upload_trade_pairs_rsi', upload_trade_pairs_rsi, name='create_trade_pair_rsi'),
    path('', auth_views.LoginView.as_view( template_name='Login/login.html'), name='login'),
    path('api/', include(router.urls)),
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('api-token-delete/', TokenDelete.as_view(), name='token_delete'),
    path('api/numberdata/<str:site>/<str:pair>/', NumberDataBySiteAndPairAPIView.as_view(), name='numberdata-by-site-and-pair'),
    path('logout/', auth_views.LogoutView.as_view(template_name='Logout/logout.html'), name='logout'),


    path('update-trade-pair/<int:trade_pair_id>/', update_trade_pair, name='update_trade_pair'),
    path('delete-trade-pair/<int:trade_pair_id>/', delete_trade_pair, name='delete_trade_pair'),

    path('delete-trade-pair-off/<str:user>/<int:trade_pair_id>/', Off_trade_pair_rsi, name='delete_trade_pair_off'),
    path('update-trade-pair-off/<str:user>/<int:trade_pair_id>/', up_trade_pair_rsi, name='update_trade_pair_off'),

    path('update-trade-pair_rsi/<str:user>/<int:trade_pair_id>/', update_trade_pair_rsi, name='update_trade_pair_rsi'),
    path('delete-trade-pair_rsi/<str:user>/<int:trade_pair_id>/', delete_trade_pair_rsi, name='delete_trade_pair_rsi'),

    path('update-trade-utm/<str:user>', up_trade_sort, name='update-trade-utm'),

    path('trading-pairs/', TradingPairListView.as_view(), name='trading_pair_list'),
    path('trading-pairs-rsi/', TradingPairRsiListView.as_view(), name='trading_pair_list_rsi'),

    path('setting-data/', SettingData.as_view(), name='setting_data'),


    path('off-trade-pairs/', OffTradePairRsiListView.as_view(), name='off-trade-pair-list'),
    path('off-trade-pairs2/', OffTradePairRsiListView2.as_view(), name='off-trade-pair-list2'),
    


    path('trade-pairs/', trade_pair_list, name='trade_pair_list'),
    path('trade-pairs-rsi/<str:user>', trade_pair_list_rsi, name='trade_pair_list_rsi'),
]