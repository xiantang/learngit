from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Board
def home(request):
    # return HttpResponse('Hello, World!')
    boards=Board.objects.all()#从数据库里面获取所有的版块对象
    return render(request,'home.html',{'boards':boards})