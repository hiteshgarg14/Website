from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from allauth.account.views import PasswordSetView, PasswordChangeView
from django.urls import reverse_lazy, reverse
from allauth.socialaccount.models import SocialAccount
from webapp.models import Event


def is_linkedin_connected(user):
	if user.is_authenticated and SocialAccount.objects.filter(user=user):
		return True
	return False


def home_page(request):
	linkedin_connected = is_linkedin_connected(request.user)
	return render(request, 'webapp/home_page.html',
			{'linkedin_connected': linkedin_connected})


@login_required
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect(reverse('webapp_home_page'))


@login_required
def profile(request):
	linkedin_connected = is_linkedin_connected(request.user)
	return render(request, 'webapp/profile.html',
			{'linkedin_connected': linkedin_connected})



def blog(request):
	return render(request, 'webapp/blog.html')


def event(request):
	events = Event.objects.all().order_by('-datetime')
	return render(request, 'webapp/events.html', {'events': events})

class CustomPasswordSetView(PasswordSetView):

	@property
	def success_url(self):
		return reverse_lazy('webapp_home_page')

	def render_to_response(self, context, **response_kwargs):
	    if self.request.user.has_usable_password():
	        return HttpResponseRedirect(reverse('webapp_home_page'))
	    return super(PasswordSetView, self).render_to_response(
	        context, **response_kwargs)



class CustomPasswordChangeView(PasswordChangeView):
	@property
	def success_url(self):
		return reverse_lazy('webapp_home_page')


custom_password_change = login_required(CustomPasswordChangeView.as_view())
custom_password_set = login_required(CustomPasswordSetView.as_view())
