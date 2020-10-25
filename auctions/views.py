from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, List, WatchList, Comments, Bid
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required

from .models import User
from datetime import date


def index(request):
    current_user=request.user
    if request.method == "POST" :
        title = request.POST["title"]
        bid = request.POST["bid"]
        photo_url= request.POST["photo"]
        description= request.POST["description"]
        category=request.POST["cat"]
        #isactive=request.POST["Isactive"]
        today=date.today()
        d=today.strftime("%B %d, %Y")
        data=List()
        data.date=d
        data.title=title
        data.bid=bid
        data.category=category
        data.photo_url=photo_url
        data.description=description
        data.created=current_user.username
        data.isactive=1
        data.save()
    current_user=request.user
    ob=List.objects.raw('select * from auctions_list where  auctions_list.isactive=1 and auctions_list.id not in(select title_id from auctions_watchlist where auctions_watchlist.user_id=%s)',[current_user.id])
    return render(request, "auctions/index.html", {
        "list":ob
         })
    return render(request, "auctions/index.html")
@login_required
def create(request):
   return render(request, "auctions/create.html")
def active_list(request):
    current_user=request.user
    if request.method == "POST" :
        title = request.POST["title"]
        bid = request.POST["bid"]
        photo_url= request.POST["photo"]
        description= request.POST["description"]
        category=request.POST["cat"]
        #isactive=request.POST["Isactive"]
        today=date.today()
        d=today.strftime("%B %d, %Y")
        data=List()
        data.date=d
        data.title=title
        data.bid=bid
        data.category=category
        data.photo_url=photo_url
        data.description=description
        data.created=current_user.username
        data.isactive=1
        data.save()
    current_user=request.user
    ob=List.objects.raw('select * from auctions_list where  auctions_list.isactive=1 and auctions_list.id not in(select title_id from auctions_watchlist where auctions_watchlist.user_id=%s)',[current_user.id])
    return render(request, "auctions/active_list.html", {
        "list":ob
         })
@login_required
def item(request,name):
     title = name
     bidd=""
     close=False
     user=""
     current_user=request.user
     for p in List.objects.raw('select * from auctions_list where auctions_list.title = %s',[title]):
             idd=p.id
             user=p.created
     ob3=List.objects.raw('select * from auctions_list where auctions_list.isactive = 1')
     if(current_user.username==user):
         close=True
     ob=Comments.objects.filter(list_id=idd,user_id=current_user.id)
     ob1=Bid.objects.filter(list_id=idd)
     for m in ob1:
        bidd=m.current_bid
     return render(request, "auctions/item.html",{
        "list":ob3,
        "comments":ob,
        "title":title,
        "bidd":bidd,
        "close":close
        })
def categories(request):
    return render(request, "auctions/categories.html")
def category(request,name):
    ob=List.objects.raw('select * from auctions_list where auctions_list.isactive=1 and auctions_list.category= %s',[name])
    return render(request, "auctions/category.html", {
        "list":ob,
        "category":name
        })
@login_required
def comments(request):
    title=""
    close=False
    current_user=request.user
    user=""
    for l in List.objects.raw('select * from auctions_list where auctions_list.title = %s',[title]):
             idd=l.id
             user=l.created
    if request.method == 'POST':
        comment=request.POST["comments"]
        title = request.POST['t']
        dat=Comments()
        dat.comments=comment
        for p in List.objects.raw('select * from auctions_list where auctions_list.title = %s',[title]):
             idd=p.id
        dat.title_id=idd
        dat.user_id=current_user.id
        dat.list_id=idd
        dat.save()
    for p in List.objects.raw('select * from auctions_list where auctions_list.title = %s',[title]):
        idd=p.id
    ob1=Comments.objects.filter(list_id=idd,user_id=current_user.id)
    ob2=Bid.objects.filter(list_id=idd)
    for m in ob2:
        bidd=m.current_bid
    if(current_user.username==user):
         close=True
    close=True
    return render(request, "auctions/comments.html",{
        "list":List.objects.all,
        "comments":ob1,
        "title":title,
        "bidd":bidd,
        "close":close
        })   
@login_required
def watchlist(request):
    title=""
    close=False
    current_user=request.user
    user="" 
    if request.method == 'POST':
        title = request.POST['t']
    for p in List.objects.raw('select * from auctions_list where auctions_list.title = %s',[title]):
        idd=p.id
        user=p.created
    data=WatchList()
    data.user_id=current_user.id
    data.title_id=idd
    data.save()
    ob1=Comments.objects.filter(list_id=idd,user_id=current_user.id)
    ob2=List.objects.raw('select * from auctions_list where auctions_list.isactive=1')
    if(current_user.username==user):
         close=True
    return render(request, "auctions/watchlist.html",{
        "list":ob2,
        "comments":ob1,
        "title":title,
        "close":close
        })   
@login_required
def showwatchlist(request):
    current_user=request.user
    ob=List.objects.raw('select * from auctions_list,auctions_watchlist where auctions_watchlist.user_id= %s and auctions_list.isactive=1 and auctions_list.id=auctions_watchlist.title_id',[current_user.id])
    return render(request, "auctions/showwatchlist.html",{
        "list":ob
    })
@login_required
def removeWatchlist(request):
    title=""
    current_user=request.user
    if request.method == 'POST':
        title = request.POST['t']
    for p in List.objects.raw('select * from auctions_list where auctions_list.title = %s',[title]):
        idd=p.id
    WatchList.objects.filter(title_id=idd,user_id=current_user.id).delete()
    ob=List.objects.raw('select * from auctions_list,auctions_watchlist where auctions_watchlist.user_id= %s and auctions_list.isactive=1 and auctions_list.id=auctions_watchlist.title_id',[current_user.id])
    return render(request, "auctions/showwatchlist.html",{
        "list":ob
        })   
@login_required
def bid(request):
    #start_bid=""
    bidd=""
    current_user=request.user
    check_id=0
    message=""
    close=False
    user=""
    if request.method == 'POST':
        title = request.POST['t']
        madebid=int(request.POST['bid'])
    for p in List.objects.raw('select * from auctions_list where auctions_list.title = %s',[title]):
        start_bid=p.bid
        listt_id=p.id
        user=p.created
    for k in Bid.objects.raw('select * from auctions_bid where auctions_bid.list_id=%s',[listt_id]):
        check_id=k.list_id
        current_bid=k.current_bid
    if(check_id != listt_id):
            if(madebid>start_bid):
                b = Bid(user_id=current_user.id,current_bid=madebid,list_id=listt_id)
                b.save()
                message="your bid placed successfully"
            else:
                message="your bid should be grater than starting bid"
          
    else:
           if(current_bid<madebid):
               Bid.objects.filter(list_id=listt_id).update(current_bid=madebid)
               message="your bid placed successfully"
           else:
                 message="your bid should be grater than current bid"   
    ob=Comments.objects.filter(list_id=listt_id,user_id=current_user.id)
    ob1=Bid.objects.filter(list_id=listt_id)
    for m in ob1:
      bidd=m.current_bid
    if(current_user.username==user):
         close=True
    return render(request, "auctions/makingbid.html",{
        "list":List.objects.all,
        "comments":ob,
        "title":title,
        "bidd":bidd,
        "message":message,
        "close":close
        })   
@login_required
def close(request):
    title=""
    current_user=request.user
    if request.method == 'POST':
        title = request.POST['t']
    
    for p in List.objects.raw('select * from auctions_list where auctions_list.title = %s',[title]):
        idd=p.id
    List.objects.filter(id=idd).update(isactive=0)
    ob2=Bid.objects.raw('select * from auctions_bid where auctions_bid.list_id=%s',[idd])
    for l in ob2:
        current_bid=l.current_bid
        user_id=l.user_id
    ob3=User.objects.raw('select * from auctions_user where  auctions_user.id=%s',[user_id])
    for u in ob3:
        username=u.username
    ob1=Comments.objects.filter(list_id=idd,user_id=current_user.id)
    return render(request, "auctions/closelist.html",{
        "list":List.objects.all,
        "comments":ob1,
        "title":title,
        "current_bid":current_bid,
        "username":username
        })     
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
