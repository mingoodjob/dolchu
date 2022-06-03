from django.shortcuts import render

# Create your views here.

def main_view(request):
    return render(request, 'food/main.html')

def detail_view(request):
    return render(request, 'food/detail.html')

