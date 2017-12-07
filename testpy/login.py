
# -*- coding:utf-8 -*-
#Build-in /Std
import os,sys,time,platform,random
import re,json,cookielib
#requirements
import requests

s=requests.session()
requests.cookies=cookielib.LWPCookieJar('cookies')

try:
	requests.cookies.load(ignore_discard=True)
except:
	pass


class LoginPasswordError(Exception):
	def __init__(self, message):
		if type(message) != type("") or message == "":
			self.message = u"account or password error"
		else:
			self.message = message
		print(self.message)

class NetworkError(Exception):
	def __init__(self, message):
		if type(message) != type("") or message == "":
			self.message = u"network error"
		else: self.message = message
		print(self.message)
class AccountError(Exception):
	def __init__(self, message):
		if type(message) != type("") or message == "":
			self.message = u"account type error"
		else:
			self.message = message
		print(self.message)

def download_captcha():
	url="http://www.zhihu.com/captcha.gif"
	r = s.get(url,params={"r":random.random()})
	if int(r.status_code)!=200:
		raise NetworkError(u"request captcha error")
	image_name=u"verify."+r.headers['content-type'].split("/")[1]
	open(image_name,"wb").write(r.content)

	print(u"正在调用外部程序渲染验证码....")

	captcha_code=raw_input("please enter captcha: ")
	return captcha_code

def search_xsrf():
	url="http://www.zhihu.com"
	r=requests.get(url)
	if int(r.status_code)!=200:
		raise NetworkError(u" requestcaptcha network error")
	results=re.compile(r"\<input\stype=\"hidden\"\sname=\"_xsrf\"\svalue=\"(\S+)\"",re.DOTALL).findall(r.text)
	if len(results)<1:
		print(u"can not get XSRF")
		return None
	return results[0]

def build_form(account,password):
	account_type="email"
	if re.match(r"^\d{11}$",account):
		account_type="phone"
	elif re.match(r"^\S+\@\S+\.\S+$",account):
		account_type="email"
	else:
		raise  AccountError(u"account type error")
	form={account_type:account,"password":password,"remember_me":'true'}
	form['_xsrf']=search_xsrf()

	print("XSRF is %s" %form['_xsrf'])
	form['captcha']=download_captcha()
	print(form['captcha'])
	return form

def upload_form(form):
	url="http://www.zhihu.com/login/email"
	headers = {
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36",
        'Host': "www.zhihu.com",
        'Origin': "http://www.zhihu.com",
        'Pragma': "no-cache",
        'Referer': "http://www.zhihu.com/",
        'X-Requested-With': "XMLHttpRequest"
    }
	r=s.post(url,data=form,headers=headers)
	if int(r.status_code)!=200:
		raise  NetworkError(u"upload form failed")

	if r.headers['content-type'].lower() =="application/json":
		result=r.json()
		print(result)
		if result["r"]==0:
			print(u"login success")
			return{"result":True}
		elif result["r"]==1:
			print(u"login failed")
			return {"error": {"code": int(result['errcode']), "message": result['msg'], "data": result['data'] } }
		else:
			print(u"unknow form data error:\n \t %s") %(str(result))
			return {"error": {"code": -1, "message": u"unknow error"} }
	else:
		print(u"can not get the server content: \n \t %s " % r.text )
		return {"error": {"code": -2, "message": u"parse error"} }
def isLogin():
	url="http://www.zhihu.com/settings/profile"
	r=s.get(url,allow_redirects=False)
	status_code=int(r.status_code)
	if status_code==301 or status_code==302:
		return False
	elif status_code==200:
		return True
	else:
		print(u"network error")
		return None

def login(account=None,password=None):
	if isLogin() ==True:
		print(u"you have logined")
		return None
	if account==None:
		account =raw_input("enter account: ")
		password=raw_input("enter password: ")

	form_data=build_form(account,password)

	result=upload_form(form_data)

	if "error" in result:
		if result["error"]['code'] ==1991829:
			print(u"captcha error，please input again")
			return login()
		else:
			print(u"Unknow error")
			return False
	elif "result" in result and result['result']==True:
		print(u"login success")
		requests.cookies.save()
		return True

if __name__=="__main__":
	login()
