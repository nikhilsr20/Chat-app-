from django.db import models
from django.contrib.auth.models import User
# Create your models here.



# this model is for the creating a connection between two
class Chatgroup(models.Model):

    group_name=models.CharField(max_length=128,unique=True)

    def __str__(self):
        return self.group_name
    

#this model is for showing related messages to a group 
class Groupmessages(models.Model):
    group=models.ForeignKey(Chatgroup,related_name='chat_messages',on_delete=models.CASCADE) 
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    body=models.CharField(max_length=300)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username}:{self.body}'
    
    class Meta:
        ordering=['created']