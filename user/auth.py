from django.shortcuts import render_to_response
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.contrib.auth.models import User

def authenticate(view):
    verifier = AuthenticateUser(view)
    return verifier.authenticate

class AuthenticateUser:
  def __init__(self, method):
    self.view = method

  def authenticate(self, request, page_slug=None):
    self.request = request
    context = {}
    form = None
    user = None
    if request.session.get('user'):
      user = request.session['user']
    elif request.POST:
      form = LoginForm(request.POST)
      if form.is_valid():
        user = self.verifyAccount(form['username'].data, form['password'].data)
        if user:
            request.session['user'] = user
        else:
            form = None
            context['error'] = 'Incorrect password'
    
    if user:
        if page_slug:
            if user.has_access(page_slug):
                return self.view(request, page_slug)
        else:
            return self.view(request)
    
    if not form:
        form = LoginForm()
        action = request.META['PATH_INFO']
        context.update({'form': form, 'action_url': action})
        return render_to_response("login.html", RequestContext(request, context))

  def verifyAccount(self, username, password):
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            # change this to require separate login/signup workflow
            user = User(username=username,password=password)
            user.save()
            return user
        if password == user.password:
            return user
        else:
            return False
		
class LoginForm(forms.Form):
	username = forms.CharField(max_length=40)
	password = forms.CharField(max_length=40, widget=forms.PasswordInput)

		
