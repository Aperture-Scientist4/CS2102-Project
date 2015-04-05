from django.shortcuts import render
from store.forms import UserForm
from store.forms import SearchForm
from store.forms import FeedbackForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect, HttpResponse
from django.db import connection
from store.models import Purchased, Rent, App

import random, string, datetime


def indexView(request):
    search_form = SearchForm()
    return render(request, 'store/index.html', {'search_form':search_form})

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print ("Error!")
    else:
        user_form = UserForm()
    return render(request,
            'store/register.html',
            {'user_form': user_form, 'registered': registered} )


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect('/store/')
        else:
            return HttpResponse("Invalid login!")

    else:

        return render(request, 'store/login.html', {})


@login_required(login_url='/store/login/')
def my_account(request, user_name):
    if request.user.username != user_name :
        return HttpResponse("You are not allowed to access this page!")
    user = User.objects.get(username = user_name)
    context_dict = {}
    context_dict['username'] = user.username
    cursor = connection.cursor()
    cursor.execute("SELECT a.appid, a.name, a.genre, a.icon FROM store_app a, store_purchased p WHERE p.appid_id = a.appid AND p.userid_id = %d;" % int(user.id))
    app_list_purchased = cursor.fetchall()
    for i in range(len(app_list_purchased)):
        is_reviewed = is_rated(app_list_purchased[i][0], user.id)
        random_picture = str(random.randint(51,70))
        app_list_purchased[i] += (is_reviewed, random_picture)
    cursor.execute("SELECT a.appid, a.name, a.genre, a.icon, r.expire_date FROM store_app a, store_rent r WHERE r.appid_id = a.appid AND r.userid_id = %d;" % int(user.id))
    app_list_rent = cursor.fetchall()
    for i in range(len(app_list_rent)):
        is_reviewed = is_rated(app_list_rent[i][0], user.id)
        random_picture = str(random.randint(51,70))
        app_list_rent[i] += (is_reviewed, random_picture)
    context_dict['app_list_purchased'] = app_list_purchased
    context_dict['app_list_rent'] = app_list_rent
    search_form = SearchForm()
    return render(request, 'store/my_orders.html', {'context_dict': context_dict,'search_form':search_form})

@login_required
def user_logout(request):
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/store/')

@login_required
def password_change(request,user_name):
    user = User.objects.get(username = user_name)
    context_dict = {}
    context_dict['username'] = user.username
    if request.method == 'POST':
        password = request.POST.get('password')
        newpassword1 = request.POST.get('newpassword1')
        newpassword2 = request.POST.get('newpassword2')
        if newpassword1 != newpassword2:
           return HttpResponse("New password does not match!")
        
        data = {
            'old_password': password,
            'new_password1': newpassword1,
            'new_password2': newpassword2,
        }
        
        form = PasswordChangeForm(user, data)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect('/store/login/')
        else:
            return HttpResponse("Invalid Password")
    else:
        return render(request, 'store/changePassword.html', context_dict)

#ProdcutPage views-->


def ProductPage(request, product_id):
    cursor = connection.cursor()
    app = App.objects.get(appid = product_id)
    if request.user.is_authenticated():
        userid = request.user.id
        is_purchased = is_valid_purchase(product_id, userid)
        is_rent = is_valid_rent(product_id, userid)
        is_reviewed = is_rated(product_id, userid)  
    else :
        is_purchased = False
        is_rent = False
        is_reviewed = False

    expire_date = False
    if is_rent:
        cursor.execute("SELECT expire_date FROM store_rent WHERE userid_id = %d AND appid_id =%d" % (int(userid), int(product_id)))
        expire_date = cursor.fetchone()[0]

    random_picture = str(random.randint(51,70))
    stars = calculate_rating(product_id)
    app_data = (app.appid, app.name,app.purchase_price, app.rent_price,app.genre,app.device,app.release_date,app.description, app.icon, stars, random_picture)

    cursor.execute("SELECT a.username, p.rating, p.review FROM store_purchased p, auth_user a WHERE p.appid_id = %d AND p.userid_id = a.id AND p.rating > 0" % int(product_id))
    rating_entries_tuple = cursor.fetchall()
    cursor.execute("SELECT a.username, r.rating, r.review FROM store_rent r, auth_user a WHERE r.appid_id = %d AND r.userid_id = a.id AND r.rating > 0" % int(product_id))
    rating_entries_tuple += cursor.fetchall()

    rating_entries = list()
    for entry in rating_entries_tuple:
        rating_entries.append((entry[0], int(entry[1])*"*", entry[2]))

    
    search_form = SearchForm()
    feedback_form = FeedbackForm()
    return render(request,'store/product.html',{'app_data':app_data,'purchased':is_purchased,'rent':is_rent,'expire_date':expire_date,
                                                'feedback_form':feedback_form,'rating_entries':rating_entries, 'search_form': search_form, 'reviewed': is_reviewed})
@login_required(login_url='/store/login/')
def ProductPurchase(request, product_id):
    if request.user.is_authenticated():
        if request.method == 'POST':
            userid = request.user.id
            orderid = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(10))
            cursor = connection.cursor()
            cursor.execute("INSERT INTO store_purchased(userid_id, order_id, appid_id) VALUES (%d, '%s', %d);" % (int(userid), orderid, int(product_id)))        
        return HttpResponseRedirect('/store/product/'+product_id)
    else :
        return render(request, 'store/login.html', {})

@login_required(login_url='/store/login/')
def ProductRent(request, product_id):
    if request.user.is_authenticated():
        if request.method == 'POST':
            userid = request.user.id
            orderid = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(10));
            expire_date = (datetime.date.today()+datetime.timedelta(days=7)).strftime('%Y-%m-%d')
            cursor = connection.cursor()
            cursor.execute("INSERT INTO store_rent(userid_id, order_id, appid_id, expire_date) VALUES (%d, '%s', %d, '%s');" % (int(userid), orderid, int(product_id), expire_date))        
        return HttpResponseRedirect('/store/product/'+product_id)
    else:
        return render(request, 'store/login.html', {})

@login_required
def ProductFeedback(request, product_id):
    if request.method == 'POST':
        feedbackForm = FeedbackForm(request.POST)
        if feedbackForm.is_valid():
            userid = request.user.id
            rating = feedbackForm.cleaned_data['rating']
            review = feedbackForm.cleaned_data['review']
            cursor = connection.cursor()
            if is_valid_purchase(product_id, userid):
                cursor.execute("UPDATE store_purchased SET rating = %d, review = '%s' WHERE userid_id = %d AND appid_id = %d;" % (int(rating), review, int(userid), int(product_id)))        
            else:
                cursor.execute("UPDATE store_rent SET rating = %d, review = '%s' WHERE order_id = (SELECT order_id FROM store_rent WHERE userid_id = %d AND appid_id = %d LIMIT 1);" % (int(rating), review, int(userid), int(product_id)))        
    return HttpResponseRedirect('/store/product/'+product_id)

def ErrorPage(request):
    return HttpResponse("<H1>ERROR!</H1>")

#<--ProdcutPage view

#SearchPage View-->
def create_search(request):
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            keywords = search_form.cleaned_data['keyword']
            genre = search_form.cleaned_data['types']
            rows_with_rating = list()
            '''0-2: appid, name, purchase_price,  
               3-5: genre, icon, stars,  
               6-8: is_purchased, is_rent, random_picture'''
            cursor = connection.cursor()
            if genre=='all':
                if keywords == '':
                    cursor.execute("SELECT a.appid, a.name, a.purchase_price, a.genre, a.icon FROM store_app a;")
                else :
                    cursor.execute("SELECT a.appid,a.name,a.purchase_price, a.genre, a.icon FROM store_app a WHERE (name LIKE '%s' OR description LIKE '%s');" % ('%'+keywords+'%','%'+keywords+'%'))
            else:
                if keywords == '':
                    cursor.execute("SELECT a.appid, a.name, a.purchase_price, a.genre, a.icon FROM store_app a WHERE genre = '%s';" % genre)
                else :
                    cursor.execute("SELECT a.appid,a.name,a.purchase_price, a.genre, a.icon FROM store_app a WHERE genre = %r AND (name LIKE '%s' OR description LIKE '%s');" % (genre,'%'+keywords+'%','%'+keywords+'%'))                
            rows = cursor.fetchall() #return a list
            #rating implementation
            for app in rows: #app is a tuple
                appid = app[0]
                stars = calculate_rating(appid)
                is_purchased = False
                is_rent = False
                if request.user.is_authenticated():
                    userid = request.user.id
                    is_purchased = is_valid_purchase(appid, userid)
                    is_rent = is_valid_rent(appid, userid)
                random_picture = str(random.randint(51,70))
                rows_with_rating.append(app+(stars, is_purchased, is_rent, random_picture))
            SearchDone = True
            return render(request,'store/search.html',
                    {'search_form':search_form,'result':rows_with_rating,'SearchDone':SearchDone})
    else:
        search_form = SearchForm()
        return render(request,'store/search.html',{'search_form':search_form})
#<--SearchPage View

@login_required
def rate_review(request, user_name, orderid) :
    user = User.objects.get(username = user_name)

    if len(Purchased.objects.filter(order_id = orderid)[:])!= 0:
        order = Purchased.objects.get(order_id = orderid)
    else:
        order = Rent.objects.get(order_id = orderid)
    context_dict={}
    context_dict['order'] = order
    context_dict['username'] = user.username
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        review = request.POST.get('review')
        order.rating = rating
        order.review = review
        order.save()
        return HttpResponseRedirect('/store/')

    else:
        return render(request, 'store/review.html', context_dict)

def is_valid_rent(appid, userid):
    cursor = connection.cursor()
    cursor.execute("SELECT r.expire_date FROM store_rent r WHERE r.appid_id = %d AND r.userid_id = %d;" % (int(appid), int(userid)))
    for order in cursor.fetchall():
        if datetime.date.today() < order[0]:
            return True
    return False

def is_valid_purchase(appid, userid):
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM store_purchased p WHERE p.appid_id = %d AND p.userid_id = %d;" % (int(appid), int(userid)))
    return cursor.fetchone()[0] == 1

def calculate_rating(appid):
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*), SUM(r.rating) FROM store_rent r WHERE r.rating > 0 AND r.appid_id = %d; " % int(appid))
    rent = cursor.fetchone()
    cursor.execute("SELECT COUNT(*), SUM(p.rating) FROM store_purchased p WHERE p.rating > 0 AND p.appid_id = %d;" % int(appid))
    purchase = cursor.fetchone()
    if rent[0]+purchase[0] == 0:
        rating = 0
    elif rent[0] == 0:
        rating = int(int(purchase[1])/float(purchase[0]))
    elif purchase[0] == 0:
        rating = int(int(rent[1])/float(rent[0]))
    else:
        rating = int((int(rent[1]) + purchase[1])/float(rent[0]+purchase[0]))
    return rating*"x";

def is_rated(appid, userid):
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM store_rent r WHERE r.rating > 0 AND r.appid_id = %d AND r.userid_id = %d; " % (int(appid), int(userid)))
    rent = cursor.fetchone()
    cursor.execute("SELECT COUNT(*) FROM store_purchased p WHERE p.rating > 0 AND p.appid_id = %d AND p.userid_id = %d;" % (int(appid), int(userid)))
    purchase = cursor.fetchone()
    return rent[0]+purchase[0] > 0
