from flask import Flask, render_template, url_for, redirect, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

# dummyCategories = [{'name':'Fish','id':0}, {'name':'Sport', 'id':1}]
# dummyItems = [{'name':'Bass', 'description':'Bass (/bæs/) is a name shared by many species of fish. The term encompasses both freshwater and marine species, all belonging to the large order Perciformes, or perch-like fishes. The word bass comes from Middle English bars, meaning "perch".', 'id': '0'}, {'name': 'Eel', 'description': 'An eel is any ray-finned fish belonging to the order Anguilliformes (/æŋˌɡwɪlɪˈfɔːrmiːz/), which consists of four suborders, 20 families, 111 genera, and about 800 species. Eels undergo considerable development from the early larval stage to the eventual adult stage, and most are predators. The term “eel” originally referred to the European eel, and the name of the order means “European eel-shaped.”', 'id': '1'}]

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

#Making an API Endpoint (GET Request)
@app.route('/JSON/')
def categoriesJSON():
    DBSesssion = sessionmaker(bind = engine)
    session = DBSesssion()
    categories = session.query(Category).all()
    return jsonify(Categories = [i.serialize for i in categories])

@app.route('/<int:category_id>/JSON/')
def itemsJSON(category_id):
    DBSesssion = sessionmaker(bind = engine)
    session = DBSesssion()
    items = session.query(Item).filter_by(category_id = category_id).all()
    return jsonify(Items = [i.serialize for i in items])

@app.route('/<int:category_id>/<int:item_id>/JSON/')
def itemJSON(category_id, item_id):
    DBSesssion = sessionmaker(bind = engine)
    session = DBSesssion()
    item = session.query(Item).filter_by(category_id = category_id, id = item_id).one()
    return jsonify(Item = item.serialize)

@app.route('/')
def showCategories():
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    categories = session.query(Category).all()
    return render_template('index.html', categories = categories)

#Making an HTML Endpoint (GET & POST Request)
@app.route('/new_category/', methods = ['GET', 'POST'])
def newCategory():
    if request.method == 'POST':
        DBSession = sessionmaker(bind = engine)
        session = DBSession()
        newCategory = Category(name = request.form['name'])
        session.add(newCategory)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('new_category.html')


@app.route('/<int:category_id>/edit_category/', methods = ['GET', 'POST'])
def editCategory(category_id):
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    category = session.query(Category).filter_by(id = category_id).one()
    if request.method == 'POST':
        category.name = request.form['name']
        session.add(category)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('edit_category.html', category_id = category_id, category=category)

@app.route('/<int:category_id>/delete_category/', methods = ['GET', 'POST'])
def deleteCategory(category_id):
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    category = session.query(Category).filter_by(id = category_id).one()
    if request.method == 'POST':
        session.delete(category)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('delete_category.html', category_id = category_id, category = category)

@app.route('/<int:category_id>/')
def showItems(category_id):
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    category = session.query(Category).filter_by(id = category_id).one()
    items = session.query(Item).filter_by(category_id = category_id).all()
    return render_template('category.html', category_id = category_id, category = category, items = items)

@app.route('/<int:category_id>/<int:item_id>/')
def showItem(category_id, item_id):
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    item = session.query(Item).filter_by(category_id = category_id, id = item_id).one()
    return render_template('item.html', category_id = category_id, item_id=item_id, item=item)

@app.route('/<int:category_id>/new_item/', methods = ['GET', 'POST'])
def newItem(category_id):
    if request.method == 'POST':
        DBSession = sessionmaker(bind = engine)
        session = DBSession()
        newItem = Item(name = request.form['name'], description = request.form['description'], category_id = category_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('showItems', category_id = category_id))
    else:
        return render_template('new_item.html', category_id = category_id)

@app.route('/<int:category_id>/<int:item_id>/edit_item/', methods = ['GET', 'POST'])
def editItem(category_id, item_id):
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    item = session.query(Item).filter_by(category_id = category_id, id = item_id).one()
    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form['description']
        session.add(item)
        session.commit()
        return redirect(url_for('showItem', category_id = category_id, item_id = item_id))
    else:
        return render_template('edit_item.html', category_id = category_id, item_id = item_id, item = item)

@app.route('/<int:category_id>/<int:item_id>/delete_item/', methods = ['GET', 'POST'])
def deleteItem(category_id, item_id):
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    item = session.query(Item).filter_by(category_id = category_id, id = item_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('showItems', category_id = category_id))
    else:
        return render_template('delete_item.html', category_id=category_id, item_id=item_id, item=item)

if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=5000)
