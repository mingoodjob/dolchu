from django.http import HttpResponse
from django.shortcuts import render, redirect
from requests import request
from food.models import Food, Comment, Category
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.decorators import admin_required
from django.db.models import Avg
from django.db.models import Q
import requests
from bs4 import BeautifulSoup

def listparsing(page):
    
	url = f'https://www.mangoplate.com/search/%EC%A0%9C%EC%A3%BC%EB%8F%84%20%EB%A7%9B%EC%A7%91?keyword=%EC%A0%9C%EC%A3%BC%EB%8F%84%20%EB%A7%9B%EC%A7%91&page={page}'

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

	for row in rows:
		cols = row.find_all('td')
		cols = [ele.text.strip() for ele in cols]
		data.append(cols)
		
	img = soup.select('.restaurant-photos-item')

	imgs = []

	for i in img:
		alt = i.img['alt']
		img = alt.split(' 사진 - ')
		store = img[0]
		address = img[1]
		img = i.img['src']
		imgs.append(i.img['src'])

	tel = data[1][0]
	price = data[3][0]
	try:
		parking = data[4][0]
	except:
		parking = ''
	try:	
		close = data[5][0]
	except:
		close = ''
	
	return store, address, img, tel, price, parking, close 

# @admin_required
def dbsave(request):
	linklists = listparsing(8)
	for linklist in linklists:
		store_info = storeparsing(linklist)
		category = Category.objects.get(id=8)
		Food.objects.create(store=store_info[0],address=store_info[1],img=store_info[2],tel=store_info[3],price=store_info[4],parking=store_info[5],close=store_info[6],category=category)
     
	return HttpResponse("<h1>dbsave!</h1>")