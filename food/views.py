from django.shortcuts import render
from . models import Food
# Create your views here.

def main_view(request):
    return render(request, 'food/main.html')

def detail_view(request):
    if request.method == 'GET':
        
        all = Food.objects.get(id=1)
        address = (all.address)
        store = (all.store)
        price = (all.price)
        img = (all.img)
        tel = (all.tel)
        parking =  (all.parking)
        close = (all.close)
        holliday = (all.holliday)

        return render(request, 'food/detail.html',{'address':address,'store':store,'img':img,'tel':tel,'parking':parking,'close':close,'holliday':holliday,'price':price})

