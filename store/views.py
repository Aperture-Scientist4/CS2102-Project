from django.shortcuts import render
from store.forms import UserForm
from store.forms import SearchForm
from store.forms import RentForm,FeedbackForm,AppEditForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect, HttpResponse
from django.db import connection
from store.models import Purchased, Rent, App



def indexView(request):
    return render(request, 'store/index.html', {})

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
            print ("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login!")

    else:

        return render(request, 'store/login.html', {})


@login_required
def restricted(request, user_name):
	user = User.objects.get(username = user_name)
	context_dict = {}
	context_dict['username'] = user.username
	app_list_purchased = Purchased.objects.filter(userid_id = user.id)[:]
	app_list_rent = Rent.objects.filter(userid_id = user.id)[:]
	'''
	app_list = Purchased.objects.raw('SELECT * FROM store_purchased WHERE user= %s' , [user.username])

	app_list.append(Rent.objects.raw('SELECT * FROM store_rent WHERE user= %s' , [user.username]))
	'''
	context_dict['app_list_purchased'] = app_list_purchased
	context_dict['app_list_rent'] = app_list_rent

	return render(request, 'store/restricted.html', context_dict)

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
<<<<<<< HEAD
        return render(request, 'store/restricted/changePassword.html', {})
#ProdcutPage views-->
def ProductEdit(request, product_id):
    if request.method == 'POST':
        form = AppEditForm()
    else:
        return render(request,'store/AppEdit.html',{'form':form})
def ProductPage(request, product_id):
    rentForm = RentForm()
    feedbackForm = FeedbackForm()
    purchased = False
    othersRating = [('Elephant','1','Badddddd!'),('Rabbit','5','Exxxxceeeeelllenttttt!'),]
    appData = ['1','ProductPage','haha','wahaha','hahahaha','some','any','most']
    return render(request,'store/product.html',{'appData':appData,'purchased':purchased,
                                                'feedbackForm':feedbackForm,
                                                'rentForm':rentForm,'othersRating':othersRating})

def ProductPurchase(request, product_id):
    if request.method == 'POST':
        a = 1        
    return HttpResponseRedirect('/store/product/'+product_id)

def ProductRent(request, product_id):
    if request.method == 'POST':
        rentForm = RentForm(request.POST)
        if rentForm.is_valid():
            a = 1
    return HttpResponseRedirect('/store/product/'+product_id)

def ProductFeedback(request, product_id):
    if request.method == 'POST':
        feedbackForm = FeedbackForm(request.POST)
        if feedbackForm.is_valid():
            a = 1
    return HttpResponseRedirect('/store/product/'+product_id)

def ErrorPage(request):
    return HttpResponse("<H1>ERROR!</H1>")

#<--ProdcutPage view

#SearchPage View-->
def create_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        cursor = connection.cursor()
        cursor.execute('SELECT db.appid,db.name,db.purchase_price,db.device FROM mockDB db;')
        rows = cursor.fetchall()
        if form.is_valid():
            SearchDone = True
            return render(request,'store/search.html',
                    {'form':form,'result':rows,'SearchDone':SearchDone,
                     'SearchName':form.cleaned_data['keyword'],
                     'SearchGenre':form.cleaned_data['types']})
    else:
        form = SearchForm()
        return render(request,'store/search.html',{'form':form})
#<--SearchPage View
=======
        return render(request, 'store/changePassword.html', context_dict)

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
      

>>>>>>> origin/master
