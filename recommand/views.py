import pandas as pd
import numpy as np
import random
from sklearn.metrics.pairwise import cosine_similarity
from django.shortcuts import render, redirect
from food.models import Food, Comment,Category
from user.models import UserModel
from django.contrib.auth.decorators import login_required

def recommand(request):
    userid = request.user.id
    comment = Comment.objects.filter(username=userid)

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

    if not comment:
        return render(request, 'food/recommand.html', {'message': '평점을 남겨주세요', 'best_food' : best_food, 'categories1' : categories1, 'categories2' : categories2})


    rating = pd.read_csv('user_rating.csv')
    store = pd.read_csv('store_info.csv')

	# 상점명(store)을 기준으로 rating 와 store 를 결합함
    store_ratings = pd.merge(rating, store, on='store')

	# user별로 상점에 부여한 rating 값을 볼 수 있도록 pivot table 사용
    title_user = store_ratings.pivot_table('rating', index='userid', columns='store')

	# 평점을 부여안한 영화는 그냥 0이라고 부여
    title_user = title_user.fillna(0)

	#  모든 유저간의 코사인 유사도를 구함
    user_based_collab = cosine_similarity(title_user, title_user)

	# 위는 그냥 numpy 행렬이니까, 이를 데이터프레임으로 변환
    user_based_collab = pd.DataFrame(user_based_collab, index=title_user.index, columns=title_user.index)

	# 현재 유저와 가장 비슷한 유저를 뽑고
    user = user_based_collab[userid].sort_values(ascending=False)[:10].index[1]
	# 위에 유저의 가장높게 부여한 가게를 내림차순으로 정렬
    recommand_store = title_user.query(f"userid == {user}").sort_values(ascending=False, by=user, axis=1)
    # 위에꺼 리스트로 10개만 가져옴
    recommand_list = recommand_store.columns.tolist()[:10]

	# pandas table to list
	# 만약 해당 유저가 아직 보지 않은 영화에 대해서, 평점을 예측하고자 한다면?
	# (어떤 유저와 비슷한 정도 * 그 유저가 영화에 대해 부여한 평점) 을 더해서 (유저와 비슷한 정도의 합)으로 나눠보면 됨!
	# index_list 는 비슷한 유저의 id 값 리스트 / weight_list 는 비슷한 유저와의 유사도 리스트
	
    user_index_list = user_based_collab[userid].sort_values(ascending=False)[:10].index.tolist()
    user_weight_list = user_based_collab[userid].sort_values(ascending=False)[:10].tolist()

    store_list = []

    for i in recommand_list:
        try:
            store = Food.objects.get(store=i)
        except:
            pass
        store_list.append(store)

    star_result = []
	#위에 10개의 상점을 돌면서 현재 유저가 부여될 평점을 예측	
    for i in store_list:
        try:
            store = i.store
        except:
            pass
        weighted_sum = []
        weighted_user = []
        for i in range(1, 10):
            # 해당 상점에 평점을 부여한 사람들의 유사도와 평점만 추가 (즉, 0이 아닌 경우에만 계산에 활용)
            if int(title_user[store][user_index_list[i]]) != 0:
                # 평점 * 유사도 추가
                weighted_sum.append(title_user[store][user_index_list[i]] * user_weight_list[i])
                # 유사도 추가
                weighted_user.append(user_weight_list[i])

        # 총 평점*유사도 / 총 유사도를 토대로 평점 예측
        result = sum(weighted_sum)/sum(weighted_user)

        star_result.append(result)

        dolchu = []

    for i,x in zip(store_list, star_result):
        dolchu_data = {
            'id': i.id,
            'store': i.store,
            'img': i.img,
            'address': i.address,
            'star': x,
        }
        dolchu.append(dolchu_data)
        dolchu.sort(key=lambda x: x['star'], reverse=True)

    return render(request, 'food/recommand.html',{'dolchu' : dolchu, 'store_list':store_list, 'star_result':star_result, 'categories1':categories1,'categories2':categories2,'best_food':best_food})