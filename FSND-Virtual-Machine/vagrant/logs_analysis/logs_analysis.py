#!/usr/bin/env python3






import psycopg2

DBNAME="news"

def get_popular_articles():
    """Return all posts from the 'database', most recent first."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT path, COUNT(*) AS num FROM log WHERE status='200 OK' AND path LIKE '/article/%' GROUP BY path ORDER BY num DESC LIMIT 3;")
    populer_articles = c.fetchall()
    db.close()
    print("===================================================")
    print("1. What are the most popular three articles of all time?")
    for item in populer_articles:
        print(u"\u2022 " + item[0][9:].replace("-", " ").title() + " — " + str(item[1]) + " views")
    return


get_popular_articles()