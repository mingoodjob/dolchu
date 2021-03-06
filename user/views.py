from django.shortcuts import render, redirect
from .models import UserModel
from food.models import Comment, Food
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def home(request):
    user = request.user.is_authenticated
    if user:
        return redirect('main_view')
    else:
        return render(request, 'user/login.html')

def login(request):
    if request.method == 'POST':
        user = request.POST.get('username','')
        pwd = request.POST.get('password','')
        login = auth.authenticate(request, username=user, password=pwd)
        if login is not None:
            auth.login(request, login)
            return redirect('home')
        else:
            return render(request, 'user/login.html', {'error': '아이디 혹은 패스워드를 확인 해 주세요!'})
        
    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('main_view')
        else:
            return render(request, 'user/login.html')

def join(request):
    if request.method == 'POST':
        user = request.POST.get('username','')
        pwd = request.POST.get('password','')
        pwd2 = request.POST.get('password2','')
        if user == '' or pwd == '':
            return render(request, 'user/join.html',{'error':'아이디 혹은 비밀번호가 입력되지 않았습니다!'})
        elif len(user) > 15 or len(pwd) > 15:
            return render(request, 'user/join.html',{'error':'아이디 혹은 비밀번호는 15자 이상을 초과 할수 없습니다!'})
        elif pwd != pwd2:
            return render(request, 'user/join.html',{'error':'비밀번호가 서로 맞지 않습니다!'})
        else:
            exist_user = get_user_model().objects.filter(username=user)
            if exist_user:
                return render(request, 'user/join.html',{'error':'이미 가입된 사용자 아이디 입니다!'})
            else:
                UserModel.objects.create_user(username=user, password=pwd)
                return render(request, 'user/join.html',{'sucsess':'sucsess'})
        
    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('main_view')
        else:
            return render(request, 'user/join.html')
    
@login_required        
def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required
def mypage_view(request, username):
    if request.method == 'GET':
        username_id = UserModel.objects.get(username=username).id
        comments = Comment.objects.filter(username_id=username_id)
        if not comments:
            find_comment = False
            return render(request, 'user/mypage.html', {'find_comment': find_comment})
        else:
            find_comment = True
            stores = []
            for comment in comments:
                store = Food.objects.get(id=comment.store_id)
                stores.append(store)

            review_stores = zip(stores, comments)
            reviews = {
                'review_stores': review_stores
            }
            return render(request, 'user/mypage.html', {'find_comment': find_comment, 'comments': comments, 'reviews': reviews})