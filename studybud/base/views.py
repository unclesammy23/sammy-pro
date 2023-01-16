from django.shortcuts import render, redirect
from .models import Room, Topic
from .forms import RoomFrom
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import  login, logout, authenticate




def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'user does not exist')

        user = authenticate(request,username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')


    context ={}
    return render(request, 'base/login_register.html',context)

#just commit something


def home(request):

    q = request.GET.get('q') if request.GET.get('q') != None else '' 

    rooms = Room.objects.filter(
            Q(topic__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q)
            )

    topic = Topic.objects.all()
    room_count = rooms.count()

    context={'rooms':rooms, 'topics': topic, 'room_count':room_count}
    return render(request,'base/home.html',context)



def room(request,  pk):
    room = Room.objects.get(id=pk)
    return render(request,'base/room.html',{'room':room})


def createRoom(request):
    form = RoomFrom()
    if request.method == 'POST':
        form = RoomFrom(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')


    context ={'form':form} 

    return render(request,'base/room_form.html',context)

def updateRoom(request,pk):
    room =Room.objects.get(id=pk)
    form = RoomFrom(instance=room)

    if request.method == 'POST':
        form = RoomFrom(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')


    context = {'form':form}
    return render(request, 'base/room_form.html',context)

def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj':room})