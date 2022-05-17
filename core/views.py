from django.shortcuts import render, redirect
from django.views import View
from .models import Donation, Institution, Category
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

class LandingPage(View):
    ctx = {}

    def get(self, request):

        donations = Donation.objects.all()
        sacks = []
        for donation in donations:
            sacks.append(donation.quantity)
        sum_of_sacks = sum(sacks)
        self.ctx['sum_of_sacks'] = sum_of_sacks

        supported_institutions = []
        for donation in donations:
            if donation.institution not in supported_institutions:
                supported_institutions.append(donation.institution)
        self.ctx['supported_institutions'] = len(supported_institutions)

        foundations = Institution.objects.filter(type_of_institution="F")
        self.ctx['foundations'] = foundations

        non_governments = Institution.objects.filter(type_of_institution="NG")
        self.ctx['non_governments'] = non_governments

        local_collections = Institution.objects.filter(type_of_institution="LC")
        self.ctx['local_collections'] = local_collections

        categories = Category.objects.all()
        self.ctx['categories'] = categories

        return render(request, 'index.html', self.ctx)


class AddDonation(View):
    ctx = {}

    def get(self, request):
        user = request.user

        if user.is_authenticated:
            categories = Category.objects.all()
            institutions = Institution.objects.all()
            self.ctx['categories'] = categories
            self.ctx['institutions'] = institutions
            return render(request, 'form.html', self.ctx)
        else:
            return redirect('/login/')

    def post(self, request):
        user = request.user
        categories = request.POST.get('categories')
        bags = request.POST.get('bags')
        organization = request.POST.get('organization')
        address = request.POST.get('address')
        city = request.POST.get('city')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        date = request.POST.get('data')
        time = request.POST.get('time')
        comment = request.POST.get('more_info')
        new_donation = Donation(quantity=bags,
                                address=address,
                                phone_number=phone,
                                city=city,
                                institution=Institution.objects.get(name=organization),
                                zip_code=postcode,
                                pick_up_date=date,
                                pick_up_time=time,
                                pick_up_comment=comment,
                                user=user)
        new_donation.save()
        for category in categories:
            new_donation.categories.add(Category.objects.get(id=category))
        return render("/confirmation/")


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            return redirect("/")
        else:
            return redirect("/register/")


class Register(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password2')

        if name and surname and email and password and password_confirmation and password == password_confirmation:
            User.objects.create_user(first_name=name, last_name=surname, email=email, password=password, username=email)
            return redirect('/login/')


class Logout(View):

    def get(self, request):
        logout(request)
        return redirect("/")


class Confirmation(View):
    ctx = {}

    def get(self, request):
        user = request.user
        self.ctx['user'] = user

        if user.is_superuser:
            self.ctx["superuser"] = user
        return render(request, "form-confirmation.html", self.ctx)


class Profile(View):
    ctx = {}

    def get(self, request):
        user = request.user

        if user.is_authenticated:
            self.ctx['user'] = user
            user_donations = Donation.objects.filter(user=user)
            self.ctx['donations'] = user_donations
            return render(request, 'profile.html', self.ctx)
