from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core import serializers
from .models import Food, Comment, Category,Travel
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
import random
from django.views.decorators.csrf import csrf_exempt


count = 0

@login_required
def main_view(request):
    global count 
    count = 0
    user = request.user.is_authenticated
    if user:
        food_data = Food.objects.all().order_by('-staravg')[:20]
        categoies = Category.objects.all()

        category_count = 0
        categories1 = []
        categories2 = []
        for i in categoies:
            category_count += 1
            cate = {
                'id': i.id,
                'category' : i.category,
                'desc' : i.desc,
            }
            if category_count <= 4:
                categories1.append(cate)
            else:
                categories2.append(cate)

        best_store = []

        for x in categoies:
            store = Food.objects.filter(category=x.id)
            best_stores = store.all().order_by('-staravg')[:1]
            for s in best_stores:
                doc = {
                    'id' : s.id,
                    'store' : s.store,
                    'img' : s.img,
                }
                best_store.append(doc)

        best_food = random.choice(best_store)

        return render(request, 'food/main.html', {'food_data' : food_data, 'categories1' : categories1, 'categories2' : categories2, 'best_food' : best_food})
    else:
        return render(request, 'user/login.html')


# 카테고리별  무한스크롤
@login_required
@csrf_exempt
def ajax_method(request, cate=None):
    user = request.user.is_authenticated
    if user:
        if request.method == 'POST':
            category = request.POST.get('category')
            return HttpResponse(category, content_type="text/json-comment-filtered")
        if request.method == 'GET':
            global count
            count += 1
            for i in str(count):
                if i == i:
                    category = Category.objects.get(id=cate)
                    food_data = Food.objects.filter(category=category).order_by('-staravg')[count * 10:count * 10 + 10]
                    category = serializers.serialize('json', food_data)
                    return HttpResponse(category, content_type="text/json-comment-filtered")

# 메인페이지 무한스크롤
def ajax_method_main(request):
    user = request.user.is_authenticated
    if user:      
        if request.method == 'GET':
            global count
            count += 1
            for i in str(count):
                if i == i:
                    food_data = Food.objects.all().order_by('-staravg')[count * 10:count * 10 + 10]
                    category = serializers.serialize('json', food_data)
                    return HttpResponse(category, content_type="text/json-comment-filtered")


@login_required
def category_get(request,id):
    global count
    count = 0
    categoies = Category.objects.all()

    category_count = 0
    categories1 = []
    categories2 = []
    for i in categoies:
        category_count += 1
        cate = {
            'id': i.id,
            'category' : i.category,
            'desc' : i.desc,
        }
        if category_count <= 4:
            categories1.append(cate)
        else:
            categories2.append(cate)

    category = Category.objects.get(id=id)
    food_data = Food.objects.filter(category=category).order_by('-staravg')[:10]

    best_store = []

    for x in categoies:
        store = Food.objects.filter(category=x.id)
        best_stores = store.all().order_by('-staravg')[:1]
        for s in best_stores:
            doc = {
                'id' : s.id,
                'store' : s.store,
                'img' : s.img,
            }
            best_store.append(doc)

    best_food = random.choice(best_store)
    


    return render(request, 'food/category.html', {'food_data' : food_data, 'categories1' : categories1, 'categories2' : categories2, 'best_food' : best_food})

@login_required
def search(request):
    global count 
    count = 0
    if request.method =='POST':
        post = request.POST.get('search','')
        all = Food.objects.all()
        result = all.filter(
            Q(category__category__contains= post)  |
            Q(store__icontains = post) |
            Q(address__icontains = post),
        )

        for results in result:
            if results.img == "":
                results.img = './static/img/noimage.png'

        return render(request,'search.html',{'post':post,'result':result})


@login_required
def detail_view(request, id):
    global count
    count = 0
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

    add = address.split(' ')[2]
    
    travel = Travel.objects.filter(region=add)

    comments = Comment.objects.filter(store=id)
    staravg = comments.aggregate(Avg('star')).get('star__avg')
    if staravg != None:
        food_staravg = round(staravg, 1)
    else:
        food_staravg = '리뷰가 없어요'

    
    if address == "":
        address = '내용없음'
    if price == "":
        price = '내용없음'
    if img =="":
        img = './static/img/noimage.png'
    if tel == "":
        tel = '내용없음'
    if parking == "":
        parking = '내용없음'
    if close == "":
        close = '내용없음'
    if holiday == "":
        holiday = '내용없음'

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
            'price': price,
            'travel': travel
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
            f = open('user_rating.csv', 'a', encoding='utf-8')

            model_comment = Comment()
            model_comment.username = username
            model_comment.store = Food.objects.get(id=id)
            model_comment.comment = comment
            model_comment.star = star
            model_comment.save()

            store_name = Food.objects.get(id=id)

            f.write(f'{request.user.id},{store_name.store},{star}\n')

            f.close()
            

            all.staravg = staravg
            all.save()

            return redirect('detail_view', id)


@login_required
def delete_comment(request, id):
    if request.method == 'POST':
        username = request.POST.get('username')
        comment = request.POST.get('comment')
        if request.user.username == username:
            find_comment = Comment.objects.get(username_id=request.user.id, comment=comment)
            find_comment.delete()
            return redirect('detail_view', id)
        else:
            return redirect('detail_view', id)