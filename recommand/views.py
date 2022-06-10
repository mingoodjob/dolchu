import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from django.shortcuts import render, redirect
from food.models import Food, Comment,Category
from user.models import UserModel
from django.contrib.auth.decorators import login_required

def recommand(request):
    userid = request.user.id
    comment = Comment.objects.filter(username=userid)
    if not comment:
        return render(request, 'food/recommand.html', {'message': '평점을 남겨주세요'})


    rating = pd.read_csv('user_rating.csv')
    store = pd.read_csv('store_info.csv')

	# movieId를 기준으로 ratings 와 movies 를 결합함
    store_ratings = pd.merge(rating, store, on='store')

	# user별로 영화에 부여한 rating 값을 볼 수 있도록 pivot table 사용
    title_user = store_ratings.pivot_table('rating', index='userid', columns='store')

	# 평점을 부여안한 영화는 그냥 0이라고 부여
    title_user = title_user.fillna(0)

	# 유저 1~610 번과 유저 1~610 번 간의 코사인 유사도를 구함
    user_based_collab = cosine_similarity(title_user, title_user)

	# 위는 그냥 numpy 행렬이니까, 이를 데이터프레임으로 변환
    user_based_collab = pd.DataFrame(user_based_collab, index=title_user.index, columns=title_user.index)

	# 1번 유저와 가장 비슷한 266번 유저를 뽑고,
    user = user_based_collab[userid].sort_values(ascending=False)[:10].index[1]
	# 266번 유저가 좋아했던 영화를 평점 내림차순으로 출력
    recommand_store = title_user.query(f"userid == {user}").sort_values(ascending=False, by=user, axis=1)
    recommand_list = recommand_store.columns.tolist()[:10]

    store_list = []

    for i in recommand_list:
        store = Food.objects.get(store=i)
        store_list.append(store)


    		
	# pandas table to list
	# 만약 해당 유저가 아직 보지 않은 영화에 대해서, 평점을 예측하고자 한다면?
	# (어떤 유저와 비슷한 정도 * 그 유저가 영화에 대해 부여한 평점) 을 더해서 (유저와 비슷한 정도의 합)으로 나눠보면 됨!
	# index_list 는 비슷한 유저의 id 값 리스트 / weight_list 는 비슷한 유저와의 유사도 리스트
	
    user_index_list = user_based_collab[userid].sort_values(ascending=False)[:10].index.tolist()
    user_weight_list = user_based_collab[userid].sort_values(ascending=False)[:10].tolist()

		# 1번 유저가 다크나이트를 보고 어떤 평점을 부여할지 예측
    store = '남양수산'
    weighted_sum = []
    weighted_user = []
    for i in range(1, 10):
        # 해당 영화를 보고 평점을 부여한 사람들의 유사도와 평점만 추가 (즉, 0이 아닌 경우에만 계산에 활용)
        if int(title_user[store][user_index_list[i]]) != 0:
            # 평점 * 유사도 추가
            weighted_sum.append(title_user[store][user_index_list[i]] * user_weight_list[i])
            # 유사도 추가
            weighted_user.append(user_weight_list[i])

    # 총 평점*유사도 / 총 유사도를 토대로 평점 예측
    result = sum(weighted_sum)/sum(weighted_user)

    categoies = Category.objects.all()

    return render(request, 'food/recommand.html',{'store_list':store_list, 'result':result, 'categoies':categoies})