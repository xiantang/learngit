from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Board
from django.http import Http404

def home(request):
    # return HttpResponse('Hello, World!')
    boards=Board.objects.all()#从数据库里面获取所有的版块对象
    return render(request,'home.html',{'boards':boards})

def board_topics(request, pk):
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:  #we want show 404 not 500
        raise Http404
    return render(request, 'topics.html', {'board': board})
#
# def about(request):
#     return render(request,'about.html')
#
#
# def about_company(request):
#     return render(request,'about_company.html',{'company_name':'Simple Complex'})