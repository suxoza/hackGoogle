import http.client, urllib.parse, json, requests, socket, ssl

from helpers.proxy import getProxy
from helpers.parseGoogleHtml import parseHTML

try:
	ssl._create_default_https_context = ssl._create_unverified_context
except Exception as e:
	print(e)


class Auth:

	_proxy 	 = {}
	_host 	 = "accounts.google.com"	
	_headers = {} 
	_params  = {}
	_cookie  = {}
	conn 	 = False
	_regUrl  = "/signup/v2?flowName=GlifWebSignIn&amp;flowEntry=SignUp"
	_regActionUrl = "/_/signup/accountdetails?hl=ka&_reqid=70475&rt=j"
	wichProxy = False

	def __init__(self):
		self.prepareRequest()
		self.proxy()
		

		#auth page
		self.getRegistrationPage()
		#self.registrationAction()

	def __del__(self): 
		if self.conn:
			self.conn.close()

	def proxy(self, force = False):
		if self.wichProxy:
			self._proxy = getProxy(force)
			self.initConnection()
		else:
			self.initWithoutProxyConnection()

	def initWithoutProxyConnection(self):
		self.conn = http.client.HTTPSConnection(self._host, 443, timeout = 30)

	def initConnection(self):
		self.conn = http.client.HTTPSConnection(self._proxy.proxyIP, self._proxy.proxyPORT, timeout = 30)
		self.conn.set_tunnel(self._host)

	def sendRequest(self, method, url):
		try:
			if method == 'POST':
				self.conn.request(method, url, urllib.parse.urlencode(self._params), self._headers)
			else:
				self.conn.request(method, url)
		#except (http.client.RemoteDisconnected, socket.error) as e:
		except Exception as e:
			print("force run...", str(e), "\n")
			self.proxy(True)
			return self.sendRequest(method, url)


	def registrationAction(self):
		print("---call method: registrationAction")
		self._headers['Cookie'] = 'GAPS='+self._cookie['GAPS']
		self._headers['Referer'] = "https://{0}{1}".format(self._host, self._regUrl)

		postData = {
			'name': 'someUniqueName',
			'lastName': 'someLastName',
			'email': 'someUniqueEmail1234',
			'password': 'somePassword1234'
		}
		postData['someBoolValue'] =  bool(1)

		kk = ['name','lastName','name','lastName','email','password','email', 'someBoolValue']
		for i in kk:
			self._params['f.req'].append(postData[i])
		self._params['f.req'] = json.dumps(self._params['f.req'])

		print(self._params['f.req'])
		#return

		print("----headers")
		print(self._headers)
		print('---params')
		print(self._params)
		print("---f.req")

		self.sendRequest("POST", self._regActionUrl)	
		r1 = self.conn.getresponse()
		print(r1.status, r1.reason)
		print(r1.read().decode("utf_8"))
		#r1 = self.conn.getCookie()



	def getRegistrationPage(self):
		print("---call method: getRegistrationPage")
		self.sendRequest("GET", self._regUrl)				
				
		r1 = self.conn.getresponse()
		rdr = r1.read().decode("utf_8")
		if r1.status != 200:
			self.proxy(True)
			return self.getRegistrationPage()

		print(r1.status, r1.reason)
		
		params = parseHTML(rdr)
		self._params['f.req'] = params.params['f.req']
		self._params['azt'] = params.params['azt']


		
		self.getCookie(r1.headers)
	

		self.registrationAction()
		#print(self._headers)

	def getCookie(self, headers):
		for i,v in headers.items():
			if i == 'Set-Cookie':
				fKey = v.split(";")
				for itr in fKey:
					sKey = itr.split("=")
					try:
						self._cookie[sKey[0]] = sKey[1]
					except:
						self._cookie[sKey[0]] = ''
				break
		

	def connection(self):
		pass

	def prepareRequest(self):
		self._params = {
		   "flowName":"GlifWebSignIn",
		   "flowEntry":"SignUp",
		   "continue":"https://accounts.google.com/ManageAccount",
		   "cookiesDisabled":"false",
		   "deviceinfo":"[null,null,null,[],null,\"EN\",null,null,[],\"GlifWebSignIn\",null,[null,null,[],null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,[],null,null,null,[],[]]]",
		   "gmscoreversion":"undefined",
		   "":""
		}

		self._headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
            "X-Same-Domain": "1",
            "Google-Accounts-XSRF": "1",
            "TE": "Trailers",
            "Host": self._host,
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0"
        }




if __name__ == '__main__':
	Auth()