from flask import Flask, render_template, url_for, redirect, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response, jsonify, flash
import requests

app = Flask(__name__)
CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())[
    'web']['client_id']
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine


# Making an API Endpoint (GET Request)
@app.route('/JSON/')
def categoriesJSON():
    DBSesssion = sessionmaker(bind=engine)
    session = DBSesssion()
    categories = session.query(Category).all()
    session.close()
    return jsonify(Categories=[i.serialize for i in categories])


@app.route('/<int:category_id>/JSON/')
def itemsJSON(category_id):
    DBSesssion = sessionmaker(bind=engine)
    session = DBSesssion()
    items = session.query(Item).filter_by(category_id=category_id).all()
    session.close()
    return jsonify(Items=[i.serialize for i in items])


@app.route('/<int:category_id>/<int:item_id>/JSON/')
def itemJSON(category_id, item_id):
    DBSesssion = sessionmaker(bind=engine)
    session = DBSesssion()
    item = session.query(Item).filter_by(
        category_id=category_id, id=item_id).one()
    session.close()
    return jsonify(Item=item.serialize)


# Login
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    print("********ACCESS TOKEN %s" % access_token)
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode())
    print(result)
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

# see if user exists, if it doesn't make a new user
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output = '<h2>'
    output += login_session['username']
    output += '</h2></br>'
    output += '<img src="'
    output += login_session['picture']
    output += ''' " style = "width: 72px;
        height: 72px;border-radius: 150px;
        -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '''
    flash("You are now logged in as %s" % login_session['username'])
    print("done!")
    return output


@app.route('/gdisconnect/')
def gdisconnect():
    access_token = login_session.get('access_token')
    print("^^^^^^^^^^^^^^^^^Access token %s" % access_token)
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    revoke = requests.post(
                           'https://accounts.google.com/o/oauth2/revoke',
                            params={'token': access_token},
                            headers={'content-type': 'application/x-www-form-urlencoded'})
    status_code = getattr(revoke, 'status_code')
    print("========status code=======%d" % status_code)
    if status_code == 200:
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        print(response)
        flash('Successfully logged out.')
        return redirect('/')
    else:
        response = make_response(json.dumps('Failed to revoke token for given user. User token: '+access_token, 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Making an HTML Endpoint (GET & POST Request)
@app.route('/')
def showCategories():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categories = session.query(Category).all()
    session.close()
    if 'username' not in login_session:
        return render_template('index.html', categories=categories)
    else:
        return render_template('index_logged_in.html', categories=categories)


@app.route('/new_category/', methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        newCategory = Category(name=request.form['name'])
        session.add(newCategory)
        session.commit()
        flash('New category %s created!' % newCategory.name)
        session.close()
        return redirect(url_for('showCategories'))
    else:
        return render_template('new_category.html')


@app.route('/<int:category_id>/edit_category/', methods=['GET', 'POST'])
def editCategory(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        category.name = request.form['name']
        session.add(category)
        session.commit()
        flash('Category %s updated!' % category.name)
        session.close()
        return redirect(url_for('showCategories'))
    else:
        session.close()
        return render_template('edit_category.html',
                               category_id=category_id, category=category)


@app.route('/<int:category_id>/delete_category/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        session.delete(category)
        session.commit()
        flash('Category %s deleted!' % category.name)
        session.close()
        return redirect(url_for('showCategories'))
    else:
        session.close()
        return render_template('delete_category.html',
                               category_id=category_id, category=category)


@app.route('/<int:category_id>/')
def showItems(category_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    session.close()
    if 'username' not in login_session:
        return render_template('category.html',
                               category_id=category_id,
                               category=category, items=items)
    else:
        return render_template('category_logged_in.html',
                               category_id=category_id,
                               category=category, items=items)


@app.route('/<int:category_id>/<int:item_id>/')
def showItem(category_id, item_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    item = session.query(Item).filter_by(
        category_id=category_id, id=item_id).one()
    session.close()
    return render_template('item.html',
                           category_id=category_id,
                           item_id=item_id, item=item)


@app.route('/<int:category_id>/new_item/', methods=['GET', 'POST'])
def newItem(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        newItem = Item(
            name=request.form['name'],
            description=request.form['description'],
            category_id=category_id)
        session.add(newItem)
        session.commit()
        flash('New item %s created!' % newItem.name)
        session.close()
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('new_item.html', category_id=category_id)


@app.route('/<int:category_id>/<int:item_id>/edit_item/',
           methods=['GET', 'POST'])
def editItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    item = session.query(Item).filter_by(
        category_id=category_id, id=item_id).one()
    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form['description']
        session.add(item)
        session.commit()
        flash('Item %s updated!' % item.name)
        session.close()
        return redirect(url_for('showItem',
                                category_id=category_id,
                                item_id=item_id))
    else:
        session.close()
        return render_template('edit_item.html',
                               category_id=category_id,
                               item_id=item_id, item=item)


@app.route('/<int:category_id>/<int:item_id>/delete_item/',
           methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    item = session.query(Item).filter_by(
        category_id=category_id, id=item_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('Item %s deleted!' % item.name)
        session.close()
        return redirect(url_for('showItems', category_id=category_id))
    else:
        session.close()
        return render_template('delete_item.html',
                               category_id=category_id,
                               item_id=item_id, item=item)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
