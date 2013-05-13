import urllib2
from HTMLParser import HTMLParser

def scrapeGamePage(url):
	html = urllib2.urlopen(url).read().decode("latin1")
	parser = GamePageScraper()
	parser.feed(html)
	info = parser.getGameInfo()
	parser.close()
	return info

# parses an html Steam game webpage into a dictionary containing basic info
class GamePageScraper(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.foundName = False
		self.foundDescription = False
		self.foundPrice = False
		self.foundScore = True
		self.gameInfo = {}
	def handle_starttag(self, tag, attrs):
		if tag == 'span':
			if len(attrs) > 0 and attrs[0][0] == 'itemprop' and attrs[0][1] == 'name':
				self.foundName = True
		elif tag == 'div':
			if len(attrs) > 0  and attrs[0][0] == 'class' and attrs[0][1] == 'game_description_snippet':
				self.foundDescription = True
			elif len(attrs) > 1 and attrs[1][0] == 'itemprop' and attrs[1][1] == 'price':
				self.foundPrice = True
			elif len(attrs) > 0 and attrs[0][0] == 'id' and attrs[0][1] == 'game_area_metascore':
				self.foundScore = True
	def handle_endtag(self, tag):
		if self.foundName:
			self.foundName = False
		if self.foundDescription:
			self.foundDescription = False
		if self.foundPrice:
			self.foundPrice = False
		if self.foundScore:
			self.foundScore = False
	def handle_data(self, data):
		if self.foundName:
			self.gameInfo['name'] = data.strip()
		if self.foundDescription:
			self.gameInfo['description'] = data.strip()
		if self.foundPrice:
			if len(data.strip()) != 0:
				self.gameInfo['price'] = data.strip()
		if self.foundScore:
			if len(data.strip()) != 0:
				self.gameInfo['score'] = data.strip()
	def getGameInfo(self):
		return self.gameInfo