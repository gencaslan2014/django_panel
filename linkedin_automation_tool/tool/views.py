from django.shortcuts import render

# Create your views here.
def login(request):
    if request.POST==True:
        email=request.get('email')
        password=request.get('password')
        if request.User.authenticate()==True:
            return True
def post_p(request):
   obj = list(PostModel.objects.filter(username=request.user).values())
   print(obj)

   x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
   if x_forwarded_for:
      user_ip = x_forwarded_for.split(',')[0]
   else:
      user_ip = request.META.get('REMOTE_ADDR')
      user_ip = '202.47.55.117'

   for o in range(len(obj)):
      user_time = obj[o]['time']  # Assuming user entered 4pm
      user_time = datetime.datetime.combine(datetime.datetime.today(), user_time)

      geoip_db = geoip2.database.Reader('GeoLite2-City.mmdb')
      # Replace with the user's IP address
      user_ip = user_ip
      print(user_ip)

      # Lookup the user's location using the GeoIP database
      geoip_data = geoip_db.city(user_ip)

      # Determine the user's timezone
      user_tz = pytz.timezone(geoip_data.location.time_zone)
      print(user_tz)

      # Convert the UTC time to the user's timezone
      user_time = user_time.replace(tzinfo=pytz.utc).astimezone(user_tz)
      obj[o]['time'] = user_time.time()
   return render(request,'post.html',{'posts':obj})


@csrf_exempt
def login_user(request):
    print("aaaaa")
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)

            return redirect(home)
        else:

            return render(request, 'index.html')
    else:
        return render(request, 'index.html')

def logout_user(request):
   print("logout")
   if request.method == 'POST':
      auth.logout(request)
   return redirect(login_user)


from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views
from .models import *
import datetime
from django.contrib import messages, auth
from .forms import *
from django.shortcuts import redirect
from django.template import loader
from selenium.webdriver.support.ui import Select
from selenium import webdriver
import time
from django.utils import timezone
import pytz
import geoip2.database
from django.http import JsonResponse


# path="E:/Analyt IQ/28th/chromedriver"
# driver = webdriver.Chrome(path)

# Create your views here.
def group(request):
    obj = list(GroupModel.objects.filter(username=request.user).values())

    # return render(request, 'home.html', {'pages': obj})
    return render(request, "group.html", {'groups': obj})


def save_group(request):
    if request.method == 'POST':
        group_id = request.POST['group_id']
        group_name = request.POST['group_name']
        obj = GroupModel()
        obj.group_id = group_id
        obj.group_name = group_name
        obj.username = request.user
        obj.save()
    return redirect(group)


@csrf_exempt
def login_with_facebook_cookies(request):
    if request.method == 'POST':
        facebook_cookies = request.POST.get('facebook_cookies')
        # TODO: Authenticate user and retrieve Facebook data using the cookies
        print(facebook_cookies)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def add_account(request):
    if request.method == 'POST':
        try:
            obj = FBAccount.objects.get(username=request.user)
            email = request.POST['email']
            password = request.POST['password']
            obj.email = email
            obj.password = password
            obj.status = "run"
            obj.save()
        except Exception as e:
            print(e)
            email = request.POST['email']
            password = request.POST['password']
            obj = FBAccount()
            obj.email = email
            obj.password = password
            obj.username = request.user
            obj.status = "run"
            obj.save()
        try:
            obj = FBAccount.objects.get(username=request.user)
            print(obj)
            if obj:
                return render(request, "add_account.html", {"email": obj.email, "password": obj.password})
        except Exception as e:
            print(e)
            pass
    else:
        try:
            obj = FBAccount.objects.get(username=request.user)
            print(obj)
            if obj:
                return render(request, "add_account.html", {"email": obj.email, "password": obj.password})
        except Exception as e:
            print(e)
            pass

    return render(request, "add_account.html")


def save_page(request):
    if request.method == 'POST':
        page_id = request.POST['page_id']
        obj = PageModel()
        obj.page_id = page_id
        obj.username = request.user
        obj.save()
        return redirect(home)


def submit(request):
    if request.method == 'POST':
        form = post_form(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            form.instance.username = request.user
            form.instance.status = "on"

            user_time = form.instance.time
            user_time = datetime.datetime.combine(datetime.datetime.today(), user_time)
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                user_ip = x_forwarded_for.split(',')[0]
            else:
                user_ip = request.META.get('REMOTE_ADDR')
                user_ip = '202.47.55.117'

            geoip_db = geoip2.database.Reader('GeoLite2-City.mmdb')
            # Replace with the user's IP address
            user_ip = user_ip
            print(user_ip)

            # Lookup the user's location using the GeoIP database
            geoip_data = geoip_db.city(user_ip)

            # Determine the user's timezone
            user_tz = pytz.timezone(geoip_data.location.time_zone)
            print(user_tz)

            user_time = user_tz.localize(user_time)

            # Convert the user input to UTC
            utc_time = timezone.localtime(user_time, timezone.utc)

            form.instance.time = utc_time.time()

            form.save()
            post_id = form.instance.id
            groups = list(GroupModel.objects.filter(username=request.user).values())

            for group in groups:
                group_id = group['group_id']
                group_name = group['group_name']
                every = request.POST['every-' + group_id]
                time = request.POST['time-' + group_id]
                obj = GroupPosting()
                obj.group_id = group_id
                obj.group_name = group_name
                obj.every = every
                obj.time = time
                obj.post_id = post_id
                obj.username = request.user
                obj.save()

            return redirect(post_p)

        else:
            form = post_form()
        return render(request, 'title.html', {'form': form})


def on_post(request, title=None):
    obj = PostModel.objects.get(username=request.user, title=title)
    print(obj.status)
    obj.status = "on"
    print(obj.status)
    obj.save()
    return redirect(post_p)


def off_post(request, title=None):
    obj = PostModel.objects.get(username=request.user, title=title)
    print(obj.status)
    obj.status = "off"
    obj.save()
    return redirect(post_p)


def update_post(request):
    if request.method == 'POST':
        obj = PostModel.objects.get(username=request.user, title=request.POST['title'])
        form = post_form(request.POST, request.FILES, instance=obj)
        # obj = PostModel.objects.get(username=request.user, title=form.title)

        if form.is_valid():
            # form.instance.username = request.user
            # form.instance.status = "on"
            # obj = PostModel.objects.get(username=form.instance.username,title=form.instance.title)
            # obj.text = form.instance.text

            user_time = form.instance.time
            user_time = datetime.datetime.combine(datetime.datetime.today(), user_time)
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                user_ip = x_forwarded_for.split(',')[0]
            else:
                user_ip = request.META.get('REMOTE_ADDR')
                user_ip = '202.47.55.117'

            geoip_db = geoip2.database.Reader('GeoLite2-City.mmdb')
            # Replace with the user's IP address
            user_ip = user_ip
            print(user_ip)

            # Lookup the user's location using the GeoIP database
            geoip_data = geoip_db.city(user_ip)

            # Determine the user's timezone
            user_tz = pytz.timezone(geoip_data.location.time_zone)
            print(user_tz)

            user_time = user_tz.localize(user_time)

            # Convert the user input to UTC
            utc_time = timezone.localtime(user_time, timezone.utc)

            form.instance.time = utc_time.time()

            form.save()

            post_id = form.instance.id
            groups = list(GroupModel.objects.filter(username=request.user).values())

            for group in groups:
                group_id = group['group_id']
                # post_id =group['post_id']
                every = request.POST['every-' + group_id]
                time = request.POST['time-' + group_id]
                obj = GroupPosting.objects.get(username=request.user, post_id=post_id, group_id=group_id)
                # obj.group_id = group_id
                obj.every = every
                obj.time = time
                # group.post_id = post_id
                # group.username = request.user
                obj.save()

            # return redirect(post_p)

            # form.save()
            return redirect(post_p)

        else:
            form = post_form()
        return render(request, 'title.html', {'form': form})


def edit_post(request, id):
    # print(title)
    # title=title.replace("%20"," ")
    # obj = list(PostModel.objects.filter(username=request.user,title=title).values())[0]

    obj = PostModel.objects.get(username=request.user, id=id)
    form = post_form(instance=obj)
    obj = list(PageModel.objects.filter(username=request.user).values())
    choices = [(request.user, request.user)]
    for i in obj:
        choices.append((i['page_id'], i['page_id']))
    choices = tuple(choices)
    form.fields['post_as'].choices = choices
    groups = list(GroupPosting.objects.filter(username=request.user, post_id=id).values())
    # form = post_form(initial={"title":obj['title'],"text":obj['text'],
    #                           "post_as":obj["post_as"],"every":obj["every"],
    #                           "time":obj['time'],"group":obj["group"],"image":obj['image']})

    print(form)
    # print(obj)
    # form.title = obj['title']

    return render(request, "edit_post.html", {'form': form, 'groups': groups})


def login(request):
    return render(request, "index.html")


def home(request):
    print("Home")
    obj = list(PageModel.objects.filter(username=request.user).values())

    return render(request, 'home.html', {'pages': obj})


def delete_page(request, page_id=None):
    print(request.method)

    PageModel.objects.filter(username=request.user, page_id=page_id).delete()
    return redirect(home)


def delete_group(request, group_id=None):
    print(request.method)

    GroupModel.objects.filter(username=request.user, group_id=group_id).delete()
    return redirect(group)


def delete_post(request, title=None):
    print(request.method)

    PostModel.objects.filter(username=request.user, title=title).delete()
    return redirect(post_p)


def post_p(request):
    obj = list(PostModel.objects.filter(username=request.user).values())
    print(obj)

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        user_ip = x_forwarded_for.split(',')[0]
    else:
        user_ip = request.META.get('REMOTE_ADDR')
        user_ip = '202.47.55.117'

    for o in range(len(obj)):
        user_time = obj[o]['time']  # Assuming user entered 4pm
        user_time = datetime.datetime.combine(datetime.datetime.today(), user_time)

        geoip_db = geoip2.database.Reader('GeoLite2-City.mmdb')
        # Replace with the user's IP address
        user_ip = user_ip
        print(user_ip)

        # Lookup the user's location using the GeoIP database
        geoip_data = geoip_db.city(user_ip)

        # Determine the user's timezone
        user_tz = pytz.timezone(geoip_data.location.time_zone)
        print(user_tz)

        # Convert the UTC time to the user's timezone
        user_time = user_time.replace(tzinfo=pytz.utc).astimezone(user_tz)
        obj[o]['time'] = user_time.time()
    return render(request, 'post.html', {'posts': obj})


def title(request):
    print("Title page")
    form = post_form(request.POST, request.FILES)
    if form.is_valid():
        form.save()

    else:
        form = post_form(user=request.user)
    obj = list(PageModel.objects.filter(username=request.user).values())
    choices = [("Profile", "Profile")]
    for i in obj:
        choices.append((i['page_id'], i['page_id']))
    choices = tuple(choices)
    print(choices)
    groups = list(GroupModel.objects.filter(username=request.user).values())
    # user = request.user
    # form.fields['post_as'].choices = choices
    return render(request, 'title.html', {'form': form, 'groups': groups})


def logout_user(request):
    print("logout")
    if request.method == 'POST':
        auth.logout(request)
    return redirect(login_user)


@csrf_exempt
def login_user(request):
    print("aaaaa")
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)

            return redirect(home)
        else:

            return render(request, 'index.html')
    else:
        return render(request, 'index.html')


def title_post(request):
    print("bbbbbbbbbbbb")
    if request.method == 'GET':
        print("aaaaaaaa")
        title = request.POST['title']
        message = request.POST['message']
        print(title, "title====title")
        print(message, "message====message")

        # driver.get("https://www.facebook.com/")

        # email = "+91971865-1836"
        # password = "stonewhite@078"
        # post= "Hi"+"how are you"
        # # post = str(title+message)

        # def post():

        #    email_input = driver.find_element(by="xpath",value="//input[@aria-label='Email address or phone number']")
        #    email_input.send_keys(email)

        #    password_input = driver.find_element(by="xpath",value="//input[@aria-label='Password']")
        #    password_input.send_keys(password)

        #    button = driver.find_element(by="xpath",value="//button[@name='login']").click()
        #    time.sleep(5)

        #    post_click = driver.find_element(by="xpath",value="//div[@class='x1lkfr7t xkjl1po x1mzt3pk xh8yej3 x13faqbe xi81zsa']").click()
        #    time.sleep(10)

        #    post_input = driver.find_element(by="xpath",value="//div[@class='x78zum5 xl56j7k']")
        #    post_input.send_keys(post)

        #    send=driver.find_element(by="xpath",value="//*[contains(text(), 'post')]").click()
        #    print(send)

    return render(request, 'post.html')