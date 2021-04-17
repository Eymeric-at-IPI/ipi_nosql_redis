from django.http import HttpResponse


def home(request):
	return HttpResponse("Home page, please go <a href='/redischat'>there</a>")
