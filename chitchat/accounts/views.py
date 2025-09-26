from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login
from .forms import Register,Auth,Chatmessagecreateform
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

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

    if request.method == "POST":
        form = Chatmessagecreateform(request.POST)
        print("POST data:", request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            print("Saved message id:", message.pk)

            # detect HTMX
            is_htmx = getattr(request, "htmx", False) or request.headers.get("HX-Request") == "true"

            if is_htmx:
                # return only the fragment for the single message
                html = render_to_string("accounts/partial/chatnew.html",
                                        {"message": message, "user": request.user},
                                        request=request)
                return HttpResponse(html, status=200)
            return HttpResponseRedirect(request.path)

    # GET: show messages oldest -> newest so that hx-swap="beforeend" appends at bottom
    form = Chatmessagecreateform()
    messages = chat_group.chat_messages.all().order_by('created')[:300]  # adjust limit as needed
    return render(request, "accounts/chat.html", {"messages": messages, "form": form})