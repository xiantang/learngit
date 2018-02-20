from django.shortcuts import render,get_object_or_404,redirect
from .models import Board, User, Topic,Post
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


def new_topic(request,pk):
    board = get_object_or_404(Board,pk=pk)  #如果网页不存在跳出404
    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']

        user = User.objects.first()

        topic = Topic.objects.create(
            subject=subject,
            board=board,
            starter=user
        )

        post = Post.objects.create(
            message=message,
            topic=topic,  #外来键
            created_by=user
        )

        return redirect('board_topics', pk=board.pk)  #add to topicpage

    return render(request,'new_topic.html',{'board': board})


