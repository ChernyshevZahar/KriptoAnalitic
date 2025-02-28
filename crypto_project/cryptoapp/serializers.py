from rest_framework import serializers
from cryptoapp.models import *

class NumberDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = NumberData
        fields = '__all__'

class TradingPairSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradingPair
        fields = ['lisen_pair','way_pair','price_pair','user']


class TradingPairRsiSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradingPairRsi
        fields = ['lisen_pair','way_pair','price_pair','user']


class OffTradePairRsiSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradePairRsi
        fields = ['norm', 'pair' , 'off_on']

class OffTradePairRsiSerializer2(serializers.ModelSerializer):
    class Meta:
        model = TradePairRsi
        fields = ['norm', 'pair' , 'off_on']

class SettingDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = settingAll
        fields = '__all__'