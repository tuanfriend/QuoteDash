from django.shortcuts import render, redirect
from .models import *
import bcrypt
from django.contrib import messages

def index(request):
    return render(request, "QuoteApp/login.html")

def signup(request):
    return render(request, "QuoteApp/signup.html")

def regacc(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/signup')
    else:
        f_name = request.POST["firstname"]
        l_name = request.POST["lastname"]
        e_mail = request.POST["reg-email"]
        passw = bcrypt.hashpw(request.POST["reg-pw"].encode(), bcrypt.gensalt())
        User.objects.create(fname=f_name,lname=l_name,email=e_mail,pword=passw)
        user = User.objects.get(email = request.POST['reg-email'])
        request.session['user_id'] = user.id
        request.session['logged'] = True
        messages.success(request, "Successfully Registered!")
        return redirect("/dashboard")

def logacc(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        request.session['logged'] = True
        user = User.objects.get(email = request.POST['log-email'])
        request.session['user_id'] = user.id
        # messages.success(request, 'Successfully loging in...!')
        return redirect('/dashboard')

def logout(request):
    request.session.clear()
    messages.success(request, 'Successfully logout!')
    return redirect('/')

def dashboard(request):
    if request.session['logged'] == False:
        return redirect("/")
    elif request.session['logged'] == True:
        user = User.objects.get(id=request.session['user_id'])
        content = {
            "user": user,
            "allquote": Quotes.objects.all().order_by('-created_at')[:8],
        }
        return render(request, "QuoteApp/quotepg.html", content)

def addquote(request):
    errors = Quotes.objects.quote_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/dashboard')
    else:
        user = User.objects.get(id=request.session['user_id'])
        Quotes.objects.create(user=user, auth=request.POST['auth-form'],quote=request.POST['quo-form'])
        return redirect('/dashboard')

def userpost(request, id):
    user = User.objects.get(id=id)
    allquo = Quotes.objects.filter(user=user).order_by('-created_at')[:5]
    content = {
        "user": User.objects.get(id=request.session['user_id']),
        "allquote": allquo
    }
    return render(request, "QuoteApp/quotepg.html", content)

def editacc(request):
    if request.session['logged'] == False:
        return redirect("/")
    elif request.session['logged'] == True:
        user = User.objects.get(id=request.session['user_id'])
        content = {
            "user": user
        }
    return render(request, "QuoteApp/edituser.html", content)

def btedit(request,id):
    print(request.POST)
    errors = User.objects.update_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/editacc')
    else:
        user = User.objects.get(id=id)
        user.fname = request.POST['up-fname']
        user.lname = request.POST["up-lname"]
        user.email = request.POST["up-email"]
        user.save()
        return redirect('/dashboard')

def postlike(request,id):
    user = User.objects.get(id=request.session['user_id'])
    message = Quotes.objects.get(id=id)
    message.like.add(user)
    message.save()
    return redirect('/dashboard')

def delequote(request,id):
    me = Quotes.objects.get(id=id)
    me.delete()
    return redirect('/dashboard')