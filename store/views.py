from django.shortcuts import render
from store.forms import UserForm
from django.contrib.auth.models import User
from django.views import generic

class IndexView(generic.ListView):
    template_name = 'store/index.html'

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

