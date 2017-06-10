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

    named_tokens={}  # dict. of named tokens
    for i in range(5): # for 50 search results
        r=s.get("https://www.google.com/search", params=params)
        soup = BeautifulSoup(r.content,'lxml')
        soup=soup.findAll('h3', {'class': 'r'})
        params['start']+=10 # every page consists of 10 results
        
        for text in soup:
        # iterate through titles
            for text2 in text.a.contents:
                # all text titles in text2
                li=nltk.word_tokenize(text2.string.encode('utf-8'))
                tagged = nltk.pos_tag(li)
                namedEnt = nltk.ne_chunk(tagged)
                for text3 in namedEnt:
                    if(type(text3))==nltk.tree.Tree:
                        if text3[0][0] in named_tokens:
                            named_tokens[text3[0][0]]+=1
                        else:
                            named_tokens[text3[0][0]]=1
            
    return named_tokens
    


@app.route('/')
def search():
    return render_template('index.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method=='POST':
        q= request.form
	result= sorted(scrape(q['query']).items(), key = lambda x:x[1], reverse = True)
	return render_template("result.html",result=result)


if __name__ == '__main__':
    app.run(debug = True)
    app.run(host='0.0.0.0', port=5001)
