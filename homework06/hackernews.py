from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier
import string
model = NaiveBayesClassifier(1, ['good', 'never'])

def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)

def learn():
    s = session()
    rows = s.query(News).filter(News.label != None).all()
    x, y = [], []
    for i in rows:
        x.append(i.title + ' ' + i.author)
        y.append(i.label)
    x = [clean(i).lower() for i in x]
    '''
    n = len(x)
    X_train, Y_train = x[:(n*90//100)], y[:(n*90//100)]
    X_test, Y_test = x[(n*90//100):], y[(n*90//100):]
    '''
    X_train, Y_train = x, y
    
    model.fit(X_train, Y_train)
    #print(model.score(X_test, Y_test), "\n\n")

@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    # PUT YOUR CODE HERE
    label = request.GET.get('label')
    ID = request.GET.get('id')

    s = session()
    row = s.query(News).get(ID)

    #print("!!!!!!  ", row.title, '\n')
    row.label = label
    s.add(row)
    s.commit()

    #print(label, ' ', ID)

    redirect("/news")


@route("/update")
def update_news():
    
    pageCount = 1
    #newsCount = pageCount * 30

    new_news = (get_news("https://news.ycombinator.com/newest", pageCount))
    
    s = session()
    old_news = s.query(News).order_by(News.id).limit(1).all()
    #print(old_news[0].title)
    sample_string = old_news[0].title+old_news[0].author

    for i in new_news:
        temp_str = i['title']+i['author']
        if(temp_str != sample_string):
            news = News(title = i['title'], author = i['author'], url = i['url'], comments = i['comments'], points = i['points'])
            s.add(news)
        else:
            break

    s.commit()
    redirect("/news")
    
@route("/classify")
def classify_news():
    # PUT YOUR CODE HERE
    learn()
    s = session()
    classified_news = s.query(News).filter(News.label == None).all()
    for i in classified_news:
        x = clean((i.title + ' ' + i.author)).lower()
        label = model.predict(x)
        i.label = label
        s.add(i)
    
    print(type(classified_news))
    #s.add(classified_news)
    s.commit()
    pass

@route('/recommendations')
def recommendations():
    # 1. Получить список неразмеченных новостей из БД
    # 2. Получить прогнозы для каждой новости
    # 3. Вывести ранжированную таблицу с новостями

    learn()
    s = session()
    classified_news = s.query(News).filter(News.label == None).all()
    for i in classified_news:
        x = clean((i.title + ' ' + i.author)).lower()
        label = model.predict(x)
        i.label = label
        #print(i.title, ' ', i.label, "\n\n")
    
    return template('news_recommendations', rows=classified_news)

if __name__ == "__main__":
    run(host="localhost", port=8080)
