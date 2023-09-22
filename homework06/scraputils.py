import requests 
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []

    lst = parser.body.table.findAll('table')[1].findAll('tr')
    
    i = 0
    while (i < len(lst)-2):
        temp1= lst[i].findAll('td')[2].findAll('a')
        title_s = temp1[0].text
        url_s = ""
        if(len(temp1) == 2):
            url_s = temp1[1].text

        temp2 = lst[i+1].findAll('td')[1].span
        points_s = temp2.span.text[0]
        
        temp3 = temp2.findAll('a')
        author_s = temp3[0].text
        comments_s = temp3[4].text

        if(comments_s == "discuss"):
            comments_s = 0
        else:
            comments_s = int(comments_s[0])

        news_list.append(dict(author = author_s, comments = comments_s, points = points_s, title = title_s, url = url_s))

        i+=3

    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    lst = parser.body.table.findAll('table')[1].findAll('tr')
    n = len(lst)-1

    return(lst[n].findAll('td')[1].a.get('href'))


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news

'''if __name__ == "__main__":
    get_news("https://news.ycombinator.com/newest", 1)'''

    


