from  django . shortcuts  import  render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from todoapp import models
from todoapp.models import TODO
from django.contrib.auth.decorators import login_required

@login_required(login_url='/loginn')
def home(request):
    return render(request, 'signup.html')


def signup(request):
    if request.method == 'POST':
        fnm=request.POST.get('fnm')
        emailid=request.POST.get('emailid')
        pwd=request.POST.get('pwd')
        print(fnm,emailid,pwd)
        my_user=User.objects.create_user(fnm,emailid,pwd)
        my_user.save()
        return redirect('/loginn')
    
    return render(request, 'signup.html')


def loginn(request):
    if request.method == 'POST':
        fnm=request.POST.get('fnm')
        pwd=request.POST.get('pwd')
        print(fnm,pwd)
        userr=authenticate(request,username=fnm,password=pwd)
        if userr is not None:
            login(request,userr)
            return redirect('/todopage')
        else:
            return redirect('/loginn/', skip_redirect='True')
               
    return render(request, 'loginn.html')

@login_required(login_url='/loginn')

def todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        print(title)
        obj =models.TODO(title=title, user=request.user)  # Use the imported TODO model
        obj.save()
        user = request.user        
        res =models.TODO.objects.filter(user=user).order_by('-date')  # Use the imported TODO model
        return redirect('/todopage', {'res': res})
    
    res =models.TODO.objects.filter(user=request.user).order_by('-date')  # Use the imported TODO model
    return render(request, 'todo.html', {'res': res})

def delete_todo(request,srno):
    print(srno)
    obj=models.TODO.objects.get(srno=srno)
    obj.delete()
    return redirect('/todopage')

@login_required(login_url='/loginn')

def edit_todo(request, srno):
    if request.method == 'POST':
        title = request.POST.get('title')
        print(title)
        obj = models.TODO.objects.get(srno=srno)
        obj.title = title
        obj.save()
        return redirect('/todopage')

    obj = models.TODO.objects.get(srno=srno)
    return render(request, 'edit_todo.html', {'obj': obj})


def signout(request):
    logout(request)
    return redirect('/loginn')