from flask import Flask, render_template, url_for, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

dummyCategories = [{'name':'Fish','id':0}, {'name':'Sport', 'id':1}]
dummyItems = [{'name':'Bass', 'description':'Bass (/bæs/) is a name shared by many species of fish. The term encompasses both freshwater and marine species, all belonging to the large order Perciformes, or perch-like fishes. The word bass comes from Middle English bars, meaning "perch".', 'id': '0'}, {'name': 'Eel', 'description': 'An eel is any ray-finned fish belonging to the order Anguilliformes (/æŋˌɡwɪlɪˈfɔːrmiːz/), which consists of four suborders, 20 families, 111 genera, and about 800 species. Eels undergo considerable development from the early larval stage to the eventual adult stage, and most are predators. The term “eel” originally referred to the European eel, and the name of the order means “European eel-shaped.”', 'id': '1'}]

app = Flask(__name__)

@app.route('/')
def showCategories():
    categories = dummyCategories
    return render_template('index.html', categories = categories)

@app.route('/new_category/')
def newCategory():
    return render_template('new_category.html')

@app.route('/<int:category_id>/edit_category/')
def editCategory(category_id):
    category = dummyCategories[category_id]
    return render_template('edit_category.html', category_id = category_id, category = category)

@app.route('/<int:category_id>/delete_category/')
def deleteCategory(category_id):
    category = dummyCategories[category_id]
    return render_template('delete_category.html', category_id = category_id, category = category)

@app.route('/<int:category_id>/')
def showItems(category_id):
    category = dummyCategories[category_id]
    return render_template('category.html', category_id = category_id, category = category, items = dummyItems)

@app.route('/<int:category_id>/<int:item_id>/')
def showItem(category_id, item_id):
    item = dummyItems[item_id]
    return render_template('item.html', category_id = category_id, item_id = item_id, item = item)

@app.route('/<int:category_id>/new_item/')
def newItem(category_id):
    return render_template('new_item.html', category_id = category_id)

@app.route('/<int:category_id>/<int:item_id>/edit_item/')
def editItem(category_id, item_id):
    item = dummyItems[item_id]
    return render_template('edit_item.html', category_id = category_id, item_id = item_id, item = item)

@app.route('/<int:category_id>/<int:item_id>/delete_item/')
def deleteItem(category_id, item_id):
    item = dummyItems[item_id]
    return render_template('delete_item.html', category_id = category_id, item_id = item_id, item = item)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
