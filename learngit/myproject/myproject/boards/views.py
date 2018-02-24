from django.shortcuts import render,get_object_or_404,redirect
from .models import Board, User, Topic,Post
from django.http import Http404
from .forms import NewTopicForm


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


def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('board_topics', pk=board.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})
