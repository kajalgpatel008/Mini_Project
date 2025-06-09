from django.shortcuts import render
from .models import Contact, User
from django.core.mail import send_mail
from django.conf import settings
import random 

# Create your views here.
def index(request):
    return render(request,'index.html')
def contact(request):
    if request.method == "POST":
        Contact.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],    
            mobile=request.POST['mobile'],
            remarks=request.POST['remarks']
        )
        msg="Contact Created Successfully"
        contacts=Contact.objects.all().order_by('-id')[:3] 
        return render(request,'contact.html',{'msg':msg ,'contacts':contacts})
    else:
        contacts=Contact.objects.all().order_by('-id')[:3]
        return render(request,'contact.html',{'contacts':contacts})
def signup(request):
    if request.method == "POST":
        try:
            User.objects.get(email=request.POST['email'])
            msg="Email already exists"
            return render(request,'signup.html',{'msg':msg})
        except:
            if request.POST['password'] == request.POST['cpassword']:
                User.objects.create(
                   fname=request.POST['fname'],
                   lname=request.POST['lname'],
                   email=request.POST['email'],    
                   mobile=request.POST['mobile'],
                   address=request.POST['address'],
                   password=request.POST['password'],
                   user_image=request.FILES['user_image']
               )
                msg="User Created Successfully"
                return render(request,'signup.html',{'msg':msg})
            else:
                msg="Password and Confirm Password do not match"
                return render(request,'signup.html',{'msg':msg})
    else:
        return render(request,'signup.html')  
          
def login(request):
    if request.method == "POST":
        try:
            user=User.objects.get(email=request.POST['email'])
            if user.password == request.POST['password']:
                request.session['email'] = user.email
                request.session['fname'] = user.fname
                request.session['user_image'] = user.user_image.url
                return render(request,'index.html')
            else:
                msg="Incorrect Password"
                return render(request,'login.html',{'msg':msg})
        except:
            msg="Invalied Email"
            return render(request,'login.html',{'msg':msg})
    else:
        return render(request,'login.html')
def logout(request):
        try:
            del request.session['email']
            del request.session['fname']
            del request.session['user_image']
        except:
            pass
        return render(request,'login.html')
def profile(request):
    user=User.objects.get(email=request.session['email'])
    if request.method == "POST":
        user.fname = request.POST['fname']
        user.lname = request.POST['lname']
        user.email = request.POST['email']
        user.mobile = request.POST['mobile']
        user.address = request.POST['address']
        if 'user_image' in request.FILES:
            user.user_image = request.FILES['user_image']
        user.save()
        request.session['user_image'] = user.user_image.url
        msg="Profile Updated Successfully"
        return render(request,'profile.html',{'user':user,'msg':msg})
    else:
        return render(request,'profile.html',{'user':user})
def change_password(request):
    if request.method == "POST":
        user=User.objects.get(email=request.session['email'])
        if user.password == request.POST['old_password']:
            if request.POST['new_password'] == request.POST['cnew_password']:
                if user.password != request.POST['new_password']:
                    user.password = request.POST['new_password']
                    user.save()
                    del request.session['email']
                    del request.session['fname']
                    del request.session['user_image']
                    msg="Password Changed Successfully"
                    return render(request,'login.html',{'msg':msg})
                else:
                    msg="Your New Password cannot be from Your Old Password"
                    return render(request,'change_password.html',{'msg':msg})
            else:
                msg="New Password and Confirm New Password do not match"
                return render(request,'change_password.html',{'msg':msg})
        else:
            msg="Old Password Does Not Matched"
            return render(request,'change_password.html',{'msg':msg})
    else:
        return render(request,'change_password.html')
def forgot_password(request):
    if request.method == "POST":
        try:
            user=User.objects.get(email=request.POST['email'])
            subject="OTP For Forgot Password"
            otp=random.randint(1000,9999)
            message="Your OTP for forgot password is "+str(otp)
            send_mail(subject, message, settings.EMAIL_HOST_USER,[user.email,])
            request.session['e'] = user.email
            request.session['otp'] = otp
            return render(request,'otp.html')
        except:
            msg="Email Not Registered"
            return render(request,'forgot_password.html',{'msg':msg})
    else:
        return render(request,'forgot_password.html')

def verify_otp(request):
    if int(request.POST['otp']) == request.session['otp']:
        del request.session['otp']
        return render(request,'new-password.html')
    else:
        msg="Invalid OTP"
        return render(request,'otp.html',{'msg':msg})

def new_password(request):
    if request.POST['new_password'] == request.POST['cnew_password']:
        user=User.objects.get(email=request.session['e'])
        user.password = request.POST['new_password']
        user.save()
        del request.session['e']
        msg="Password Updated Successfully"
        return render(request,'login.html',{'msg':msg})
    else:
        msg="New Password and Confirm New Password do not matched"
        return render(request,'new-password.html',{'msg':msg})














            
          


            





        
