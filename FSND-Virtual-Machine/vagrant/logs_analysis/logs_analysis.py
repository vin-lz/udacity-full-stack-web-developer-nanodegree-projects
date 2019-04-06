#!/usr/bin/env python3






import psycopg2

DBNAME="news"

def get_popular_articles():
    """Return the most popular articles with numbers of views from 'news', descending order."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""SELECT articles.title, COUNT(*) AS num FROM articles, log 
        WHERE log.path LIKE '%' || articles.slug 
        GROUP BY articles.title 
        ORDER BY num DESC LIMIT 3;""")
    popular_articles = c.fetchall()
    db.close()
    print("===================================================")
    print("1. What are the most popular three articles of all time?")
    for item in popular_articles:
        print(u"\u2022 " + item[0].title() + " — " + str(item[1]) + " views")
    return


def get_popular_authors():
    """Return the most popular authors with numbers of views from 'news', descending order."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""SELECT authors.name, SUM(popular_articles.num) AS t_num FROM (SELECT articles.title, COUNT(*) AS num FROM articles, log WHERE log.path LIKE '%' || articles.slug 
        GROUP BY articles.title) as popular_articles, articles, authors 
        WHERE popular_articles.title=articles.title AND authors.id=articles.author 
        GROUP BY authors.name 
        ORDER BY t_num DESC;""")
    popular_articles = c.fetchall()
    db.close()
    print("===================================================")
    print("2. Who are the most popular article authors of all time?")
    for item in popular_articles:
        print(u"\u2022 " + item[0] + " — " + str(item[1]) + " views")
    return

get_popular_authors()