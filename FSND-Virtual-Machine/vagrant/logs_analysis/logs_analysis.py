#!/usr/bin/env python3

import psycopg2

DBNAME = "news"


def get_popular_articles():
    """Return the most popular articles with numbers of views from 'news',
    descending order."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""SELECT articles.title, COUNT(*) AS num FROM articles, log
        WHERE log.path LIKE '%' || articles.slug
        GROUP BY articles.title
        ORDER BY num DESC LIMIT 3;""")
    popular_articles = c.fetchall()
    db.close()
    print("=============================================================")
    print("1. What are the most popular three articles of all time?")
    for item in popular_articles:
        print(u"\u2022 " + item[0].title() + " — " + str(item[1]) + " views")
    print("=============================================================")
    return


def get_popular_authors():
    """Return the most popular authors with numbers of views from 'news',
    descending order."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""SELECT authors.name, SUM(popular_articles.num) AS t_num
        FROM (SELECT articles.title, COUNT(*) AS num FROM articles, log
        WHERE log.path LIKE '%' || articles.slug
        GROUP BY articles.title) as popular_articles, articles, authors
        WHERE popular_articles.title = articles.title
        AND authors.id = articles.author
        GROUP BY authors.name
        ORDER BY t_num DESC;""")
    popular_articles = c.fetchall()
    db.close()
    print("=============================================================")
    print("2. Who are the most popular article authors of all time?")
    for item in popular_articles:
        print(u"\u2022 " + item[0] + " — " + str(item[1]) + " views")
    print("=============================================================")
    return


def get_error_dates():
    """Return the dates and error rates when more than 1% of requests led
    to errors occurs from 'news'."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""SELECT total.dates,
        ROUND(CAST(errors.num::Float / total.num * 100 AS NUMERIC),2) FROM
        (SELECT DATE(time) as dates, COUNT(*) AS num FROM log
        WHERE status!='200 OK' GROUP BY DATE(time)) AS errors,
        (SELECT DATE(time) as dates, COUNT(*) AS num FROM log
        GROUP BY DATE(time)) AS total
        WHERE errors.dates = total.dates
        AND errors.num::float / total.num > 0.01;""")
    popular_articles = c.fetchall()
    db.close()
    print("=============================================================")
    print("3. On which days did more than 1% of requests lead to errors?")
    for item in popular_articles:
        print(u"\u2022 " + str(item[0]) + " — " + str(item[1]) + "% errors")
    print("=============================================================")
    return


get_popular_articles()
get_popular_authors()
get_error_dates()
