from flask import Flask,request,jsonify
import requests

s = requests.Session()
# Am nevoie de cookie-ul ăsta pentru a putea accesa site-ul
s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'


def get_category_list(category_id):
    return "https://www.listafirme.ro/" + str(category_id) + "/d1.htm"



app = Flask(__name__)


#print(s.get(get_category_list(16)))
try:
    req = s.get(get_category_list(16))
    print(req.text)
except:
    print("error")

# print(requests.get("https://www.listafirme.ro/"))
