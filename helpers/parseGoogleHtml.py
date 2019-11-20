from bs4 import BeautifulSoup
import asyncio, re

class parseHTML:


	def __init__(self, source = False):
		self.source = source
		self.params = {}
		self.init()
		
		
	def init(self):
		if not self.source:
			with open("googleFromPython.html") as r:
				self.source = r.read()
		self.parse()
		
	def parse(self):
		self.soup = BeautifulSoup(self.source, "html.parser")
		self.getAzt()
		self.getFReq()
		print(self.params)

	def getFReq(self):
		td = self.soup.find("div", {"id":"view_container"}).attrs['data-initial-setup-data'].replace("null,",'')
		attr = re.split(r'[^\w^a-zA-Z0-9\_\-\:\s\.\,]', td)
		attr = list([x for x in attr if x != '' and len(x.strip()) > 10])[0]
		self.params['f.req'] = []
		self.params['f.req'].append(attr)


	def getAzt(self):
		forAzt = self.soup.find('script', {'data-id': "_gd"}).text.split('"OewCAd":')[1].split('"Qzxixc"')[0]
		forAzt = re.split(r'[^\w^a-zA-Z0-9\_\-\:\s\.\,]', forAzt)
		forAzt = list([x for x in forAzt if x != '' and len(x.strip()) > 10])[0]
		
		self.params['azt'] = forAzt

if __name__ == '__main__':
	parseHTML()