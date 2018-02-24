from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
def signup(request):
    # form=UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():  # 如果有效
            user = form.save()
            auth_login(request, user)
            return redirect('home')  # 重定向
    else:  # 不是post请求
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})  # 传给我的前端