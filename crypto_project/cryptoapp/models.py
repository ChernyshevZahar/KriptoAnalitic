from django.db import models
from django.utils.safestring import mark_safe

class NumberData(models.Model):
    Site = models.CharField(max_length=20)
    pair = models.CharField(max_length=20)
    pair1 = models.CharField(max_length=20,null=True)
    pair2 = models.CharField(max_length=20,null=True)
    askPrice = models.FloatField()
    askSize = models.FloatField()
    priсe = models.FloatField()
    bidSize = models.FloatField()
    bid = models.FloatField()
    priсe_1m = models.FloatField(null=True)
    datetime_1m = models.DateTimeField(null=True)
    priсe_5m = models.FloatField(null=True)
    datetime_5m = models.DateTimeField(null=True)
    priсe_15m = models.FloatField(null=True)
    datetime_15m = models.DateTimeField(null=True)
    priсe_30m = models.FloatField(null=True)
    datetime_30m = models.DateTimeField(null=True)
    priсe_1h = models.FloatField(null=True)
    datetime_1h = models.DateTimeField(null=True)
    priсe_3h = models.FloatField(null=True)
    datetime_3h = models.DateTimeField(null=True)
    priсe_6h = models.FloatField(null=True)
    datetime_6h = models.DateTimeField(null=True)
    priсe_12h = models.FloatField(null=True)
    datetime_12h = models.DateTimeField(null=True)
    priсe_1d = models.FloatField(null=True)
    datetime_1d = models.DateTimeField(null=True)

class ProfitPrice(models.Model):  
    pair = models.CharField(max_length=20,null=True)
    pair1 = models.CharField(max_length=20,null=True)
    pair2 = models.CharField(max_length=20,null=True)
    binance = models.FloatField(max_length=20,null=True)
    huobi =  models.FloatField(max_length=20,null=True)
    gateio = models.FloatField(max_length=20,null=True)
    kucoin = models.FloatField(max_length=20,null=True)
    rubs = models.FloatField(max_length=20,null=True)
    dolars = models.FloatField(max_length=20,null=True)
    def profitprice(self):
        numbers = [value for value in [self.binance, self.huobi, self.gateio, self.kucoin] if value is not None]
        if numbers:
            end = max(numbers) - min(numbers)
            # print(end)
            return end
        else:
            return None
    profit = models.FloatField(max_length=20,null=True)
    buy = models.CharField(max_length=20,null=True)
    sell = models.CharField(max_length=20,null=True)
    round = models.FloatField(max_length=20,null=True)
    spred = models.FloatField(max_length=20,null=True)
    buyurl = models.URLField(unique=True,null=True)
    sellurl = models.URLField(unique=True,null=True)

    def clickableBuy_url(self):
        return mark_safe(f'<a href="{self.buyurl}" target="_blank">{self.buy}</a>')
    clickableBuy_url.short_description = 'Buy'

    def clickableSell_url(self):
        return mark_safe(f'<a href="{self.sellurl}" target="_blank">{self.sell}</a>')
    clickableSell_url.short_description = 'Sell'

class settingAll(models.Model):
    name = models.CharField(max_length=20,null=True)
    balance = models.FloatField(max_length=20,null=True)
    

class ProfitPrice2(models.Model):
    site = models.CharField(max_length=20,null=True)
    datetime_uploder = models.DateTimeField(null=True)
    paurstart = models.CharField(max_length=20,null=True)
    balance1 = models.FloatField(max_length=20,null=True)
    buy1 = models.FloatField(max_length=20,null=True)
    buyask1 = models.FloatField(max_length=20,null=True)
    sell1 = models.FloatField(max_length=20,null=True)
    sellask1 = models.FloatField(max_length=20,null=True)
    idpaur2 = models.IntegerField(null=True)
    dvizhenie_valut_2 = models.IntegerField(null=True)
    speed_valute_2 = models.IntegerField(null=True)
    paur2 = models.CharField(max_length=20,null=True)
    paur2url = models.URLField(unique=True,null=True)
    balance2 = models.FloatField(max_length=20,null=True)
    buy2 = models.FloatField(max_length=20,null=True)
    buyask2 = models.FloatField(max_length=20,null=True)
    sell2 = models.FloatField(max_length=20,null=True)
    sellask2 = models.FloatField(max_length=20,null=True)
    idpaur3 = models.IntegerField(null=True)
    dvizhenie_valut_3 = models.IntegerField(null=True)
    speed_valute_3 = models.IntegerField(null=True)
    paur3 = models.CharField(max_length=20,null=True)
    paur3url = models.URLField(unique=True,null=True)
    balance3 = models.FloatField(max_length=20,null=True)
    buy3 = models.FloatField(max_length=20,null=True)
    buyask3 = models.FloatField(max_length=20,null=True)
    sell3 = models.FloatField(max_length=20,null=True)
    sellask3 = models.FloatField(max_length=20,null=True)
    idpaur4 = models.IntegerField(null=True)
    dvizhenie_valut_4 = models.IntegerField(null=True)
    speed_valute_4 = models.IntegerField(null=True)
    paurstart2 = models.CharField(max_length=20,null=True)
    paurstart2url = models.URLField(null=True)
    balance4 = models.FloatField(max_length=20,null=True)
    dohod =  models.FloatField(max_length=20,null=True)
    dohodtyda =  models.FloatField(max_length=20,null=True)
    dohodsyda =  models.FloatField(max_length=20,null=True)
    datadohod =  models.DateTimeField(null=True)

    def clickablepaur2url(self):
        return mark_safe(f'<a href="{self.paur2url}" target="_blank">{self.paur2}</a>')
    clickablepaur2url.short_description = 'paur2'

    def clickablepaur3url(self):
        return mark_safe(f'<a href="{self.paur3url}" target="_blank">{self.paur3}</a>')
    clickablepaur2url.short_description = 'paur3'

    def clickablepaurstart2url(self):
        return mark_safe(f'<a href="{self.paurstart2url}" target="_blank">{self.paurstart2}</a>')
    clickablepaur2url.short_description = 'paurstart2'

class dashbord_torgov(models.Model):
    site = models.CharField(max_length=20,null=True)
    type_dohod = models.CharField(max_length=20,null=True,blank=True)
    dohod = models.FloatField(max_length=20,null=True,blank=True)
    fakt_dohod = models.FloatField(max_length=20,null=True,blank=True)
    Data_torgov = models.DateTimeField(null=True,blank=True)

    pair_start = models.CharField(max_length=20,null=True,blank=True)
    price_start = models.FloatField(max_length=20,null=True,blank=True)

    pair1 = models.CharField(max_length=20,null=True,blank=True)
    price_pair1 = models.FloatField(max_length=20,null=True,blank=True)
    dvizhenie_pair1 = models.FloatField(max_length=20,null=True,blank=True)
    speed_pair1 = models.FloatField(max_length=20,null=True,blank=True)

    pair2 = models.CharField(max_length=20,null=True,blank=True)
    price_pair2 = models.FloatField(max_length=20,null=True,blank=True)
    dvizhenie_pair2 = models.FloatField(max_length=20,null=True,blank=True)
    speed_pair2 = models.FloatField(max_length=20,null=True,blank=True)

    pair_end = models.CharField(max_length=20,null=True,blank=True)
    price_end = models.FloatField(max_length=20,null=True,blank=True)
    dvizhenie_end = models.FloatField(max_length=20,null=True,blank=True)
    speed_end = models.FloatField(max_length=20,null=True,blank=True)



    one_id = models.IntegerField(null=True,blank=True)
    one_pair = models.CharField(max_length=20,null=True,blank=True)
    one_pair1 = models.CharField(max_length=20,null=True,blank=True)
    one_pair2 = models.CharField(max_length=20,null=True,blank=True)
    one_askPrice = models.FloatField(max_length=20,null=True,blank=True)
    one_askSize = models.FloatField(max_length=20,null=True,blank=True)
    one_priсe = models.FloatField(max_length=20,null=True,blank=True)
    one_bidSize = models.FloatField(max_length=20,null=True,blank=True)
    one_bid = models.FloatField(max_length=20,null=True,blank=True)
    one_priсe_1m = models.FloatField(null=True,blank=True)
    one_datetime_1m = models.DateTimeField(null=True,blank=True)
    one_priсe_5m = models.FloatField(null=True,blank=True)
    one_datetime_5m = models.DateTimeField(null=True,blank=True)
    one_priсe_15m = models.FloatField(null=True,blank=True)
    one_datetime_15m = models.DateTimeField(null=True,blank=True)
    one_priсe_30m = models.FloatField(null=True,blank=True)
    one_datetime_30m = models.DateTimeField(null=True,blank=True)
    one_priсe_1h = models.FloatField(null=True,blank=True)
    one_datetime_1h = models.DateTimeField(null=True,blank=True)
    one_priсe_3h = models.FloatField(null=True,blank=True)
    one_datetime_3h = models.DateTimeField(null=True,blank=True)
    one_priсe_6h = models.FloatField(null=True,blank=True)
    one_datetime_6h = models.DateTimeField(null=True,blank=True)
    one_priсe_12h = models.FloatField(null=True,blank=True)
    one_datetime_12h = models.DateTimeField(null=True,blank=True)
    one_priсe_1d = models.FloatField(null=True,blank=True)
    one_datetime_1d = models.DateTimeField(null=True,blank=True)


    two_id = models.IntegerField(null=True,blank=True)
    two_pair = models.CharField(max_length=20,null=True,blank=True)
    two_pair1 = models.CharField(max_length=20,null=True,blank=True)
    two_pair2 = models.CharField(max_length=20,null=True,blank=True)
    two_askPrice = models.FloatField(max_length=20,null=True,blank=True)
    two_askSize = models.FloatField(max_length=20,null=True,blank=True)
    two_priсe = models.FloatField(max_length=20,null=True,blank=True)
    two_bidSize = models.FloatField(max_length=20,null=True,blank=True)
    two_bid = models.FloatField(max_length=20,null=True,blank=True)
    two_priсe_1m = models.FloatField(null=True,blank=True)
    two_datetime_1m = models.DateTimeField(null=True,blank=True)
    two_priсe_5m = models.FloatField(null=True,blank=True)
    two_datetime_5m = models.DateTimeField(null=True,blank=True)
    two_priсe_15m = models.FloatField(null=True,blank=True)
    two_datetime_15m = models.DateTimeField(null=True,blank=True)
    two_priсe_30m = models.FloatField(null=True,blank=True)
    two_datetime_30m = models.DateTimeField(null=True,blank=True)
    two_priсe_1h = models.FloatField(null=True,blank=True)
    two_datetime_1h = models.DateTimeField(null=True,blank=True)
    two_priсe_3h = models.FloatField(null=True,blank=True)
    two_datetime_3h = models.DateTimeField(null=True,blank=True)
    two_priсe_6h = models.FloatField(null=True,blank=True)
    two_datetime_6h = models.DateTimeField(null=True,blank=True)
    two_priсe_12h = models.FloatField(null=True,blank=True)
    two_datetime_12h = models.DateTimeField(null=True,blank=True)
    two_priсe_1d = models.FloatField(null=True,blank=True)
    two_datetime_1d = models.DateTimeField(null=True,blank=True)


    theer_id = models.IntegerField(null=True,blank=True)
    theer_pair = models.CharField(max_length=20,null=True,blank=True)
    theer_pair1 = models.CharField(max_length=20,null=True,blank=True)
    theer_pair2 = models.CharField(max_length=20,null=True,blank=True)
    theer_askPrice = models.FloatField(max_length=20,null=True,blank=True)
    theer_askSize = models.FloatField(max_length=20,null=True,blank=True)
    theer_priсe = models.FloatField(max_length=20,null=True,blank=True)
    theer_bidSize = models.FloatField(max_length=20,null=True,blank=True)
    theer_bid = models.FloatField(max_length=20,null=True,blank=True)
    theer_priсe_1m = models.FloatField(null=True,blank=True)
    theer_datetime_1m = models.DateTimeField(null=True,blank=True)
    theer_priсe_5m = models.FloatField(null=True,blank=True)
    theer_datetime_5m = models.DateTimeField(null=True,blank=True)
    theer_priсe_15m = models.FloatField(null=True,blank=True)
    theer_datetime_15m = models.DateTimeField(null=True,blank=True)
    theer_priсe_30m = models.FloatField(null=True,blank=True)
    theer_datetime_30m = models.DateTimeField(null=True,blank=True)
    theer_priсe_1h = models.FloatField(null=True,blank=True)
    theer_datetime_1h = models.DateTimeField(null=True,blank=True)
    theer_priсe_3h = models.FloatField(null=True,blank=True)
    theer_datetime_3h = models.DateTimeField(null=True,blank=True)
    theer_priсe_6h = models.FloatField(null=True,blank=True)
    theer_datetime_6h = models.DateTimeField(null=True,blank=True)
    theer_priсe_12h = models.FloatField(null=True,blank=True)
    theer_datetime_12h = models.DateTimeField(null=True,blank=True)
    theer_priсe_1d = models.FloatField(null=True,blank=True)
    theer_datetime_1d = models.DateTimeField(null=True,blank=True)


    
class TradePair(models.Model):
    site = models.CharField(max_length=100)
    pair_step_1 = models.CharField(max_length=100)
    pair_step_1_pair1 = models.CharField(max_length=100)
    pair_step_1_pair2 = models.CharField(max_length=100)
    pair_step_1_price = models.CharField(max_length=100)
    pair_step_1_price_line_up  = models.CharField(max_length=100)
    pair_step_1_price_line_down  = models.CharField(max_length=100)
    pair_step_2 = models.CharField(max_length=100)
    pair_step_2_pair1 = models.CharField(max_length=100)
    pair_step_2_pair2 = models.CharField(max_length=100)
    pair_step_2_price = models.CharField(max_length=100)
    pair_step_2_price_line_up  = models.CharField(max_length=100)
    pair_step_2_price_line_down  = models.CharField(max_length=100)
    pair_step_3 = models.CharField(max_length=100)
    pair_step_3_pair1 = models.CharField(max_length=100)
    pair_step_3_pair2 = models.CharField(max_length=100)
    pair_step_3_price = models.CharField(max_length=100)
    pair_step_3_price_line_up  = models.CharField(max_length=100)
    pair_step_3_price_line_down  = models.CharField(max_length=100)
    dohod_go = models.CharField(max_length=100)
    dohod_back = models.CharField(max_length=100)
    up_Data = models.DateTimeField(null=True,blank=True)



class TradingPair(models.Model):
    site = models.CharField(max_length=100, null=True,blank=True )
    pair_step_1_pair2 = models.CharField(max_length=100 , null=True,blank=True)
    pair_step_1_price = models.CharField(max_length=100 , null=True,blank=True)
    pair_step_2_pair2 = models.CharField(max_length=100 , null=True,blank=True)
    pair_step_2_price = models.CharField(max_length=100 , null=True,blank=True) 
    pair_step_3_pair2 = models.CharField(max_length=100 , null=True,blank=True)
    pair_step_3_price = models.CharField(max_length=100 , null=True,blank=True)
    fakt_dohod = models.CharField(max_length=100 , null=True,blank=True)
    lisen_pair = models.CharField(max_length=100 , null=True,blank=True)
    way_pair = models.CharField(max_length=100 , null=True,blank=True)
    price_pair = models.CharField(max_length=100 , null=True,blank=True)
    user = models.CharField(max_length=100 , null=True,blank=True)


class TradePairRsi(models.Model):
    site = models.CharField(max_length=100, null=True,blank=True )
    pair = models.CharField(max_length=100 , null=True,blank=True)
    pair_up = models.CharField(max_length=100 , null=True,blank=True)
    pair_down = models.CharField(max_length=100 , null=True,blank=True)
    pair_price = models.CharField(max_length=100 , null=True,blank=True) 
    pair_rsi = models.CharField(max_length=100 , null=True,blank=True)
    lisen_pair_rsi = models.CharField(max_length=100 , null=True,blank=True)
    way_pair_rsi = models.CharField(max_length=100 , null=True,blank=True)
    price_pair_rsi = models.CharField(max_length=100 , null=True,blank=True)
    up_Data = models.DateTimeField(null=True,blank=True)
    off_on = models.BooleanField(default=True, verbose_name="Переключатель")
    norm = models.BooleanField(default=True, verbose_name="Переключатель2")



class TradingPairRsi(models.Model):
    site = models.CharField(max_length=100, null=True,blank=True )
    pair = models.CharField(max_length=100 , null=True,blank=True)
    pair_up = models.CharField(max_length=100 , null=True,blank=True)
    pair_down = models.CharField(max_length=100 , null=True,blank=True)
    pair_price = models.CharField(max_length=100 , null=True,blank=True) 
    pair_rsi = models.CharField(max_length=100 , null=True,blank=True)
    lisen_pair = models.CharField(max_length=100 , null=True,blank=True)
    way_pair = models.CharField(max_length=100 , null=True,blank=True)
    price_pair = models.CharField(max_length=100 , null=True,blank=True)
    user = models.CharField(max_length=100 , null=True,blank=True)

class Utm_metci(models.Model):
    Name = models.CharField(max_length=100, null=True,blank=True )
    utm = models.CharField(max_length=100 , null=True,blank=True)
    user = models.CharField(max_length=100 , null=True,blank=True)

    

    
    