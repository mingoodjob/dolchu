from sqlite3 import Row
from django.http import HttpResponse
from django.shortcuts import render, redirect
from requests import request
from food.models import Food, Comment, Category, Travel
from user.models import UserModel
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.decorators import admin_required
from django.db.models import Avg
from django.db.models import Q
import requests
from bs4 import BeautifulSoup
import random,string
from selenium import webdriver
from time import sleep
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def listparsing(food_url,page):
    
	url = f'{food_url}{page}'

	headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
	data = requests.get(url,headers=headers)

	soup = BeautifulSoup(data.text, 'html.parser')

	soup = soup.select('.list-restaurant-item')

	linklist = []

	for i in soup:
		linklist.append(i.a['href'])
  
	return linklist

def storeparsing(url):
    
	url = f'https://www.mangoplate.com{url}'

	headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

	data = requests.get(url,headers=headers)

	soup = BeautifulSoup(data.text, 'html.parser')

	table = soup.find('table')
	table_body = table.find('tbody')

	rows = table_body.find_all('tr')

	data = []
	data2 = []

	for row in rows:
		colsth = row.find_all('th')
		colstd = row.find_all('td')
		colstd = [ele.text.strip() for ele in colstd]
		colsth = [ele.text.strip() for ele in colsth]
		data.append(colsth)
		data2.append(colstd)

	try:
		if data[1][0] == '전화번호':
			tel = data2[1][0]
		else:
			tel = ''
	except:
		tel = ''
  
	try:
		if data[3][0] == '가격대':
			price = data2[3][0]
		else:
			price = ''
	except:
		price = ''
  
	try:
		if data[4][0] == '주차':
			parking = data2[4][0]
		else:
			parking = ''
	except:
		parking = ''
  
	try:
		if data[5][0] == '영업시간':
			close = data2[5][0]
		else:
			close = ''
	except:
		close = ''
 
	img = soup.select('.restaurant-photos-item')

	imgs = []

	for i in img:
		alt = i.img['alt']
		img = alt.split(' 사진 - ')
		store = img[0]
		address = img[1]
		img = i.img['src']
		imgs.append(i.img['src'])
	
	return store, address, img, tel, price, parking, close 


def food_switch(argument):
    switcher = {
        1: "https://www.mangoplate.com/search/%EC%A0%9C%EC%A3%BC%EB%8F%84-%ED%95%9C%EC%8B%9D?keyword=%EC%A0%9C%EC%A3%BC%EB%8F%84%20%ED%95%9C%EC%8B%9D&page=",
        2: "https://www.mangoplate.com/search/%EC%A0%9C%EC%A3%BC%EB%8F%84-%EC%A4%91%EC%8B%9D?keyword=%EC%A0%9C%EC%A3%BC%EB%8F%84%20%EC%A4%91%EC%8B%9D&page=",
        3: "https://www.mangoplate.com/search/%EC%A0%9C%EC%A3%BC%EB%8F%84-%EC%9D%BC%EC%8B%9D?keyword=%EC%A0%9C%EC%A3%BC%EB%8F%84%20%EC%9D%BC%EC%8B%9D&page=",
        4: "https://www.mangoplate.com/search/%EC%A0%9C%EC%A3%BC%EB%8F%84-%EC%96%91%EC%8B%9D?keyword=%EC%A0%9C%EC%A3%BC%EB%8F%84%20%EC%96%91%EC%8B%9D&page=",
        5: "https://www.mangoplate.com/search/%EC%A0%9C%EC%A3%BC%EB%8F%84-%EC%84%B8%EA%B3%84%EC%9D%8C%EC%8B%9D?keyword=%EC%A0%9C%EC%A3%BC%EB%8F%84%20%EC%84%B8%EA%B3%84%EC%9D%8C%EC%8B%9D&page=",
        6: "https://www.mangoplate.com/search/%EC%A0%9C%EC%A3%BC%EB%8F%84-%EB%B7%94%ED%8E%98?keyword=%EC%A0%9C%EC%A3%BC%EB%8F%84%20%EB%B7%94%ED%8E%98&page=",
        7: "https://www.mangoplate.com/search/%EC%A0%9C%EC%A3%BC%EB%8F%84-%EC%B9%B4%ED%8E%98?keyword=%EC%A0%9C%EC%A3%BC%EB%8F%84%20%EC%B9%B4%ED%8E%98&page=",
        8: "https://www.mangoplate.com/search/%EC%A0%9C%EC%A3%BC%EB%8F%84-%EC%A3%BC%EC%A0%90?keyword=%EC%A0%9C%EC%A3%BC%EB%8F%84%20%EC%A3%BC%EC%A0%90&page=",
    }
 
    return switcher.get(argument, "nothing")


# @admin_required
def dbsave(request):
	catenum = 0
	for cate in range(8):
		catenum = catenum + 1
		result = food_switch(catenum) 
		for i in range(5):
			food_list = listparsing(result,i+1)
			for food in food_list:
				try:
					store, address, img, tel, price, parking, close = storeparsing(food)
					category = Category.objects.get(id=catenum)
					Food.objects.create(store=store, address=address, img=img, tel=tel, price=price, parking=parking, close=close, category=category)
				except:
					pass
		
	return HttpResponse("<h1>dbsave!</h1>")

def random_review(reqeust):
	commentlist = ['맛없습니다','맛있습니다','최고입니다','별로입니다','다신 먹지 않을게요']
	foods = Food.objects.all()
	users = UserModel.objects.all()
	for food in foods:
		foodid = food.id
		foodid = Food.objects.get(id=foodid)
		for user in users:
			userid = user.id
			userid = UserModel.objects.get(id=userid)
			star = random.randint(1,5)
			comment = random.choice(commentlist)
			Comment.objects.create(username=userid, store=foodid, comment=comment, star=star)

	return HttpResponse("<h1>Random Review!</h1>")

def category_create(request):
	category_list = ['한식','중식','일식','양식','세계음식','뷔페','카페','주점']
	category_icon = ['🍚','🍜','🍣','🍝','🍛','🍽️','🍰','🍺']
	
	for c,i in zip(category_list,category_icon):
		Category.objects.create(category=c, desc=i)

	return HttpResponse("<h1>Category 생성!</h1>")

def user_create(request):
	_LENGTH = 10 # 10자리
	string_pool = string.ascii_lowercase # 소문자
	result = "" # 결과 값
	for k in range(10):
		for i in range(_LENGTH):
			result += random.choice(string_pool) # 랜덤한 문자열 하나 선택
		UserModel.objects.create_user(username=result, password=result)
		result = ''
		
	
	return HttpResponse("<h1>User 생성!</h1>")

def star_avg(request):
	result = 0
	foods = Food.objects.all()
	for food in	foods:
		comment = Comment.objects.filter(store=food.id)
		store = Food.objects.get(id=food.id)
		for cm in comment:
			result = result + cm.star
			store.staravg = result / len(comment)
			store.save()
		result = 0
		

	return HttpResponse("<h1>Star Avg!</h1>")

def travel(request):

	lists = []

	address = Food.objects.all().order_by('address')
	for i in address:
		add = i.address.split(' ')
		add = add[2]
		lists.append(add)
	
	result = list(set(lists))

	return HttpResponse(f'{result}')


def travel_create(request):

# address = ['우도면', '표선면', '이도이동', '도두이동', '서홍동', '색달동', '용담일동', '남원읍', '노형동', '강정동', '월평동', '서귀동', '구좌읍', '회수동', '애월읍', '용담이동', '중문동', '한경면', '이호이동', '일도이동', '호근동', '일도일동', '삼도일동', '동홍동', '아라일동', '대포동', '건입동', '외도이동', '오라일동', '연동', '한림읍', '회천동', '신효동', '보목동', '안덕면', '서호동', '대정읍', '삼양일동', '이도2동', '하예동', '성산읍', '도남동', '하효동', '이도일동', '도평동', '아라이동', '상효동', '용담삼동', '영평동', '법환동', '오라이동', '상예동', '조천읍', '삼양이동', '외도일동', '삼도이동']
	address = ['우도면', '표선면', '이도이동', '도두이동', '서홍동', '색달동', '용담일동', '남원읍', '노형동', '강정동', '월평동', '서귀동', '구좌읍', '회수동', '애월읍', '용담이동', '중문동', '한경면', '이호이동', '일도이동', '호근동', '일도일동', '삼도일동', '동홍동', '아라일동', '대포동', '건입동', '외도이동', '오라일동', '연동', '한림읍', '회천동', '신효동', '보목동', '안덕면', '서호동', '대정읍', '삼양일동', '이도2동', '하예동', '성산읍', '도남동', '하효동', '이도일동', '도평동', '아라이동', '상효동', '용담삼동', '영평동', '법환동', '오라이동', '상예동', '조천읍', '삼양이동', '외도일동', '삼도이동']

	driver = webdriver.Chrome(r"C:\Users\PC\Documents\chromedriver.exe")

	sleep(3)

	for i in address:
		add = f'{i}'
		driver.get(f'https://www.visitjeju.net/kr/search?q={i}')
		driver.implicitly_wait(10)
		sleep(3)
		driver.find_element_by_css_selector('#content > div > div.cont_wrap > div > div.result_box_r > div.sort_wrap > ul > li:nth-child(3) > a').click()
		sleep(3)
		for s in range(3):
			try:
				title = driver.find_element(by='css selector', value=f'#content > div > div.cont_wrap > div > div.result_box_r > div.clear > div.resut_wrap > div > ul > li:nth-child({s+1}) > a > p.item_tit')
				img = driver.find_element(by='css selector', value=f'#content > div > div.cont_wrap > div > div.result_box_r > div.clear > div.resut_wrap > div > ul > li:nth-child({s+1}) > a > img')
				Travel.objects.create(region=add, travel_title=title.text, travel_img=img.get_attribute('src'))
			except:
				pass
			sleep(3)

		return HttpResponse('파싱 끝남')

def travel_save(request):
	# f = open('travel.txt', 'w', encoding='utf-8')
	# travel = Travel.objects.all()
	# for i in travel:
	# 	f.write(i.travel_title+',')
	# 	f.write(i.travel_img+',')
	# 	f.write(i.region+'\n')
	
	f = open('travel.txt', 'r', encoding='utf-8')
	text = f.readlines()
	for i in text:
		data = i.strip().split(',')
		Travel.objects.create(travel_title=data[0], travel_img=data[1], region=data[2])
	f.close()
		
	return HttpResponse('저장 끝남')

def review_load(request):
	f = open('user_rating.csv', 'w', encoding='utf-8')
	g = open('store_info.csv', 'w', encoding='utf-8')

	comment = Comment.objects.all()
	food = Food.objects.all()
	for c in comment:
		userid = UserModel.objects.get(username=c.username)
		store = Food.objects.get(id=c.store.id)
		f.write(f'{userid.id},')
		f.write(f'{store.store},')
		f.write(f'{c.star}\n')

	for h in food:
		g.write(f'{h.id},')
		g.write(f'{h.store}\n')
	
	f.close()
	g.close()

	return HttpResponse('로드 끝남')

def recommand(request):
	userid = request.user.id
	print(userid)

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
		if int(title_user[store][user_index_list[i]]) is not 0:
			# 평점 * 유사도 추가
			weighted_sum.append(title_user[store][user_index_list[i]] * user_weight_list[i])
			# 유사도 추가
			weighted_user.append(user_weight_list[i])

	# 총 평점*유사도 / 총 유사도를 토대로 평점 예측
	result = sum(weighted_sum)/sum(weighted_user)

	return render(request, 'food/list.html',{'store_list':store_list, 'result':result})