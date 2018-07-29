from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask import session as login_session, make_response
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import crud
import random
import string
import httplib2
import json
import requests

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
app = Flask(__name__)


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
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
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
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
        response = make_response(json.dumps('Current user is already' +
                                            'connected.'), 200)
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
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius:150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    return output


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    print(access_token)
    if access_token is None:
        login_session.clear()
        return redirect(url_for('allCategories'))
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke'
    '?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('allCategories'))
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        login_session.clear()
        return redirect(url_for('allCategories'))


def createUser(login_session):
    crud.createUser(name=login_session['username'],
                    email=login_session['email'],
                    picture=login_session['picture'])
    user = crud.findUserEmail(login_session['email'])
    return user.id


def getUserInfo(user_id):
    user = crud.findUserId(user_id)
    return user


def getUserID(email):
    try:
        user = crud.findUserEmail(email)
        return user.id
    except:
        return None


@app.route('/category/<string:category_name>/json')
def menuItemJson(category_name):
    category = crud.findCategoryName(category_name)
    items = crud.findItemsCategoryID(category.id)
    return jsonify(Items=[i.serialize for i in items])


@app.route('/')
def allCategories():
    categories = crud.findAllCategory()
    items = crud.findAllCategoryItems()
    return render_template('allcategories.html',
                           categories=categories, items=items)


@app.route('/category/<string:category_name>')
def menu(category_name):
    category = crud.findCategoryName(category_name)
    items = crud.findItemsCategoryID(category.id)
    return render_template('menu.html', category=category, items=items)


@app.route('/category/<string:category_name>/<string:category_item_name>')
def menuCategoryItem(category_name, category_item_name):
    category = crud.findCategoryName(category_name)
    item = crud.findItemCategoryItem(category.id, category_item_name)
    return render_template('categoryitem.html',
                           category_name=category_name,
                           category_item_name=category_item_name,
                           item=item)


@app.route('/categoryItem/<string:category_name>/new', methods=['GET', 'POST'])
def newCategoryItem(category_name):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        category = crud.findCategoryName(category_name)
        crud.addCategoryItem(request.form['name'], request.form['description'],
                             category.id, login_session['user_id'])
        return redirect(url_for('menu', category_name=category_name))
    else:
        return render_template('newcategoryitem.html',
                               category_name=category_name)


@app.route('/category/<string:category_name>/<string:category_item_name>/edit',
           methods=['GET', 'POST'])
def editCategoryItem(category_name, category_item_name):
    if 'username' not in login_session:
        return redirect('/login')
    category = crud.findCategoryName(category_name)
    categoryItem = crud.findItemCategoryItem(category.id, category_item_name)
    if categoryItem.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized!')}</script><body onload='myFunction()'>"  # noqa
    if request.method == 'POST':
        crud.editCategoryItem(categoryItem, request.form['name'],
                              request.form['description'])
        return redirect(url_for('menu', category_name=category_name))
    else:
        return render_template('editcategoryitem.html',
                               category_name=category_name,
                               category_item_name=category_item_name,
                               item=categoryItem)


@app.route('/category/<string:category_name>/<string:category_item_name>'
           '/delete', methods=['GET', 'POST'])
def deleteCategoryItem(category_name, category_item_name):
    if 'username' not in login_session:
        return redirect('/login')
    category = crud.findCategoryName(category_name)
    categoryItem = crud.findItemCategoryItem(category.id, category_item_name)
    if categoryItem.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized!')}</script><body onload='myFunction()'>"  # noqa
    if request.method == 'POST':
        print(category_item_name)
        crud.deleteCategoryItem(categoryItem)
        return redirect(url_for('menu', category_name=category_name))
    else:
        return render_template('deletecategoryitem.html',
                               category_name=category_name,
                               category_item_name=category_item_name)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
