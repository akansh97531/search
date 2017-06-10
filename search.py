from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
import nltk

app = Flask(__name__)


def scrape(query):
    s=requests.Session()
    params = {
	'q': query,
	'start': 0,
    }
    headers = {
	'User Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) \
	Gecko/20100101 Firefox/53.0'
    }
    r=s.get("https://www.google.com/search", params=params)
    soup = BeautifulSoup(r.content)
    soup=soup.findAll('h3', {'class': 'r'})
    tokens={}
    for text in soup:
        for text2 in text.a.contents:
            # all text titles in text2
            li=nltk.work_tokenize(text2.string)
            for text3 in li:
                if text3 in tokens:
                    tokens[text3]=0
                else:
                    tokens[text3]+=1
            
    print(tokens)
    return tokens
    


@app.route('/')
def search():
    return render_template('index.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method=='POST':
        q= request.form
	print (q['query'])
	result= scrape(q['query'])
        print(result)
	return render_template("result.html",result=q)


if __name__ == '__main__':
    app.run(debug = True)
    app.run(host='0.0.0.0', port=5000)
