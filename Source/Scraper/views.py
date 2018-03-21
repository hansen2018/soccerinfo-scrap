from django.shortcuts import render
from Scraper.funcs import *

# Create your views here.
def mining(request):
	if request.method == 'POST':
		startScraping()
		loading = 1
		return render(request, 'mining.html', {'loading' : loading})
	else:
		loading = 0
	return render(request, 'mining.html', {'loading' : loading})

def view(request):
	competitions = Competitions.objects.all()
	matches = Matches.objects.all()
	leagues = Leagues.objects.all()
	return render(request, 'view.html', {'competitions':competitions, 'matches':matches, 'leagues':leagues})