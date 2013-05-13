import json
import urllib2
import datetime
from searchscraper import scrapeSearchPage

class SteamScraper():
	def __init__(self):
		self.entries = []
		numPages = self.findNumberOfPages()
		for i in xrange(numPages):
			url = 'http://store.steampowered.com/search/results?sort_by=Name&sort_order=ASC&category1=998&page=' + str(i+1)
			print 'Processing page ' + str(i+1) + ' of ' + str(numPages) + '...'
			self.entries += scrapeSearchPage(url)
		
	def findNumberOfPages(self):
		url = 'http://store.steampowered.com/search/results?sort_by=Name&sort_order=ASC&category1=998&page=1' 
		html = urllib2.urlopen(url).read()
		html = html[html.index('<div class="search_pagination_left">')+36:]
		html = html[:html.index('</div>')].strip()
		numEntries = int(html[html.index('of')+3:])
		numPages = numEntries / 25 + 1
		return numPages

	def outputJSON(self, location):
		output = {}
		output['last_updated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
		output['game_count'] = len(self.entries)
		output['games'] = self.entries
		output = json.dumps(output, indent=4).encode('utf-8')
		with open(location, "w") as f:
			f.write(output)