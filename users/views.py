from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import UserRegisterForm,UserLoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class LoginPageView(View):
    def get(self,request):
        return render(request, "users/login.html")

    def post(self, request):
        login_form = AuthenticationForm(data = request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request,user)
            context = {"user":user}
            
            return render(request,"home.html",context)
        else:
            print("errorsss")
            context = {
                "form":login_form
            }
            return render(request,"users/login.html",context)

        # username = request.POST["username"]
        # password = request.POST["password"]
        # user = authenticate(request, username=username,password = password)

        # if user is None:
        #     return redirect("login-page")
        # else:
        #     return redirect("profile-page")


class RegisterPageView(View):
    def get(self, request):
        return render(request, "users/register.html")

    def post(self,request):
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        data = {
            "first_name": request.POST["first_name"],
            "last_name": request.POST["last_name"],
            "email": request.POST["email"],
            "username": request.POST["username"],
            "password": password1,
        }
        user = UserRegisterForm(data=data)
        if user.is_valid() and password1 == password2:
            user.save()
            return redirect("login-page")
        else:
            print("ERRor")
            context = {"form":user}
            return render(request, "users/register.html",context)

        # first_name = request.POST["first_name"]
        # last_name = request.POST["last_name"]
        # email = request.POST["email"]
        # username = request.POST["username"]
        # password = request.POST["password"]
        # user = User(
        #     first_name = first_name,
        #     last_name = last_name,
        #     email = email,
        #     username = username
        # )
        # user.set_password(password)
        # user.save()
        return redirect("login-page")


class UserListView(LoginRequiredMixin, View):
    def get(self,request):
        search = request.GET.get("search")
        if search is None:
            users = User.objects.all()
            context = {"users":users}
            return render(request, "users/user_list.html",context)

        else:
            users = User.objects.filter(first_name__icontains=search) | User.objects.filter(last_name__icontains=search)
            context = {"users":users,"search":search}
            return render(request, "users/user_list.html", context)
    def post(self):
        pass


class UserDetailView(View):
    def get(self,request,id):
        user = User.objects.get(id=id)
        context = {
            "user":user,
            "id":id
        }
        return render(request, "users/user_detail.html", context)


class UserSettingsView(View):
    def get(self,request,id):
        user = User.objects.get(id = id)
        context = {
            "user":user
        }
        return render(request,"users/user_settings.html",context)

    def post(self,request,id):
        user = User.objects.get(id=id)

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        new_password = request.POST.get("new_password")
        print(password, new_password)
        if password == '' and new_password == '':
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()
            return redirect("users-page")

        user = authenticate(request, username=user.username, password=password)

        if user is None:
            return HttpResponse("wrong password")

        else:
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.set_password(new_password)
            user.save()
            return redirect("users-page")

class LogOutView(View):
    def get(self,request):
        logout(request)
        return redirect("home_page_name")

class UserAddView(View):
    def get(self,request):
        return render(request, "users/user_add.html")

    def post(self,request):
        
        # first_name =  request.POST["first_name"],
        # last_name =  request.POST["last_name"],
        # email =  request.POST["email"],
        # username =  request.POST["username"],
        # password =  request.POST["password"],

        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users-page")
        else:
            print("errrrrrrrorrrrrr")
