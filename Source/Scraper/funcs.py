
from Scraper.models import *

# ----------------------------------------
# scraping utility consts
# ----------------------------------------
import time
import datetime
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

base_url = 'http://www.futbol24.com'

# ----------------------------------------
# scraping start function
# ----------------------------------------
def startScraping():
	scraping_international()
	scraping_national()

# ----------------------------------------
# scraping international competition kinds
# ----------------------------------------
def scraping_international():
	time.sleep(5)
	uClient = uReq(base_url)
	page_html = uClient.read()
	uClient.close()

	page_soup = soup(page_html, "html.parser")

	kindDiv = page_soup.find("div", {"class":"international"})
	kindUl = kindDiv.ul
	kindlis = kindUl.findAll("li")

	for kindli in kindlis:
		href = kindli.a["href"]
		kind = kindli.find("a").text

	scraping_titles(0, kind, href)

# ----------------------------------------
# scraping national competition kinds
# ----------------------------------------
def scraping_national():
	time.sleep(5)
	uClient = uReq(base_url)
	page_html = uClient.read()
	uClient.close()

	page_soup = soup(page_html, "html.parser")

	kindDiv = page_soup.find("div", {"class":"national"})
	kindUl = kindDiv.ul
	kindlis = kindUl.findAll("li")

	for kindli in kindlis:
		href = kindli.a["href"]
		kind = kindli.find("a").text

	scraping_titles(1, kind, href)

# ----------------------------------------
# scraping competition title
# ----------------------------------------
def scraping_titles(league, kind, kindhref):
	site_url = base_url + kindhref
	time.sleep(5)
	uClient = uReq(site_url)
	page_html = uClient.read()
	uClient.close()

	page_soup = soup(page_html, "html.parser")
	titleSel = page_soup.find("select", {"class":"gray1"})
	titleopts = titleSel.findAll("option")

	for titleopt in titleopts:
		href = titleopt["value"]
		title = titleopt.text

	scraping_session(league, kind, title, href)

# ----------------------------------------
# scraping competition session
# ----------------------------------------
def scraping_session(league, kind, title, titlehref):
	site_url = base_url + titlehref
	time.sleep(5)
	uClient = uReq(site_url)
	page_html = uClient.read()
	uClient.close()

	page_soup = soup(page_html, "html.parser")

	sessionSel = page_soup.find("select", {"class":"gray2"})
	sessionopts = sessionSel.findAll("option")

	for sessionopt in sessionopts:
		href = sessionopt["value"]
		session = sessionopt.text

	save_competitions(league, kind, title, session, href)

# ----------------------------------------
# save competition main infos
# ----------------------------------------
def save_competitions(league, kind, title, session, sessionhref):
	try:
		competition = Competitions.objects.get(league = league, kind = kind, title = title, session = session)
	except Competitions.DoesNotExist:
		competition = Competitions(league = league, kind = kind, title = title, session = session)
		competition.save()

	scraping_matchresult(competition.id, league, sessionhref)

# ----------------------------------------
# scraping competition results
# ----------------------------------------
def scraping_matchresult(competeid, league, sessionhref):
	site_url = base_url + sessionhref + "results"
	time.sleep(5)
	uClient = uReq(site_url)
	page_html = uClient.read()
	uClient.close()

	page_soup = soup(page_html, "html.parser")

	pagination = page_soup.find("p", {"class":"pagination"})
	pagespans = pagination.findAll("span")
	maxmatch = int(pagespans[2].text)
	permatch = int(pagespans[1].text)
	curpage = 0

	while True:
		if curpage != 0:
			sub_url = site_url + "/?Ajax=1&statLR-Page=" + str(curpage)

			time.sleep(5)
			uClient = uReq(sub_url)
			page_html = uClient.read()
			uClient.close()
			page_soup = soup(page_html, "html.parser")

		resultDiv = page_soup.find("div", {"class":"loadingContainer"})
		resulttrs = resultDiv.findAll("tr", {"class":"status5"})

		for resulttr in resulttrs:
			resulttds = resulttr.findAll("td")
			if league == 0:
				dateSec = resulttds[0];
				hTeamSec = resulttds[2];
				scoreSec = resulttds[3];
				aTeamSec = resulttds[4];
			else:
				dateSec = resulttds[0];
				hTeamSec = resulttds[1];
				scoreSec = resulttds[2];
				aTeamSec = resulttds[3];
			scores = scoreSec.text.split("-")

		save_leaguenames(hTeamSec.a["href"], aTeamSec.a["href"], hTeamSec.text, aTeamSec.text)
		save_matches(competeid, dateSec["data-dymek"], hTeamSec.text, aTeamSec.text, scores[0], scores[1], scoreSec.a["href"])

		curpage += 1
		if permatch*curpage >= maxmatch:
			break

# ----------------------------------------
# save match infos
# ----------------------------------------
def save_matches(competeid, matchdate, hteam, gteam, hscore, gscore, scorehref):
	site_url = base_url + scorehref
	time.sleep(5)
	uClient = uReq(site_url)
	page_html = uClient.read()
	uClient.close()

	page_soup = soup(page_html, "html.parser")

	hactionTrs = page_soup.findAll("tr", {"class":"haction"})
	gactionTrs = page_soup.findAll("tr", {"class":"gaction"})

	homescores = ""
	guestscores = ""

	for hactionTr in hactionTrs:
		status = hactionTr.find("td", {"class":"status"})
		if homescores == "":
			homescores = status.text
		else:
			homescores = homescores + "," + status.text

	for gactionTr in gactionTrs:
		status = gactionTr.find("td", {"class":"status"})
		if guestscores == "":
			guestscores = status.text
		else:
			guestscores = guestscores + "," + status.text

	dt = datetime.datetime.strptime(matchdate, '%d.%m.%Y %H:%M').strftime('%Y-%m-%d %H:%M')
	try:
		matche = Matches.objects.get(matchno = competeid, date = dt, hteam = hteam, gteam = gteam, hscore = hscore, gscore = gscore)
	except Matches.DoesNotExist:
		matche = Matches(matchno = competeid, date = dt, hteam = hteam, gteam = gteam, hscore = hscore, gscore = gscore)
		matche.save()

# ----------------------------------------
# save country name
# ----------------------------------------
def save_leaguenames(hcountry, gcountry, hteam, gteam):
	hcname = hcountry.split("/")
	gcname = gcountry.split("/")

	try:
		league = Leagues.objects.get(cname = hcname[2], lname = hteam)
	except Leagues.DoesNotExist:
		league = Leagues(cname = hcname[2], lname = hteam)
		league.save()

	try:
		league = Leagues.objects.get(cname = gcname[2], lname = gteam)
	except Leagues.DoesNotExist:
		league = Leagues(cname = gcname[2], lname = gteam)
		league.save()