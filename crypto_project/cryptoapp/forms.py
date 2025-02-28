from django import forms
from .models import dashbord_torgov , TradingPair, TradingPairRsi  # Замените YourModel на вашу модель

class YourForm(forms.ModelForm):
    class Meta:
        model = dashbord_torgov
        fields = '__all__' 


class Add_traid(forms.ModelForm):
    class Meta:
        model = TradingPair
        fields = '__all__' 

class Add_traid_rsi(forms.ModelForm):
    class Meta:
        model = TradingPairRsi
        fields = '__all__' 