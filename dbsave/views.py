from django.http import HttpResponse
from django.shortcuts import render, redirect
from requests import request
from food.models import Food, Comment, Category
from user.models import UserModel
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.decorators import admin_required
from django.db.models import Avg
from django.db.models import Q
import requests
from bs4 import BeautifulSoup
from time import sleep
import random,string

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
	category_num = 8
	result = food_switch(category_num)
	# food_list = listparsing(result,2)
	for cate in range(8):
		result = food_switch(cate+1) 
		for i in range(5):
			food_list = listparsing(result,i+1)
			for food in food_list:
				try:
					store, address, img, tel, price, parking, close = storeparsing(food)
					category = Category.objects.get(id=category_num)
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




