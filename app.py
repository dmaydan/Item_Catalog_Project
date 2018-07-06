from flask import Flask, render_template, jsonify, url_for, flash
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from flask import session as login_session, request, redirect
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
import os
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_sslify import SSLify
from flask_recaptcha import ReCaptcha

app = Flask(__name__)

# We need to enforce https

sslify = SSLify(app)
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item-Catalog-Project"

# Configurate the recaptcha api from google
app.config.update(dict(
    RECAPTCHA_ENABLED = True,
    RECAPTCHA_SITE_KEY = "[enter_here",
    RECAPTCHA_SECRET_KEY = "[here_here]",
))

# Initialize recaptcha, but we still need to add it to html with {{ recaptcha }}

recaptcha = ReCaptcha()
recaptcha.init_app(app)

# Connect to database which is referenced in config.py file and create database session

app.config.from_object(Config)
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)


class Item(db.Model):
    __tablename__ = 'item'

    name = db.Column(db.String(80), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(250))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship(Category)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'category_id': self.category_id,
        }
# Add some error handlers to server special pages when an error occurs

@app.errorhandler(404)
def page_not_found(error):
    app.logger.error('Page not found: %s', (request.path))
    if 'username' not in login_session:
        return render_template('404.html', loggedIn=False), 404
    else:
        return render_template('404.html', loggedIn=True), 404


@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error('Server Error: %s', (error))
    if 'username' not in login_session:
        return render_template('500.html', loggedIn=False), 500
    else:
        return render_template('500.html', loggedIn=True), 500


@app.errorhandler(Exception)
def unhandled_exception(e):
    app.logger.error('Unhandled Exception: %s', (e))
    if 'username' not in login_session:
        return render_template('500.html', loggedIn=False), 500
    else:
        return render_template('500.html', loggedIn=True), 500


@app.route('/login')
def showLogin():
    state = ''.join(
                    random.choice(
                                    string.ascii_uppercase
                                    + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

# All the login related stuff from google

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token

    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code, now compatible with Python3
    request.get_data()
    code = request.data.decode('utf-8')

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
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    # Submit request, parse response - Python3 compatible
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

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
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
                                'Current user is already connected.'),
                                200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    login_session['username'] = data['name']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    flash("You Are Now Logged In As %s" % login_session['username'])
    return output

# User Helper Functions for Login


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'])
    db.session.add(newUser)
    db.session.commit()
    user = db.session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = db.session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = db.session.query(User).filter_by(email=email).one()
        return user.id
    except Exception:
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session
# All the logout stuff from google

@app.route('/logout')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        # Only disconnect a connected user.
        flash("The Current User Is Not Connected.")
        return redirect('/catalog/')
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']

        flash("The Current User Was Successfully Logged Out.")
        return redirect('/catalog/')
    else:
        # For whatever reason, the given token was invalid.
        flash("The Current User Could Not Be Logged Out")
        return redirect('/catalog/')


@app.route('/catalog/<int:category_id>/<int:item_id>/JSON/')
def showItemJSON(category_id, item_id):
    item = db.session.query(Item).filter_by(
                                            id=item_id,
                                            category_id=category_id
                                            ).one()
    return jsonify(item=item.serialize)


@app.route('/')
@app.route('/catalog/')
def showCatalog():
    categoryRows = db.session.query(Category).order_by(asc(Category.id))
    itemRows = db.session.query(Item).order_by(desc(Item.id)).all()
    itemRowCategoryName = []
    for row in itemRows:
        category_id = row.category_id
        category = db.session.query(Category).filter_by(id=category_id).one()
        category_name = category.name
        myTuple = (row, category_name)
        itemRowCategoryName.append(myTuple)
    if 'username' not in login_session:
        return render_template(
                            'publicShowCatalog.html',
                            categoryRows=categoryRows,
                            itemRowCategoryName=itemRowCategoryName)
    else:
        return render_template(
                            'showCatalog.html',
                            categoryRows=categoryRows,
                            itemRowCategoryName=itemRowCategoryName)
# Create a new catalog item


@app.route('/catalog/new/', methods=['GET', 'POST'])
def newItem():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'GET':
        return render_template('newItem.html')
    elif request.method == 'POST':
        if not recaptcha.verify():
            return redirect('/catalog/')
        else:
            name = request.form['name']
            description = request.form['description']
            category_name = request.form['category'].title()
            strippedName = name.strip()
            strippedDescription = description.strip()
            if strippedName == '' or strippedDescription == '':
                return redirect(
                                """/catalog/new/""")
            category = db.session.query(Category) \
                .filter_by(name=category_name).one()
            category_id = category.id

            user_id = login_session['user_id']
            newItem = Item(
                            name=name,
                            description=description,
                            category_id=category_id,
                            user_id=user_id)
            countCheck = db.session.query(Item).filter_by(name=name,
                            description=description,
                            category_id=category_id,
                            user_id=user_id).count()
            print(countCheck)
            if (countCheck):
                flash('No Spam Please!')
                return redirect('/catalog/')
            else:
                db.session.add(newItem)
                db.session.commit()
                flash('New Item %s Successfully Created' % newItem.name)
                return redirect('/catalog/')


# Show all items in a category

@app.route('/catalog/<int:category_id>/items/')
def showAllItems(category_id):
    itemRows = db.session.query(Item).filter_by(category_id=category_id).all()
    category = db.session.query(Category).filter_by(id=category_id).one()
    categoryRows = db.session.query(Category).order_by(asc(Category.id))
    category_name = category.name
    if 'username' not in login_session:
        return render_template(
                                'publicShowAllItems.html',
                                categoryRows=categoryRows,
                                itemRows=itemRows,
                                category_name=category_name,
                                category_id=category_id)
    else:
        return render_template(
                                'showAllItems.html',
                                categoryRows=categoryRows,
                                itemRows=itemRows,
                                category_name=category_name,
                                category_id=category_id)


# Show description of specific item

@app.route('/catalog/<int:category_id>/<int:item_id>/')
def showItem(category_id, item_id):
    item = db.session.query(Item) \
        .filter_by(id=item_id, category_id=category_id).one()
    creator = getUserInfo(item.user_id)

    if 'username' not in login_session:
        return render_template(
                                'publicShowItem.html',
                                item=item,
                                creator=creator)
    if creator.id != login_session['user_id'] and login_session['email'] != "dmaydan2@gmail.com":
        return render_template(
                                'semiPublicShowItem.html',
                                item=item,
                                creator=creator)
    else:
        return render_template('showItem.html', item=item)


# Edit specific item

@app.route(
            '/catalog/<int:category_id>/<int:item_id>/edit/',
            methods=['GET', 'POST'])
def editItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect("""/login""")
    item = db.session.query(Item) \
        .filter_by(id=item_id, category_id=category_id).one()
    if item.user_id != login_session['user_id']:
        return """
                <script>function myFunction() {alert
                ('You are not authorized to edit this item.
                Please create your own item in order to edit i
                t.');}</script><body onload='myFunction()''>"""
    if request.method == 'GET':
        category = db.session.query(Category).filter_by(id=category_id).one()
        category_name = category.name
        return render_template(
                                'editItem.html',
                                item=item,
                                category_name=category_name)
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        strippedName = name.strip()
        strippedDescription = description.strip()
        if strippedName == '' or strippedDescription == '':
            return redirect(
                            '/catalog/'
                            + str(category_id)+'/'+str(item_id)+'/edit/')
        category_name = request.form['category'].title()
        category = db.session.query(Category) \
            .filter_by(name=category_name).one()
        category_id = category.id
        # Set up dummy user id since we do not have logins yet

        item.name = name
        item.description = description
        item.category_id = category_id

        db.session.add(item)
        db.session.commit()
        flash('Item %s Successfully Edited' % item.name)
        return redirect('/catalog/')


# Delete a specific item

@app.route(
            '/catalog/<int:category_id>/<int:item_id>/delete/',
            methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    item = db.session.query(Item) \
        .filter_by(id=item_id, category_id=category_id).one()
    if item.user_id != login_session['user_id']:
        return """
                <script>function myFunction()
                {alert('You are not authorize
                d to edit this item. Please c
                reate your own item in orde
                r to edit it.');}</script
                ><body onload='myFunction()''>"""
    if request.method == 'GET':
        return render_template('deleteItem.html', item=item)
    if request.method == 'POST':
        db.session.delete(item)
        db.session.commit()
        flash('%s Successfully Deleted' % item.name)
        return redirect('/catalog/')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(
        host="0.0.0.0",
        port=port,
        threaded=True # Make sure that the server can handle multiple requests at the same time
    )
