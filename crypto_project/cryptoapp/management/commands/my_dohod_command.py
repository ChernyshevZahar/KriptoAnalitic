from django.core.management.base import BaseCommand
from cryptoapp.models import NumberData ,ProfitPrice, settingAll


class Command(BaseCommand):
    help = 'My custom command'

    def handle(self, *args, **options):
        # while True:
            listpair = []
            data = NumberData.objects.all()
            for ss in data:
                if ss.pair not in listpair:
                    filtered_objects = NumberData.objects.filter(pair=ss.pair)
                    for obj in filtered_objects:
                        
                        createUpData(obj.Site,obj.pair,price=obj.priсe,pair1=obj.pair1,pair2=obj.pair2)
                        
                    listpair.append(ss.pair)
                # time.sleep(10)  # Подождите 10 секунд
                    


def createUpData(site,pair, price,pair1,pair2):  
        
        if site == 'binance':
            obj, created = ProfitPrice.objects.get_or_create(pair=pair, defaults={
                'binance': price,
                'pair1': pair1,
                'pair2': pair2,

            })

            # Если запись существует, обновляем ее значения
            if not created:
                obj.binance = price
                obj.pair1 = pair1
                obj.pair2 = pair2

                obj.save()
        elif site == 'huobi':
            obj, created = ProfitPrice.objects.get_or_create(pair=pair, defaults={
                'huobi': price,
                'pair1': pair1,
                'pair2': pair2,
            })

            # Если запись существует, обновляем ее значения
            if not created:
                obj.huobi = price
                obj.pair1 = pair1
                obj.pair2 = pair2
                obj.save()
        elif site == 'gateio':
            obj, created = ProfitPrice.objects.get_or_create(pair=pair, defaults={
                'gateio': price,
                'pair1': pair1,
                'pair2': pair2,
            })

            # Если запись существует, обновляем ее значения
            if not created:
                obj.gateio = price
                obj.pair1 = pair1
                obj.pair2 = pair2
                obj.save()
        elif site == 'kucoin':
            obj, created = ProfitPrice.objects.get_or_create(pair=pair, defaults={
                'kucoin': price,
                'pair1': pair1,
                'pair2': pair2,
            })

            # Если запись существует, обновляем ее значения
            if not created:
                obj.kucoin = price
                obj.pair1 = pair1
                obj.pair2 = pair2
                obj.save()
        try:
            filtered_objects = settingAll.objects.get(name=pair1)
            obj, created = ProfitPrice.objects.get_or_create(pair=pair, defaults={
                    'rubs': filtered_objects.balance,
                })

                # Если запись существует, обновляем ее значения
            if not created:
                obj.rubs = filtered_objects.balance
                obj.save() 
        except Exception as e:
             pass


            
        
        