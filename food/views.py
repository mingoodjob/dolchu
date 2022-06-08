from django.shortcuts import render, redirect
from .models import Food, Comment, Category
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.db.models import Q
from itertools import chain

def main_view(request):
    user = request.user.is_authenticated
    if user:
        food_data = Food.objects.all().order_by('staravg')
        categoies = Category.objects.all()
        return render(request, 'food/main.html', {'food_data' : food_data, 'categoies' : categoies})
    else:
        return render(request, 'user/login.html')


@login_required
def category_get(request,id):
    categoies = Category.objects.all()
    category = Category.objects.get(id=id)
    food_data = Food.objects.filter(category=category)
    return render(request, 'food/main.html', {'food_data' : food_data, 'categoies' : categoies})

def search(request):
    if request.method =='POST':
        post = request.POST.get('search','')
        all = Food.objects.all()
        result = all.filter(
            Q(category__category__contains= post)  |
            Q(store__icontains = post) |
            Q(address__icontains = post),
        )

        return render(request,'search.html',{'post':post,'result':result})


@login_required
def detail_view(request, id):
    all = Food.objects.get(id=id)
    food_id = all.id
    address = all.address
    store = all.store
    price = all.price
    img = all.img
    tel = all.tel
    parking = all.parking
    close = all.close
    holiday = all.holiday

    find_food = Food.objects.get(id=id)
    if find_food.staravg != None:
        food_staravg = round(find_food.staravg, 1)
    else:
        food_staravg = '리뷰가 없어요'

    comments = Comment.objects.filter(store=store)

    if request.method == 'GET':
        
        return render(request, 'food/detail.html', {
            'id': food_id, 
            'staravg': food_staravg, 
            'comments': comments, 
            'address':address, 
            'store':store, 
            'img': img, 
            'tel': tel, 
            'parking':parking, 
            'close': close, 
            'holiday': holiday, 
            'price': price
            })

    elif request.method == 'POST':
        username = request.user
        comment = request.POST.get('comment')
        star = request.POST.get('star')

        if comment == '':
            return render(request, 'food/detail.html', {
                'id': food_id, 
                'error': '코멘트 내용 없음', 
                'staravg': food_staravg, 
                'comments': comments, 
                'address': address, 
                'store': store, 
                'img': img, 
                'tel': tel, 
                'parking': parking, 
                'close': close, 
                'holiday': holiday, 
                'price': price
                })
        elif star == None:
            return render(request, 'food/detail.html', {
                'id': food_id, 
                'error': '평점 입력하지 않음', 
                'staravg': food_staravg, 
                'comments': comments, 
                'address': address, 
                'store': store, 
                'img': img, 
                'tel': tel, 
                'parking': parking, 
                'close': close, 
                'holiday': holiday, 
                'price': price
                })
        else:
            model_comment = Comment()
            model_comment.username = username
            model_comment.store = store
            model_comment.comment = comment
            model_comment.star = star
            model_comment.save()

            find_food.staravg = comments.aggregate(Avg('star')).get('star__avg')
            find_food.save()

            return redirect('detail_view', id)
    