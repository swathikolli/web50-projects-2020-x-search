from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass
class List(models.Model):
    categories=[("Home","Home"),("Education","Education"),("Health","Health"),("Fashion","Fashion"),("Sports","Sports"),("Automobile","Automobile")]
    title=models.CharField(max_length=64)
    bid=models.IntegerField()
    category=models.CharField(max_length=64, choices=categories,default=None)
    photo_url=models.CharField(max_length=20000)
    description=models.CharField(max_length=100)
    date=models.CharField(max_length=50)
    created=models.CharField(max_length=200)
    isactive=models.IntegerField(default=1)
    def __str__(self):
        return f"{self.id} {self.title} {self.bid}"
class Bid(models.Model):
    list=models.ForeignKey("auctions.List",on_delete=models.CASCADE,related_name="list_bid",blank=True,null=True)
    user=models.ForeignKey("auctions.User", on_delete=models.CASCADE,related_name="user_bid")
    current_bid=models.IntegerField()
    def __str__(self):
        return f"{self.id} {self.list_id} {self.current_bid}" 
class WatchList(models.Model):
    title=models.ForeignKey(List,on_delete=models.CASCADE,related_name="watchlist",blank=True,null=True)
    user = models.ForeignKey("auctions.User", related_name='user_watchlist',on_delete=models.CASCADE)
class Comments(models.Model):
    comments=models.CharField(max_length=10000)
    title=models.ForeignKey(List,on_delete=models.CASCADE,related_name="comments",blank=True,null=True)
    list=models.ForeignKey(List,on_delete=models.CASCADE,related_name="list_comments",blank=True,null=True)
    user=models.ForeignKey("auctions.User",on_delete=models.CASCADE,related_name="user_comments",blank=True,null=True)
    def __str__(self):
        return f"{self.comments}" 


    
