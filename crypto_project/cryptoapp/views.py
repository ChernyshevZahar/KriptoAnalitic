from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import NumberData, ProfitPrice2, settingAll, TradePair,TradingPair,TradePairRsi,TradingPairRsi
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from cryptoapp.serializers import *
from rest_framework import viewsets, generics
from django.shortcuts import get_object_or_404
from django.core.management import call_command
from django.http import HttpResponse
from django.utils import timezone

from django.core.exceptions import ValidationError
import json

from django.http import JsonResponse

from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from django.db.models import Q

from .forms import YourForm,Add_traid,Add_traid_rsi

import traceback

@login_required
def dashboard_view(request):
    date_sort_by = request.GET.get('date')
    price_sort_by = request.GET.get('price')
    balanse = get_object_or_404(settingAll, name='balance')
    # print(sort_by)  # Получение параметра сортировки из запроса
    
   
    if price_sort_by:
        data = NumberData.objects.all().order_by(price_sort_by)
    elif date_sort_by:
        data = NumberData.objects.all().order_by(date_sort_by)
    else:
        data = NumberData.objects.all()
    paginator = Paginator(data, 15)  # Разбиваем данные на страницы по 10 элементов
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    return render(request, 'dashboard.html', {'items': items, "balanse":balanse})

@login_required
def dashboard_Price_view(request):
    price_sort_by_dohodtyda = request.GET.get('dohodtyda')
    price_sort_by_dohodsyda = request.GET.get('dohodsyda')
    balanse = get_object_or_404(settingAll, name='balance')
    # print(price_sort_by)  # Получение параметра сортировки из запроса
   
    if price_sort_by_dohodtyda:
        data = ProfitPrice2.objects.filter(dohodtyda__isnull=False).order_by(price_sort_by_dohodtyda)
    elif price_sort_by_dohodsyda:
        data = ProfitPrice2.objects.filter(dohodsyda__isnull=False).order_by(price_sort_by_dohodsyda)
    else:
        data = ProfitPrice2.objects.filter(dohodsyda__isnull=False)
   
    
    paginator = Paginator(data, 15)  # Разбиваем данные на страницы по 10 элементов
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    return render(request, 'dashboard_price2.html', {'items': items, "balanse":balanse})

@login_required
def dashboard_price2_detail(request, item_id):
    item = get_object_or_404(ProfitPrice2, pk=item_id)
    pair1 = get_object_or_404(NumberData, pk=item.idpaur2)
    pair2 = get_object_or_404(NumberData, pk=item.idpaur3)
    pair3 = get_object_or_404(NumberData, pk=item.idpaur4)
    balanse = get_object_or_404(settingAll, name='balance')
    USDT =  get_object_or_404(settingAll, name='USDT')
    USDTAll = round(balanse.balance/USDT.balance, 3)
    try:
            if request.method == 'POST':
                form = YourForm(request.POST)
                if form.is_valid():
                    try:
                        your_model_instance = form.save(commit=False)
                        your_model_instance.Data_torgov = timezone.now()
                        pair_1 = get_object_or_404(NumberData, pk=form.cleaned_data['one_id'])
                        # pair_2 = get_object_or_404(NumberData, pk=form.cleaned_data['two_id'])
                        # pair_3 = get_object_or_404(NumberData, pk=form.cleaned_data['theer_id'])
                        

                        takedatanum('one_',your_model_instance,pair_1)
                        # takedatanum('two_',your_model_instance,pair_2)
                        # takedatanum('theer_',your_model_instance,pair_3)
                        print(form.cleaned_data['fakt_dohod'])
                        # print(balanse.balance)
                        # balanse.balance = balanse.balance + float(form.cleaned_data['fakt_dohod'])
                        # balanse.save()



                        your_model_instance.save()
                        return redirect(f'/dashboardprice2/{item_id}')  # Перенаправляем на страницу успешного сохранения
                    except Exception as e:
                        print(e)
                        traceback.print_exc()
            else:
                form = YourForm()
            # В этом примере мы возвращаем HttpResponse с данными объекта. Вы можете выбрать другой способ отображения данных.
            return render(request, 'dashboard_price2_all.html', {'item': item, 'pair1': pair1, 'pair2': pair2, 'pair3': pair3, 'from': form, 'USDTAll':USDTAll, "balanse":balanse, 'USDT': USDT})
    except Exception as e:
        print(e)


@login_required
def run_custom_command(request):
    # Выполнение команды
    call_command('my_dohod2_command')
    return HttpResponse('Custom command executed successfully')

@login_required
def run_custom_command_cena(request):
    # Выполнение команды
    call_command('my_prise2_command')
    return HttpResponse('Custom command executed successfully')






class NumberDataBySiteAndPairAPIView(generics.ListAPIView):
    serializer_class = NumberDataSerializer

    def get_queryset(self):
        site = self.kwargs['site']
        pair = self.kwargs['pair']
        return NumberData.objects.filter(Site=site, pair=pair)

class NumberDataViewSet(viewsets.ModelViewSet):
    queryset = NumberData.objects.all()
    serializer_class = NumberDataSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    
class TokenDelete(APIView):
    def delete(self, request, format=None):
        try:
            token = Token.objects.get(key=request.auth.key)
            token.delete()
            return Response("Токен успешно удален", status=status.HTTP_204_NO_CONTENT)
        except Token.DoesNotExist:
            return Response("Токен не найден", status=status.HTTP_404_NOT_FOUND)
        

def takedatanum(d, your_model_instance, pair1):

    list = ['pair','pair1','pair2','askPrice','askSize','priсe','bidSize','bid',
            'priсe_1m','datetime_1m','priсe_5m','datetime_5m','priсe_15m','datetime_15m',
            'priсe_30m','datetime_30m','priсe_1h','datetime_1h','priсe_3h','datetime_3h',
            'priсe_6h','datetime_6h','priсe_12h','datetime_12h','priсe_1d','datetime_1d']


    for e in list:

        setattr(your_model_instance, d+e, getattr(pair1, e))

    return your_model_instance


@api_view(['POST'])
def upload_trade_pairs(request):
    uploaded_file = request.FILES['file']
    data = json.load(uploaded_file)

    for item in data:
        site = item['site']
        pair_step_1 = item['pair_step_1_pair1']
        # Добавьте другие поля, которые вы хотите использовать для проверки

        # Проверка существующих данных и обновление или создание новой записи
        trade_pair, _ = TradePair.objects.update_or_create(
            site=site,
            pair_step_1_pair1=pair_step_1,
            defaults={
                'pair_step_1': item['pair_step_1'],
                'pair_step_1_pair1': item['pair_step_1_pair1'],
                'pair_step_1_pair2': item['pair_step_1_pair2'],
                'pair_step_1_price': item['pair_step_1_price'],
                'pair_step_1_price_line_up' : item['pair_step_1_price_line_up'],
                'pair_step_1_price_line_down' : item['pair_step_1_price_line_down'],
                'pair_step_2': item['pair_step_2'],
                'pair_step_2_pair1': item['pair_step_2_pair1'],
                'pair_step_2_pair2': item['pair_step_2_pair2'],
                'pair_step_2_price': item['pair_step_2_price'],
                'pair_step_2_price_line_up' : item['pair_step_2_price_line_up'],
                'pair_step_2_price_line_down' : item['pair_step_2_price_line_down'],
                'pair_step_3': item['pair_step_3'],
                'pair_step_3_pair1': item['pair_step_3_pair1'],
                'pair_step_3_pair2': item['pair_step_3_pair2'],
                'pair_step_3_price': item['pair_step_3_price'],
                'pair_step_3_price_line_up' : item['pair_step_3_price_line_up'],
                'pair_step_3_price_line_down' : item['pair_step_3_price_line_down'],
                'dohod_go': item['dohod_go'],
                'dohod_back': item['dohod_back'],
                'up_Data' : timezone.now()
            }
        )

    return Response({'message': 'Data has been successfully added/updated'}, status=200)

@login_required
def trade_pair_list(request):
    trade_pairs = TradePair.objects.all()
    My_USDT = get_object_or_404(settingAll, name='My_USDT')

    USDT =  get_object_or_404(settingAll, name='USDT')
    balanse = float(My_USDT.balance)*float(USDT.balance)
    menu_items = TradingPair.objects.all()
   
    if request.method == 'POST':
        form = Add_traid(request.POST)
        # print(form.is_valid())
        if form.is_valid():
            your_model_instance = form.save(commit=False)

            your_model_instance.save()
            return redirect('/trade-pairs')  
    else:
        form = Add_traid()

    return render(request, 'new_trade_dashboard.html', {'trade_pairs': trade_pairs, 'USDTAll': My_USDT, "balanse": balanse, 'USDT': USDT, 'form': form,'menu_items': menu_items})


def update_trade_pair(request, trade_pair_id):
    trade_pair = get_object_or_404(TradingPair, id=trade_pair_id)
    if request.method == 'POST':
        trade_pair.pair_step_1_price = request.POST.get('pair_step_1_price')
        trade_pair.pair_step_2_price = request.POST.get('pair_step_2_price')
        trade_pair.pair_step_3_price = request.POST.get('pair_step_3_price')
        trade_pair.fakt_dohod = request.POST.get('fakt_dohod')
        trade_pair.lisen_pair = request.POST.get('lisen_pair')
        trade_pair.way_pair = request.POST.get('way_pair')
        trade_pair.price_pair = request.POST.get('price_pair')
        # Другие поля формы
        trade_pair.save()

        return redirect('/trade-pairs')  # Перенаправить на другую страницу после успешного обновления
    else:
        return redirect('/trade-pairs')

def delete_trade_pair(request, trade_pair_id):
    trade_pair = get_object_or_404(TradingPair, id=trade_pair_id)
    trade_pair.delete()
    return redirect('/trade-pairs')  # Перенаправить на другую страницу после успешного удаления


class TradingPairListView(generics.ListAPIView):
    queryset = TradingPair.objects.all()
    serializer_class = TradingPairSerializer
    pagination_class = None  # Отключаем пагинацию, если не нужна



@api_view(['POST'])
def upload_trade_pairs_rsi(request):
    print('dd')
    uploaded_file = request.FILES['file']
    data = json.load(uploaded_file)

    for item in data:
        site = item['site']
        pair_step_1 = item['pair']
        # Добавьте другие поля, которые вы хотите использовать для проверки

        # Проверка существующих данных и обновление или создание новой записи
        trade_pair, _ = TradePairRsi.objects.update_or_create(
            site=site,
            pair=pair_step_1,
            defaults={
            #     'pair_up': item['pair_up'],
            #     'pair_down': item['pair_down'],
                'pair_price': item['pair_price'],
                'pair_rsi': item['pair_rsi'],
                'up_Data' : timezone.now(),
                'norm' : item['norm']
            }
        )

    return Response({'message': 'Data has been successfully added/updated'}, status=200)

@login_required
def trade_pair_list_rsi(request, user):
    trade_pairs = TradePairRsi.objects.exclude(off_on=False)
    select = get_object_or_404(Utm_metci, Name='sort_rsi', user=user)
    select2 = get_object_or_404(Utm_metci, Name='sort_top', user=user)
    My_USDT = get_object_or_404(settingAll, name='My_USDT')

    USDT =  get_object_or_404(settingAll, name='USDT')
    balanse = float(My_USDT.balance)*float(USDT.balance)
    menu_items = TradingPairRsi.objects.all()


    sort_rsi = request.GET.get('sort_rsi')
    sort_top = request.GET.get('sort_top')
    print(sort_top)  # Получение параметра сортировки из запроса
   
    
    if sort_rsi == 'pair_rsi_up':
        if sort_top == 'on':
            trade_pairs = TradePairRsi.objects.exclude(off_on=False).filter(norm=True).order_by('pair_rsi')
        elif sort_top == 'off':
            print('pair_rsi_up')
            trade_pairs = TradePairRsi.objects.exclude(off_on=False).filter(norm=False).order_by('pair_rsi')
        else: 
            trade_pairs = TradePairRsi.objects.exclude(off_on=False).order_by('pair_rsi') 
    elif sort_rsi == 'pair_rsi_down':
        if sort_top == 'on':
            trade_pairs = TradePairRsi.objects.exclude(off_on=False).filter(norm=True).order_by('-pair_rsi')
        elif sort_top == 'off':
            print('pair_rsi_down')
            trade_pairs = TradePairRsi.objects.exclude(off_on=False).filter(norm=False).order_by('-pair_rsi').exclude()
        else: 
            trade_pairs = TradePairRsi.objects.exclude(off_on=False).order_by('-pair_rsi') 
    else:
        if sort_top == 'on':
            trade_pairs = TradePairRsi.objects.exclude(off_on=False).filter(norm=True)
        elif sort_top == 'off':
            print('no')
            trade_pairs = TradePairRsi.objects.exclude(off_on=False).filter(norm=False)
        else: 
            trade_pairs = TradePairRsi.objects.exclude(off_on=False)

   
    if request.method == 'POST':
        form = Add_traid_rsi(request.POST)
        print(form.is_valid())
        if form.is_valid():
            your_model_instance = form.save(commit=False)

            your_model_instance.save()
            return redirect(f'/trade-pairs-rsi/{user}{take_utm(user)}')  
    else:
        form = Add_traid_rsi()

    return render(request, 'rsi_all.html', {'trade_pairs': trade_pairs, 'USDTAll': My_USDT, "balanse": str(balanse), 'USDT': USDT,'form':form, 'menu_items': menu_items, 'select':select, 'select2': select2})


def update_trade_pair_rsi(request, trade_pair_id,user):
    trade_pair = get_object_or_404(TradingPairRsi, id=trade_pair_id)
    if request.method == 'POST':
        trade_pair.lisen_pair = request.POST.get('lisen_pair')
        trade_pair.way_pair = request.POST.get('way_pair')
        trade_pair.price_pair = request.POST.get('price_pair')
        # Другие поля формы
        trade_pair.save()

        return redirect(f'/trade-pairs-rsi/{user}{take_utm(user)}')  # Перенаправить на другую страницу после успешного обновления
    else:
        return redirect(f'/trade-pairs-rsi/{user}{take_utm(user)}')

def delete_trade_pair_rsi(request, trade_pair_id,user):
    trade_pair = get_object_or_404(TradingPairRsi, id=trade_pair_id)
    trade_pair.delete()
    return redirect(f'/trade-pairs-rsi/{user}{take_utm(user)}')  # Перенаправить на другую страницу после успешного удаления

def Off_trade_pair_rsi(request, trade_pair_id,user):
    trade_pair = get_object_or_404(TradePairRsi, id=trade_pair_id)
    if request.method == 'POST':
        trade_pair.norm = False
        # Другие поля формы
        trade_pair.save()

        return redirect(f'/trade-pairs-rsi/{user}{take_utm(user)}')  # Перенаправить на другую страницу после успешного обновления
    else:
        return redirect(f'/trade-pairs-rsi/{user}{take_utm(user)}')

def up_trade_pair_rsi(request, trade_pair_id,user):
    trade_pair = get_object_or_404(TradePairRsi, id=trade_pair_id)
    if request.method == 'POST':
        print(request.POST.get('norm'))
        if request.POST.get('norm') == 'on':
            trade_pair.norm = True
            # Другие поля формы
            trade_pair.save()
        elif request.POST.get('norm') == None:
            trade_pair.norm = False
            # Другие поля формы
            trade_pair.save()
        return redirect(f'/trade-pairs-rsi/{user}{take_utm(user)}')  # Перенаправить на другую страницу после успешного обновления
    else:
        return redirect(f'/trade-pairs-rsi/{user}{take_utm(user)}')



class TradingPairRsiListView(generics.ListAPIView):
    queryset = TradingPairRsi.objects.all()
    serializer_class = TradingPairRsiSerializer
    pagination_class = None

    def put(self, request, **kwargs):
        """
        Обновление way_pair и price_pair по lisen_pair.
        """
        lisen_pair = request.data.get('lisen_pair')
        way_pair = request.data.get('way_pair')
        price_pair = request.data.get('price_pair')

        if not lisen_pair:
            return Response({'error': 'lisen_pair is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            trading_pair = TradingPairRsi.objects.get(lisen_pair=lisen_pair)

            # Проверка way_pair (добавьте свою логику валидации)
            if way_pair is not None and way_pair not in [0, 1]:
                raise ValidationError("Invalid way_pair value")

            # Проверка price_pair (добавьте свою логику валидации)
            if price_pair is not None and not isinstance(price_pair, (int, float)):
                raise ValidationError("Invalid price_pair value")

            trading_pair.way_pair = way_pair
            trading_pair.price_pair = price_pair
            trading_pair.save()

            serializer = self.serializer_class(trading_pair)
            return Response(serializer.data)

        except TradingPairRsi.DoesNotExist:
            return Response({'error': 'Trading pair not found'}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SettingData(generics.ListAPIView):
    queryset = settingAll.objects.all()
    serializer_class = SettingDataSerializer
    def put(self, request, *args, **kwargs):
        """
        Обновляет данные настройки с именем "My_usdt".
        """
        try:
            setting = settingAll.objects.get(name="My_USDT")
        except settingAll.DoesNotExist:
            return Response({"detail": "Setting not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = SettingDataSerializer(setting, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OffTradePairRsiListView(generics.ListAPIView):
    serializer_class = OffTradePairRsiSerializer

    def get_queryset(self):
        """
        Возвращает список объектов TradePairRsi с off_on=False.
        """
        return TradePairRsi.objects.filter(norm=True).exclude(off_on=False)  

class OffTradePairRsiListView2(generics.ListAPIView):
    serializer_class = OffTradePairRsiSerializer2

    def get_queryset(self):
        """
        Возвращает список объектов TradePairRsi с off_on=False.
        """
        return TradePairRsi.objects.filter(norm=False).exclude(off_on=False)

def up_trade_sort(request,user ):
    if request.method == 'POST':
        Utm_metci.objects.filter(Name='sort_rsi',user=user).update(utm=request.POST.get('sort_rsi'))
        Utm_metci.objects.filter(Name='sort_top',user=user).update(utm=request.POST.get('sort_top'))
       
        return redirect(f'/trade-pairs-rsi/{user}{take_utm(user)}')  # Перенаправить на другую страницу после успешного обновления
    else:
        return redirect(f'/trade-pairs-rsi/{user}{take_utm(user)}')


def take_utm(user):
    Utm_metci2 = Utm_metci.objects.filter(user=user)
    utm_m = '?'
    for i in Utm_metci2:
        if i.utm != None:
            utm_m = utm_m + f'{i.Name}={i.utm}&'
    return utm_m