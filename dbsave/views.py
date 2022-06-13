from django.http import HttpResponse
from django.shortcuts import render, redirect
from food.models import Food, Comment, Category, Travel
from user.models import UserModel
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.db.models import Q
from bs4 import BeautifulSoup
import requests,random,string


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
	good_comment = ['너무 맛있어요! 꼭 다시 방문할게요','재방문 각이네요ㅠㅠ 존맛탱','너무 맛있어서 여행가는 지인에게 추천했어요 ㅎㅎ','이번 여행에서 여기가 제일 맛있었습니다♡ 돌아가서 생각날 것 같아요!','정말 맛있어요! 추천합니다','사장님도 친절하시고 가게 쾌적하고 음식도 맛있어요 최고','무조건 재방문 할겁니다 맛있게 잘 먹었어요','음식이 깔끔하고 정갈합니다','가게 분위기도 너무 좋고 음식도 맛있어요','여기 방문한 건 최고의 선택..♡잘했다 나','정말 맛있어요 완전 추천!!!!!!','만족스럽게 잘 먹었습니다','전반적으로 다 만족스러운 식당이었어요 ㅎㅎ','쿨타임 차서 다시 방문했습니다 ㅋㅋㅋ 제 단골집이에요','여기 너무 맛있어요! 중독성 대박입니다','존맛탱 ㅠㅠㅠㅠㅠㅠㅠ:흰색_하트:','이 메뉴가 생각난다? 무조건 여기로 방문하시면 됩니다 후회없으실 거예요','왜 집에서 해먹으면 이 맛이 절대 안 날까요.. 사장님 최고...','맛있는데 또 친절해ㅠㅠㅠ 너무 좋아요','집이 서울인데 너무 맛있어서 어떡하죠.. 제주 오면 꼭 다시 들러야겠어요']
	bad_comment = ['불친절하시고 음식도 그닥입니다','별로 맛있는 줄 모르겠네요 저는..','그냥 다른 곳 갈걸 ㅠ','대기가 긴데 그 값을 못하는 집 같아요.. 저는 비추천','조금만 더 친절하셨으면 좋았을 것 같아요','기대했던 거에 비해 맛이 별로네요','그냥 그렇습니다','굳이 시간을 내서 방문할 만한 곳은 아닌 것 같아요','쏘쏘..:찌푸린_얼굴:','먹을 만은 한데 사장님이 불친절하세요','맛이 전반적으로 별로라서 재방문은 안 할 것 같습니다..','가격이 너무 비싸요','주차 공간도 협소하고 대기도 길고 맛도 별로네요.. 완전 실망','기대를 너무 많이 했나봐요ㅠㅠㅠ','다른 리뷰처럼 막 극찬할 정도는 아닙니다','같은 가격이면 다른 곳 가는게 더 나을지도..?','조금만 더 저렴했거나 양이 많았으면 좋았을 거 같아요','전체적으로 음식들이 다 너무 짰어요..','그냥 그랬어요 평범하고 감흥없는 맛','맛은 나쁘진 않은데 양이 아쉽네요']
	
	foods = Food.objects.all()
	users = UserModel.objects.all()
	for food in foods:
		foodid = food.id
		foodid = Food.objects.get(id=foodid)
		for user in users:
			userid = user.id
			userid = UserModel.objects.get(id=userid)
			probability = random.randint(0,1)
			if probability == 1:	
				star = random.randint(1,5)
				if star > 3:
					comment = random.choice(good_comment)
				else: 
					comment = random.choice(bad_comment)
				Comment.objects.create(username=userid, store=foodid, comment=comment, star=star)
			else:
				pass

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

def travel_save(request):
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

	f.write(f'userid,store,rating\n')
	g.write(f'storeid,store\n')

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

def dbpush(request):
	f = open('db.csv', 'r', encoding='utf-8')
	foods = f.readlines()
	for food in foods:
		category = Category.objects.get(id=food.split('@@')[7])
		Food.objects.create(store=food.split('@@')[0], address=food.split('@@')[1], img=food.split('@@')[2], tel=food.split('@@')[3], price=food.split('@@')[4], parking=food.split('@@')[5], close=food.split('@@')[6], category=category)
		
	f.close()

	# f = open('db.csv', 'w', encoding='utf-8')
	# foods = Food.objects.all()
	# # Food.objects.create(store=store, address=address, img=img, tel=tel, price=price, parking=parking, close=close, category=category)
	# for food in foods:
	# 	f.write(f'{food.store}@@{food.address}@@{food.img}@@{food.tel}@@{food.price}@@{food.parking}@@{food.close}@@{food.category.id}\n')

	# f.close()

	return HttpResponse('푸시 끝남')