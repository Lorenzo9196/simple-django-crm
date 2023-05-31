from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

# Create your views here.
def home(request):
    # if loged get records
    records = Record.objects.all()

    # if sending form then validate credentials
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # auth and login
            login(request, user)
            messages.success(request, 'Bienvenido ' + username)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is incorrect')
            return redirect('home')
    else:
        return render(request, 'home.html', {"records": records,})


def logout_user(request):
    logout(request)
    messages.info(request, 'Logged out successfully')
    return redirect('home')
    # return render(request, 'home.html', {})


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # register and login
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Account created for ' + username)
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    return render(request,'register.html', {'form':form})


def customer_record(request, pk):
    if request.user.is_authenticated:
         record = Record.objects.get(id=pk)
         return render(request, 'record.html', {"customer_record": record})
    else:
        messages.error(request, 'You need to login first')
        return redirect('home')


def delete_record(request, pk):

    if request.user.is_authenticated:
         record = Record.objects.get(id=pk)
         record.delete()
         return redirect('home')
    else:
        messages.error(request, 'You need to login first')
        return redirect('home')
        

def add_record(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AddRecordForm(request.POST)
            if form.is_valid():
                add_record = form.save()
                messages.success(request, 'Record added successfully')
                return redirect('home')
        else:
            form = AddRecordForm()
            return render(request, 'add_record.html', {'form':form})
    else:
        messages.error(request, 'You need to login first')
        return render(request,'home.html', {'form':form})


def update_record(request, pk):

    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record updated successfully')
            return redirect('home')
        return render(request, 'update_record.html', {'form':form})
    else:
        messages.error(request, 'You need to login first')
        return redirect('home')

