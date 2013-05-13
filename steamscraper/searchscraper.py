import urllib2
from HTMLParser import HTMLParser

def scrapeSearchPage(url):
	html = urllib2.urlopen(url).read().decode('utf-8')
	html = html[html.index('<!-- List Items -->'):html.index('<!-- End List Items -->')]
	parser = SearchPageScraper()
	parser.feed(html)
	entries = parser.getEntries()
	parser.close()
	return entries

# parses an entry on the search page into a dict containing pertinent info
class SearchPageScraper(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.entryStart = False
		self.foundName = False
		self.foundPrice = False
		self.foundScore = False
		self.foundReleased = False
		self.entryEnd = False
		self.currEntry = {}
		self.entries = []

	def handle_starttag(self, tag, attrs):
		if tag == 'a' and len(attrs) > 1:
			if attrs[1][1] == 'search_result_row even' or attrs[1][1] == 'search_result_row odd':
				url = attrs[0][1]
				if 'app' in url:
					self.currEntry = {}
					self.currEntry['url'] = attrs[0][1][:attrs[0][1].index('?')]
					self.currEntry['appid'] = int(attrs[0][1][attrs[0][1].index('app/') + len('app/'):attrs[0][1].index('/?')])
					self.entryStart = True
		if self.entryStart:
			if tag == 'img' and len(attrs) > 1:
				if attrs[0][0] == 'src':
					image = attrs[0][1]
					if 'capsule' not in image:
						self.currEntry = {}
						self.entryStart = False
					else:
						self.currEntry['image'] = image
				elif attrs[0][0] == 'class' and attrs[0][1] == 'platform_img':
					if 'platforms' not in self.currEntry:
						self.currEntry['platforms'] = []
					platform = attrs[1][1][attrs[1][1].index('platform_') + len('platform_'):attrs[1][1].index('.png')]
					if platform == 'steamplay_only':
						platform = 'Steamplay'
					elif platform == 'win':
						platform = 'Windows'
					elif platform == 'mac':
						platform = 'Mac'
					elif platform == 'linux':
						platform = 'Linux'
					self.currEntry['platforms'].append(platform)
			elif tag == 'h4':
				self.foundName = True
			elif tag == 'div':
				if len(attrs) > 0  and attrs[0][0] == 'class' and attrs[0][1] == 'col search_price':
					self.foundPrice = True
				elif len(attrs) > 0 and attrs[0][0] == 'class' and attrs[0][1] == 'col search_metascore':
					self.foundScore = True
				elif len(attrs) > 0 and attrs[0][0] == 'class' and attrs[0][1] == 'col search_released':
					self.foundReleased = True
				elif len(attrs) > 0 and attrs[0][0] == 'style' and attrs[0][1] == 'clear: both;':
					self.entryEnd = True

	def handle_endtag(self, tag):
		if self.foundName:
			self.foundName = False
		if self.foundPrice:
			self.foundPrice = False
		if self.foundScore:
			self.foundScore = False
		if self.foundReleased:
			self.foundReleased = False
		if self.entryEnd:
			self.entryend = False
			if self.currEntry:
				for entry in self.entries:
					if self.currEntry == entry:
						return
				self.entries.append(self.currEntry)
			
	def handle_data(self, data):
		if self.foundName:
			name = data.strip()
			self.currEntry['name'] = data.strip()
		if self.foundPrice:
			self.currEntry['price'] = data.strip()
		if self.foundScore:
			self.currEntry['score'] = int(data.strip())
		if self.foundReleased:
			self.currEntry['released'] = data.strip()
		
	def getEntries(self):
		return self.entries