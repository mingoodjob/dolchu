
from django.shortcuts import render, redirect
from .models import Food, Comment
from django.contrib.auth.decorators import login_required
from django.db.models import Avg


def main_view(request):
    return render(request, 'food/main.html')


@login_required
def detail_view(request, id):
    find_food = Food.objects.get(id=id)
    food_id = find_food.id
    food_store = find_food.store
    food_staravg = round(find_food.staravg, 1)

    comments = Comment.objects.filter(store=food_store)

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
        
        return render(request, 'food/detail.html', {'id': food_id, 'staravg': food_staravg, 'comments': comments, 'address':address,'store':store,'img':img,'tel':tel,'parking':parking,'close':close,'holliday':holliday,'price':price}})

    elif request.method == 'POST':
        username = request.user
        comment = request.POST.get('comment')
        star = request.POST.get('star')

        if comment == '':
            return render(request, 'food/detail.html', {'id': food_id, 'error': '코멘트 내용 없음', 'comments': comments})
        elif star == None:
            return render(request, 'food/detail.html', {'id': food_id, 'error': '평점 입력하지 않음', 'comments': comments})
        else:
            model_comment = Comment()
            model_comment.username = username
            model_comment.store = food_store
            model_comment.comment = comment
            model_comment.star = star
            model_comment.save()

            find_food.staravg = comments.aggregate(Avg('star')).get('star__avg')
            find_food.save()

            return redirect('detail_view', id)
    