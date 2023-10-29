from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import *
from django.contrib import messages
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as logoutUser
from django.contrib.auth.decorators import login_required

def Home(request):
    sessions =[]
    type=""
    csesions= CoffeeSesion.objects.all()[:4]
    for sess in csesions:
        sessionName=sess.name
        sessionDescription=sess.description
        sessionType =sess.type
        sessiondatetime =sess.datetime
        sessionUser =sess.user
        sessionprice=sess.price
        sessionimg=sess.img
        fetchuser = CustomUser.objects.get(username=sessionUser)
        phone_no =fetchuser.phone_no
        if sessionType =="1" :type="رياضة"
        if sessionType =="2":type="ثقافة"
        if sessionType =="3" :type="سياسة"
        fetchCoffee=Coffee.objects.filter(user=sessionUser)
        for coffee in  fetchCoffee:
            coffeeName=coffee.name
            coffeeaddress=coffee.address
            coffeeimg=coffee.img
            sessions.append({'sid':sess.id,'sessionName':sessionName,'sessionDescription':sessionDescription,"sessionimg":sessionimg,
                              "sessionprice":sessionprice , 'sessionType':type,'sessiondatetime':sessiondatetime,'coffeeName':coffeeName,
                                  'coffeeaddress':coffeeaddress,'coffeeimg':coffeeimg,"phone_no":phone_no})
    return render(request,"pages/index.html",context={"sessions":sessions})

def sessionPage(request):
    sessions =[]
    type=""
    if request.method == "POST":
        sessionType = request.POST.get("sessiontype")
        print("type",type)
        if sessionType != "0":
            csesions= CoffeeSesion.objects.filter(type=sessionType)
        else:
             csesions= CoffeeSesion.objects.all()
    else:
        csesions= CoffeeSesion.objects.all()
    for sess in csesions:
        sessionName=sess.name
        sessionDescription=sess.description
        sessionType =sess.type
        sessiondatetime =sess.datetime
        sessionprice=sess.price
        sessionimg=sess.img
        sessionUser =sess.user
        fetchuser = CustomUser.objects.get(username=sessionUser)
        phone_no =fetchuser.phone_no
        if sessionType =="1" :type="رياضة"
        if sessionType =="2":type="ثقافة"
        if sessionType =="3" :type="سياسة"
        fetchCoffee=Coffee.objects.filter(user=sessionUser)
        for coffee in  fetchCoffee:
            coffeeName=coffee.name
            coffeeaddress=coffee.address
            coffeeimg=coffee.img
            sessions.append({'sid':sess.id,'sessionName':sessionName,'sessionDescription':sessionDescription,
                                'sessionType':type,'sessiondatetime':sessiondatetime,'coffeeName':coffeeName,"sessionimg":sessionimg,
                                'coffeeaddress':coffeeaddress,'coffeeimg':coffeeimg,"phone_no":phone_no,"sessionprice":sessionprice})
    return render(request,"pages/sessions.html",context={"sessions":sessions})


def signUp_CoffeeOwner(request):
    usertype = ""
    Pfile_url =""
    Cfile_url =""
    if request.method == "POST":
        print('request.method',request.POST.get("username"))
        username = request.POST.get("username")
        name = request.POST.get("name")
        print('username,type',username,type)
        phone =request.POST.get('phone')
        if 'pimg' in  request.FILES:
            photo =request.FILES['pimg']
            pfss = FileSystemStorage()
            pfile = pfss.save(photo.name,photo)
            Pfile_url = pfss.url(pfile)
        CoffeeName =request.POST.get('CoffeeName')
        CoffeeDescripion =request.POST.get('CoffeeDescripion')
        CoffeeAdress =request.POST.get('CoffeeAdress')
        if 'CoffeeImage' in  request.FILES:
            CoffeeImage =request.FILES['CoffeeImage']
            cfss = FileSystemStorage()
            cfile = cfss.save(CoffeeImage.name,CoffeeImage)
            Cfile_url = cfss.url(cfile)
            print(Cfile_url)
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        checkuser=CustomUser.objects.filter(username=username).exists()
        if(checkuser == False):
         if password1 == password2:
                try:
                    usertype="coffee"
                    user = CustomUser.objects.create_user(Full_name=name,phone_no=phone,username=username,password=password1,userType=usertype,Photo=Pfile_url)
                    user.save()
                    print("user")
                    coffee_shop = Coffee(
                        name=CoffeeName,
                        description=CoffeeDescripion,
                        img=Cfile_url,
                        address=CoffeeAdress,
                        user=user  
                    )
                    coffee_shop.save()
                    messages.success(request, 'تم التسجيل بنجاح.')
                    return redirect('login')
                except Exception as e:
                    print(f"Save failed: {e}")
         else:messages.error(request, 'كلمة المرور متطابقة')
        else:
              messages.error(request, 'المستخدم موجود')
    return render (request,'user/signupCoffee.html')

def signUp_User(request):
    usertype = ""
    Pfile_url =""
    if request.method == "POST":
        print('request.method',request.POST.get("username"))
        username = request.POST.get("username")
        name = request.POST.get("name")
        print('username,type',username)
        phone =request.POST.get('phone')
        if 'pimg' in  request.FILES:
            photo =request.FILES['pimg']
            pfss = FileSystemStorage()
            pfile = pfss.save(photo.name,photo)
            Pfile_url = pfss.url(pfile)
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        checkuser=CustomUser.objects.filter(username=username).exists()
        if(checkuser == False):
         if password1 == password2:
                try:
                    usertype="user"
                    user = CustomUser.objects.create_user(Full_name=name,phone_no=phone,username=username,password=password1,userType=usertype,Photo=Pfile_url)
                    user.save()
                    print("user")
                    messages.success(request, 'تم التسجيل بنجاح.')
                    return redirect('login')
                except Exception as e:
                    print(f"Save failed: {e}")
         else:messages.error(request, 'كلمة المرور متطابقة')
        else:
              messages.error(request, 'المستخدم موجود')
    return render (request,'user/signupuser.html')

def Login(request):
    if request.method == "POST":
        userN = request.POST.get("username")
        password=request.POST.get('password')
        print('login userN',userN,password)
        user = authenticate(username=userN,password=password)
        print('login user',user)
        if user:
            userID = user.id
            getusertype = user.userType
            print('login getrole',getusertype)
            if getusertype == 'user' :
                auth_login(request,user)
                return redirect('/user/')
            if getusertype == 'coffee' :
                auth_login(request,user)
                return redirect('/coffee/')
        else:
          messages.error(request,'المستخدم غير موجود')
    return render (request, 'user/login.html')

def CoffeeOwner(request):
    current_user = request.user
    if current_user is not None:
        current_userId = current_user.id
        photo =current_user.Photo
        username=current_user.username
        phone_no=current_user.phone_no
        Full_name = current_user.Full_name
        Coffeefetch = Coffee.objects.filter(user=current_user)
        for coffee in Coffeefetch:
            coffeeName= coffee.name
            coffeeDes= coffee.description
            coffeeaddresss= coffee.address
            coffeeimg= coffee.img
        Coffeesesionfetch = CoffeeSesion.objects.filter(user=current_user)

            
        print("username",username,phone_no,coffeeName)
       
    context={
        "userphoto":photo,
        "userusername":username,
        "userfullName":Full_name,
        "userphone_no":phone_no,
        "coffeeName":coffeeName,
        "coffeeDes":coffeeDes,
        "coffeeaddresss":coffeeaddresss,
        "coffeeimg":coffeeimg,
        "Coffeesession":Coffeesesionfetch
    }

    return render (request, 'user/CoffeeOwner.html',context)

def UserPage(request):
    sessions=[]
    current_user = request.user
    if current_user is not None:
        current_userId = current_user.id
        photo =current_user.Photo
        username=current_user.username
        phone_no=current_user.phone_no
        Full_name = current_user.Full_name   
        reservedSesion = Booking.objects.filter(user=current_user)
        for sess in reservedSesion:
            sessionID= sess.session.id
            fetchSesion = CoffeeSesion.objects.get(id=sessionID)
            # for session in fetchSesion:
            sessionName= fetchSesion.name
            print("sessionName",sessionName)
            sessiondescription= fetchSesion.description
            sessionuser= fetchSesion.user
            sessiontype= fetchSesion.type
            sessionprice= fetchSesion.price
            sessionimg= fetchSesion.img
            sessiondatetime=fetchSesion.datetime
            if sessiontype =="1" : type="رياضة"
            if sessiontype =="2":  type="ثقافة"
            if sessiontype =="3":  type="سياسة"
            fetchCoffee=Coffee.objects.filter(user=sessionuser)
            for coffee in fetchCoffee:
                coffeeName=coffee.name
                coffeeaddress=coffee.address
                coffeeimg=coffee.img
                sessions.append({'sid':sess.id,'sessionName':sessionName,'sessionDescription':sessiondescription,
                                   "sessionprice":sessionprice,"sessionimg":sessionimg ,'sessionType':type,'sessiondatetime':sessiondatetime,'coffeeName':coffeeName,
                                    'coffeeaddress':coffeeaddress,'coffeeimg':coffeeimg,"phone_no":phone_no})
          
    context={
        "userphoto":photo,
        "userusername":username,
        "userfullName":Full_name,
        "userphone_no":phone_no,
        "sessions":sessions
       
    }

    return render (request, 'user/UserPage.html',context)

def AddcoffeeSession(request):
    current_user = request.user
    if request.method == "POST":
        current_userId = current_user.id
        if current_user is not None:
            print('current_user',current_user)
            checkEx_user=CustomUser.objects.filter(username=current_user).exists()
            if checkEx_user:
                getrole= current_user.userType
                print('checkEx_user',checkEx_user)
                print('getrole from session',getrole)
                if getrole == 'coffee':
                    sessionName = request.POST.get("sessionName")
                    sessionDescripion = request.POST.get("sessionDescripion")
                    sessionType = request.POST.get("sessionType")
                    sessionPrice = request.POST.get("sessionPrice")
                    if 'simg' in  request.FILES:
                        photo =request.FILES['simg']
                        pfss = FileSystemStorage()
                        pfile = pfss.save(photo.name,photo)
                        Pfile_url = pfss.url(pfile)
                    try:
                        session = CoffeeSesion(name=sessionName,
                        description = sessionDescripion,type=sessionType,img=Pfile_url,price =sessionPrice,
                        user=current_user)  
                        session.save()
                        print("save")
                    except Exception as e:
                        print(f"Save failed: {e}")
        else:messages.error(request, 'wrong user.')
    return redirect('/coffee/')


@login_required(login_url='/login/')  
def bookSession(request):
    current_user = request.user
    if current_user is not None:
        if request.method == "POST":
            sessionID=request.POST.get('sessionID')
            current_userId = current_user.id
            print('sessionID',sessionID)
            getuser  = CustomUser.objects.get(id= current_userId)
            getuserType=getuser.userType
            print('from userInterestRoom getuserType',getuserType)
            getsession = CoffeeSesion.objects.get(id=sessionID)
            print('getsession',getsession)
            if getuserType == 'user' :
                is_book = Booking.objects.filter(user=getuser,session=getsession).exists()
                if is_book == False:
                    book = Booking(user=getuser,session=getsession)
                    book.save()
                else:messages.error(request, 'تم حجز الجلسة من قبل')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:return redirect('/login/')

@login_required(login_url='/login/')   
def checkProfile (request):
    current_user = request.user
    if current_user is not None:
        current_userId = current_user.id
        print('current_user',current_user)
        checkEx_user=CustomUser.objects.filter(username=current_user).exists()
        print(checkEx_user)
        if checkEx_user:
            getrole= current_user.userType
            print('checkEx_user',checkEx_user)
            print('getrole',getrole)
            if getrole == 'user' :
                return redirect('/user/')
            if getrole == 'coffee' :
              return redirect('/coffee/')
    return render (request, 'user/login.html')

@login_required(login_url='/login/') 
def Logout (request):
    logoutUser(request)
    return redirect('/login/')


@login_required(login_url='/login/') 
def deleteBookingSession (request):
    current_user = request.user
    if current_user is not None:
        if request.method == "POST":
            sessionID=request.POST.get('sessionID')
        print('deleteRoom',id)
        session=Booking.objects.filter(session=sessionID,user=current_user)
        session.delete()
        return redirect('/user/')