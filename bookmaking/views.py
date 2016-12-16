from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import User1,  Horse, Stake, Ride
from .forms import RegForm, LoginForm, UserForm, User1Form, MakeStake
from django.views import View
from pip._vendor import requests
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse


@login_required(login_url='/login')
def user_view(request):
    users = User1.objects.all()
    return render(request, 'bookmaking/users.html', {'users': users})


@login_required(login_url='/login')
def horses_list(request):
    horses = Horse.objects.all()
    page = request.GET.get('page')
    paginator = Paginator(horses, 5)
    try:
        horses= paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        horses = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        horses = paginator.page(paginator.num_pages) 
    return render (request, 'bookmaking/horses_list.html', {'horses': horses})


def log_out(request):
    logout(request)
    return redirect("/")


@login_required(login_url='/login')
def edit_user(request, pk):
        us1 = get_object_or_404(User1, pk=pk)
        if request.method == "POST":
            form = UserForm(request.POST, instance=request.user)
            form1 = User1Form(request.POST, request.FILES, instance=us1)
            if form.is_valid() and form1.is_valid():
                user = form.save(commit=False)
                user1 = form1.save(commit=False)
                user.save()
                user1.user = user
                form1.save()
                form.save_m2m()
                form1.save_m2m()
                return redirect('user_detail', pk=user.pk)
        else:
            form = UserForm(instance=request.user)
            form1 = User1Form(instance=us1)
        return render(request, 'bookmaking/edit_user.html', {'form': form, 'form1': form1})


@login_required(login_url='/login') 
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    user1 = get_object_or_404(User1, pk=pk)
    stakes = Stake.objects.filter(user=pk)
    kol_stakes = len(stakes)
    return render(request, 'bookmaking/user_detail.html', {'user': user, 'user1': user1, 'stakes':stakes, 'kol_stakes':kol_stakes})


@login_required(login_url='/login')
def make_stake(request):
    if request.method == "POST":
        stake_form = MakeStake(request.POST)
        if stake_form.is_valid():
            stake = stake_form.save(commit=False)
            stake.user_id = request.user.id
            stakes = Stake.objects.filter(horse=stake.horse_id, user=stake.user_id)
            if stakes:
                errors = 'Вы уже поставили на эту лошадь'
                return render(request, 'bookmaking/make_stake.html', {'stake_form': stake_form, 'errors': errors})
            else:
                stake.save()
                stake_form.save()
                stake_form.save_m2m()
            return redirect('user_detail', pk=request.user.id)
    else:
        stake_form = MakeStake(request.POST)
    return render(request, 'bookmaking/make_stake.html', {'stake_form': stake_form})

    # form = MakeStake1(request.POST)
    # if not form.is_valid():
    #     return render(request, 'bookmaking/make_stake.html', {'errors': '', 'form': form.as_p()})
    # #horse = Horse.objects.filter(name=form.cleaned_data['horse_name'])
    # horse = Horse(name=form.cleaned_data['horse_name'])
    # us=request.user
    # stake = Stake(size=form.cleaned_data['stake_size'], horse=horse.horse_id, user=us.id)
    # stake.save()
    # return redirect('user_detail', pk=us.id)


def rides_list(request):
    rides = Ride.objects.all()
    return render(request, 'bookmaking/rides_list.html', {'rides': rides})


def ride_detail(request, pk):
    ride = get_object_or_404(Ride, pk=pk)
    horses = Horse.objects.filter(ride__ride_id=pk)
    return render(request, 'bookmaking/ride_detail.html', {'horses': horses, 'ride':ride})


@login_required(login_url='/login')
def stake_remove(request, pk):
    stake = get_object_or_404(Stake, pk=pk)
    user_pk = stake.user.id
    stake.delete()
    return redirect('user_detail', pk=user_pk)


@login_required(login_url='/login')
def horse_detail(request, pk):
    horse = get_object_or_404(Horse, pk=pk)
    return render(request, 'bookmaking/horse_detail.html', {'horse': horse})


@login_required(login_url='/login') 
def main_page(request):
    return render(request, 'bookmaking/main_page.html', {})


class Registration(View):
    def get(self, request):
        form = RegForm()
        return render(request, 'bookmaking/registration2.html', {'errors': '', 'form': form.as_p()})
   
    def post(self, request):
        form = RegForm(request.POST)  
        if not form.is_valid():
            return render(request, 'bookmaking/registration2.html', {'errors': '', 'form': form.as_p()}) 
        us = User(username=form.cleaned_data['username1'], email=form.cleaned_data['email'], last_name=form.cleaned_data['surname'], first_name=form.cleaned_data['name'])
        us.set_password(form.cleaned_data['password'])
        us.save(form.cleaned_data['username1'])
        user = authenticate(username=form.cleaned_data['username1'], password=form.cleaned_data['password'])
        us1 = User1(user_id=us.id)
        us1.save()
        login(request, user)    
        return redirect('/')   
    
# class Login (View):
#      def get(self,request):
#          return render(request, 'bookmaking/login.html', {'errors':'', 'username':''})
#
#      def post(self, request):
#          username1 = request.POST['username']
#          password = request.POST['password']
#          errors = []
#
#          user = authenticate(username=username1, password=password)
#
#          if user is not None:
#              login(request, user)
#              return redirect('/')
#          errors.append('Логин или пароль неверны')
#          return render(request, 'bookmaking/login.html', {'errors': mark_safe('<br>'.join(errors)), 'username': username1})


def log_in(request):    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            if form.get_user():
                login(request, form.get_user())
                return redirect('/')           
    else:
        form = LoginForm()
    return render(request, 'bookmaking/login2.html', {'form': form.as_p()})