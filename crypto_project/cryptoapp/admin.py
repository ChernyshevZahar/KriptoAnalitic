from django.contrib import admin
from .models import *

class NumberDataAdmin(admin.ModelAdmin):
    list_display = ('Site', 'pair', 'pair1', 'pair2', 'priсe', 'askSize', 'askPrice', 'bid', 'bidSize', )

    class Field1Filter(admin.SimpleListFilter):
        title = 'Site Filter'
        parameter_name = 'Site'  # Имя параметра запроса, используемое в URL

        def lookups(self, request, model_admin):
            unique_values = NumberData.objects.values_list('Site', flat=True).distinct()
            return [(value, value) for value in unique_values]

        def queryset(self, request, queryset):
            if self.value() is not None:
                return queryset.filter(Site=self.value())
            

    class Field1FilterPair(admin.SimpleListFilter):
        title = 'pair1 Filter'
        parameter_name = 'pair1'
        def lookups(self, request, model_admin):
            unique_values = NumberData.objects.values_list('pair1', flat=True).distinct()
            return [(value, value) for value in unique_values]

        def queryset(self, request, queryset):
            if self.value() is not None:
                return queryset.filter(pair1=self.value())
            
    class Field1FilterPair2(admin.SimpleListFilter):
        title = 'pair2 Filter'
        parameter_name = 'pair2'
        def lookups(self, request, model_admin):
            unique_values = NumberData.objects.values_list('pair2', flat=True).distinct()
            return [(value, value) for value in unique_values]

        def queryset(self, request, queryset):
            if self.value() is not None:
                return queryset.filter(pair2=self.value())

    
    list_filter = (Field1Filter,Field1FilterPair,Field1FilterPair2)


class RoundFilter(admin.SimpleListFilter):
    title = 'Round'
    parameter_name = 'round'

    def lookups(self, request, model_admin):
        # Здесь вы можете определить свои собственные значения фильтрации
        return (
            ('0-10', '0 - 10'),
            ('11-50', '11 - 50'),
            ('51-130', '51 - 130'),
            ('131-250', '131 - 250'),
            ('251-500', '251 - 500'),
            ('501-750', '501 - 750'),
            # Добавьте другие интервалы по вашему усмотрению
        )

    def queryset(self, request, queryset):
        if self.value():
            start, end = self.value().split('-')
            return queryset.filter(round__gte=start, round__lte=end)    


class ProfitPriceAdmin(admin.ModelAdmin):
    list_display = ('pair', 'binance', 'huobi', 'gateio', 'kucoin', 'rubs', 'round','spred','clickableBuy_url','clickableSell_url',)


    def clickableBuy_url(self, obj):
        return obj.clickableBuy_url()
    clickableBuy_url.short_description = 'Buy'
    clickableBuy_url.allow_tags = True

    def clickableSell_url(self, obj):
        return obj.clickableSell_url()
    clickableSell_url.short_description = 'Sell'
    clickableSell_url.allow_tags = True




    class buyFilter(admin.SimpleListFilter):
        title = 'buy Filter'
        parameter_name = 'buy'  # Имя параметра запроса, используемое в URL

        def lookups(self, request, model_admin):
            unique_values = ProfitPrice.objects.values_list('buy', flat=True).distinct()
            return [(value, value) for value in unique_values]

        def queryset(self, request, queryset):
            if self.value() is not None:
                return queryset.filter(buy=self.value())
    class sellFilter(admin.SimpleListFilter):
        title = 'sell Filter'
        parameter_name = 'sell'  # Имя параметра запроса, используемое в URL

        def lookups(self, request, model_admin):
            unique_values = ProfitPrice.objects.values_list('sell', flat=True).distinct()
            return [(value, value) for value in unique_values]

        def queryset(self, request, queryset):
            if self.value() is not None:
                return queryset.filter(sell=self.value())
    list_filter = (buyFilter,sellFilter,RoundFilter,)
class setingAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance')

class ProfitPricess(admin.ModelAdmin):
    list_display = ('site', 'paurstart', 'balance1', 'buy1', 'sell1',  'clickablepaur2url', 'balance2', 'buy2', 'sell2', 'clickablepaur3url', 'balance3', 'buy3', 'sell3','clickablepaurstart2url', 'dohod','dohodtyda','dohodsyda')

    class paurstartFilter(admin.SimpleListFilter):
        title = 'paurstart Filter'
        parameter_name = 'paurstart'  # Имя параметра запроса, используемое в URL

        def lookups(self, request, model_admin):
            unique_values = ProfitPrice2.objects.values_list('paurstart', flat=True).distinct()
            return [(value, value) for value in unique_values]

        def queryset(self, request, queryset):
            if self.value() is not None:
                return queryset.filter(paurstart=self.value())

    class paurstart2Filter(admin.SimpleListFilter):
        title = 'paurstart2 Filter'
        parameter_name = 'paurstart2'  # Имя параметра запроса, используемое в URL

        def lookups(self, request, model_admin):
            unique_values = ProfitPrice2.objects.values_list('paurstart2', flat=True).distinct()
            return [(value, value) for value in unique_values]

        def queryset(self, request, queryset):
            if self.value() is not None:
                return queryset.filter(paurstart2=self.value())
            
    class paur3Filter(admin.SimpleListFilter):
        title = 'paur3 Filter'
        parameter_name = 'paur3'  # Имя параметра запроса, используемое в URL

        def lookups(self, request, model_admin):
            unique_values = ProfitPrice2.objects.values_list('paur3', flat=True).distinct()
            return [(value, value) for value in unique_values]

        def queryset(self, request, queryset):
            if self.value() is not None:
                return queryset.filter(paur3=self.value())
   
    class siteFilter(admin.SimpleListFilter):
        title = 'site Filter'
        parameter_name = 'site'  # Имя параметра запроса, используемое в URL

        def lookups(self, request, model_admin):
            unique_values = ProfitPrice2.objects.values_list('site', flat=True).distinct()
            return [(value, value) for value in unique_values]

        def queryset(self, request, queryset):
            if self.value() is not None:
                return queryset.filter(site=self.value())
            
    def clickablepaur2url(self, obj):
        return obj.clickablepaur2url()
    clickablepaur2url.short_description = 'paur2'
    clickablepaur2url.allow_tags = True

    def clickablepaur3url(self, obj):
        return obj.clickablepaur3url()
    clickablepaur3url.short_description = 'paur3'
    clickablepaur3url.allow_tags = True

    def clickablepaurstart2url(self, obj):
        return obj.clickablepaurstart2url()
    clickablepaurstart2url.short_description = 'paurstart2'
    clickablepaurstart2url.allow_tags = True

    list_filter = (paurstart2Filter,siteFilter,paur3Filter,)#paur3Filter,paurstartFilter,

class dashbord_torgov_2(admin.ModelAdmin):
    list_display = ('site',)

admin.site.register(NumberData,NumberDataAdmin)
admin.site.register(ProfitPrice,ProfitPriceAdmin)
admin.site.register(settingAll,setingAdmin)

admin.site.register(dashbord_torgov,dashbord_torgov_2)

admin.site.register(ProfitPrice2,ProfitPricess)

admin.site.register(TradePair)

admin.site.register(TradingPair)

admin.site.register(TradePairRsi)

admin.site.register(TradingPairRsi)

admin.site.register(Utm_metci)