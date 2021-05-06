from django.shortcuts import render, redirect
from .models import  *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from datetime import date
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def admin_login(request):
    error=""
    if request.method=="POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user:
            try:
                if user.is_staff:
                    login(request, user)
                    error="no"
                else:
                    error="yes"
            except:
                error="yes"
    d = {'error':error}
    return render(request, 'admin_login.html', d)

def user_login(request):
    error=""
    if request.method=="POST":
        u = request.POST['uname'];
        p = request.POST['pwd'];
        user = authenticate(username=u, password=p)
        if user:
            try:
                user1 = StudentUser.objects.get(user=user)
                if user1.type == "Student":
                    login(request, user)
                    error="no"
                else:
                    error="yes"
            except:
                error="yes"
        else:
            error="yes"
    d={'error':error}
    return render(request, 'user_login.html', d)

def recruiter_login(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname'];
        p = request.POST['pwd'];
        user = authenticate(username=u, password=p)
        if user:
            try:
                user1 = Recruiter.objects.get(user=user)
                if user1.type == "Recruiter" and user1.status != "pending":
                    login(request, user)
                    error = "no"
                else:
                    error = "not"
            except:
                error = "yes"
        else:
            error = "yes"
    d = {'error': error}
    return render(request, 'recruiter_login.html', d)

def recruiter_signup(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        i = request.FILES['image']
        p = request.POST['pwd']
        e = request.POST['email']
        con = request.POST['contact']
        company = request.POST['company']
        gen = request.POST['gender']
        try:
            user = User.objects.create_user(first_name=f, last_name=l, username=e, password=p)
            Recruiter.objects.create(user=user, mobile=con, image=i, gender=gen, company=company, type="Recruiter", status="pending")
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'recruiter_signup.html', d)

def user_home(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    return render(request, 'user_home.html')

def recruiter_home(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    return render(request, 'recruiter_home.html')

def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    return render(request, 'admin_home.html')

def Logout(request):
    logout(request)
    return redirect('index')

def user_signup(request):
    error=""
    if request.method=='POST':
        f = request.POST['fname']
        l = request.POST['lname']
        i = request.FILES['image']
        p = request.POST['pwd']
        e = request.POST['email']
        con = request.POST['contact']
        gen = request.POST['gender']
        try:
            user = User.objects.create_user(first_name=f, last_name=l, username=e, password=p)
            StudentUser.objects.create(user=user, mobile=con, image=i, gender=gen, type="Student")
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'user_signup.html', d)
def view_users(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=StudentUser.objects.all()
    d={'data':data}
    return render(request, 'view_users.html',d)

def delete_user(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=User.objects.get(id=pid)
    data.delete()
    return redirect('view_users')

def recruiter_pending(request):
     if not request.user.is_authenticated:
         return redirect('admin_login')
     data=Recruiter.objects.filter(status='pending')
     d={'data':data}
     return render(request,'recruiter_pending.html',d)


def change(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    e=""
    recruiter = Recruiter.objects.get(id=pid)
    if request.method=="POST":
        s=request.POST["status"]
        recruiter.status=s
        try:
            recruiter.save()
            e="no"
        except:
            e="yes"
    d = {'data': recruiter,'error':e}
    return render(request, 'change_status.html', d)

def recruiter_accepted(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruiter.objects.filter(status='Accept')
    d = {'data': data}
    return render(request, 'recruiter_accepted.html', d)
def recruiter_rejected(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruiter.objects.filter(status='Reject')
    d = {'data': data}
    return render(request, 'recruiter_rejected.html', d)

def recruiter_all(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruiter.objects.all()
    d = {'data': data}
    return render(request, 'recruiter_all.html', d)

def delete_recruiter(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=User.objects.get(id=pid)
    data.delete()
    return redirect('recruiter_all')

def change_passwordadmin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    e = ""

    if request.method == "POST":
        c = request.POST["cpassword"]
        n=request.POST["npassword"]

        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                e="no"
            else:
                e="no"

        except:
            e = "yes"
    d={'error':e}
    return render(request,"change_password_admin.html",d)

def change_passworduser(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    e = ""

    if request.method == "POST":
        c = request.POST["cpassword"]
        n=request.POST["npassword"]

        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                e="no"
            else:
                e="no"

        except:
            e = "yes"
    d={'error':e}
    return render(request,"change_password_user.html",d)

def change_passwordrecruiter(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    e = ""

    if request.method == "POST":
        c = request.POST["cpassword"]
        n=request.POST["npassword"]

        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                e="no"
            else:
                e="no"

        except:
            e = "yes"
    d={'error':e}
    return render(request,"change_password_recruiter.html",d)

def add_job(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    e = ""
    if request.method == 'POST':
        t = request.POST['title']
        sd = request.POST['sdate']
        ed = request.POST['edate']
        s = request.POST['salary']
        lg = request.FILES['logo']
        loc = request.POST['location']
        exp = request.POST['exp']
        skl = request.POST['skills']
        desc = request.POST['desc']
        link=request.POST['link']
        user = request.user
        recruiter=Recruiter.objects.get(user=user)

        try:
            Job.objects.create(recruiter=recruiter, start_date=sd,end_date=ed,title=t ,salary=s,image=lg,description=desc ,experience=exp,location=loc,skills=skl,creationdate=date.today(),link=link)
            e = "no"
        except:
            e = "yes"
    d = {'error': e}
    return render(request,'Add_Job.html',d)

def job_list(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user=request.user
    recruiter = Recruiter.objects.get(user=user)
    Jlist=Job.objects.filter(recruiter=recruiter)
    return render(request,'Job_list.html',{'Jlist':Jlist})

def job_l_u(request):

    obj=Job.objects.all()
    print(request.user)
    return render(request,'job_l_u.html',{'Jlist':obj})

def apply(request,pid):
    job=Job.objects.get(id=pid)
    v=job.recruiter.user
    candidate=request.user
    obj1=Recruiter.objects.get(user=v)
    obj=StudentUser.objects.get(user=candidate)
    print(request.user)
    a=AppliedJobs.objects.create(recruiter=obj1,candidate=obj,job=job)
    a.save()
    return redirect("user_home")

def view_app_user(request):
    candidate = request.user
    obj = StudentUser.objects.get(user=candidate)
    a = AppliedJobs.objects.filter(candidate=obj)
    return render(request,"view_app_user.html",{'a':a})

#  Recruiter -- View Application Page for
def view_app_recruiter(request):

    q= Recruiter.objects.get(user=request.user)
    a = AppliedJobs.objects.filter(recruiter=q)
    for x in a:
        print(x.candidate.user.username)
    return render(request,"view_app_recruiter.html",{'a':a})

def LatestJobs(request):
    obj=Job.objects.all()[:5]
    return render(request,"LatestJobs.html",{"obj":obj})