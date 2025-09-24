from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login
from .forms import Register,Auth,Chatmessagecreateform
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from django.contrib.auth.decorators import login_required

# Create your views here.
def registration(request):
    if request.method=='POST':
        form=Register(request.POST)
        if form.is_valid():
          user=form.save()
          login(request, user) 
          return redirect(bodymessage)
    else:
       form=Register()    
    return render(request,'accounts/register.html',{'form':form})





def loginuser(request):
   if request.method=='POST':
      form=Auth(request=request,data=request.POST)
      if form.is_valid():
         user=form.get_user()
         login(request,user)
         return redirect(bodymessage)
   else:
        form = Auth()
   return render(request, "accounts/Login.html", {'form': form})



@login_required
def bodymessage(request):
    chat_group = get_object_or_404(Chatgroup, group_name="public-chat")
    if request.htmx:
        form = Chatmessagecreateform(request.POST)
        print("POST data:", request.POST)    
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            # don't redirect — re-render with fresh form+messages
            print("Saved message id:", message.pk) 
            context={
                'message':message,
                'user':request.user
            }

            return render(request,'accounts/partial/chatnew.html',context)
        else:
            print("FORM INVALID:", form.errors)   
    else:
        form = Chatmessagecreateform()

        messages = chat_group.chat_messages.all()[:30]
    return render(request, "accounts/chat.html", {'messages': messages,'form': form,})


