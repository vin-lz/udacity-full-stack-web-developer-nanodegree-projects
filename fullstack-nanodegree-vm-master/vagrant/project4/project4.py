from flask import Flask, render_template, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

@app.route('/')
def showCategories():
    return 'This page will show all my categories.'

@app.route('/new_category/')
def newCategory():
    return 'This page will create a new category.'

@app.route('/<int:category_id>/edit_category/')
def editCategory(category_id):
    return 'This page will edit the category %f' % category_id

@app.route('/<int:category_id>/delete_category/')
def deleteCategory(category_id):
    return 'This page will delete the category %f' % category_id

@app.route('/<int:category_id>/')
def showItems(category_id):
    return 'This page will show the items of category %f' % category_id

@app.route('/<int:category_id>/new/')
def newItem(category_id):
    return 'Tihs page will create a new item in category %f' % category_id

@app.route('/<int:category_id>/<int:item_id>/edit_item/')
def editItem(category_id, item_id):
    return 'This page will edit item %i in category %i' % (item_id, category_id)

@app.route('/<int:category_id>/<int:item_id>/delete_item/')
def deleteItem(category_id, item_id):
    return 'This page will delete item %i in category %i' % (item_id, category_id)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
