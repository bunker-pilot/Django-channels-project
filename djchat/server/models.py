from django.db import models
from django.conf import settings
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank =True , null= True)

    def __str__(self):
        return self.name 

class Server(models.Model):
    name = models.CharField(max_length=150)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="servers_owned" ,on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name="servers", on_delete=models.DO_NOTHING)
    description = models.TextField(max_length=250, null=True, blank=True)
    member = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name


class Channel(models.Model):
    name = models.CharField(max_length=150)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="channels", on_delete=models.CASCADE)
    server = models.ForeignKey(Server, related_name="channels", on_delete=models.CASCADE)
    

    def __str__(self):
        return self.name

    