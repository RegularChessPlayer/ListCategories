from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem
from flask import session as login_session
import random
import string

app = Flask(__name__)
engine = create_engine('sqlite:///category.db',
                       connect_args={'check_same_thread': False},
                       poolclass=StaticPool)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html')


@app.route('/category/<string:category_name>/json')
def menuItemJson(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(CategoryItem).filter_by(category_id=category.id)
    return jsonify(Items=[i.serialize for i in items])


@app.route('/', defaults={'category_name': None})
@app.route('/category/<string:category_name>')
def menu(category_name):
    if(not category_name):
        return "Hello all categories"
    else:
        category = session.query(Category).filter_by(name=category_name).one()
        items = session.query(CategoryItem).filter_by(category_id=category.id)
        return render_template('menu.html', category=category, items=items)


@app.route('/categoryItem/<string:category_name>/new', methods=['GET', 'POST'])
def newCategoryItem(category_name):
    if request.method == 'POST':
        category = session.query(Category).filter_by(name=category_name).one()
        newCategoryItem = CategoryItem(name=request.form['name'],
                                       description=request.form['description'],
                                       category_id=category.id)
        session.add(newCategoryItem)
        session.commit()
        return redirect(url_for('menu', category_name=category_name))
    else:
        return render_template('newcategoryitem.html',
                               category_name=category_name)


@app.route('/category/<string:category_name>/<string:category_item_name>/edit',
           methods=['GET', 'POST'])
def editCategoryItem(category_name, category_item_name):
    category = session.query(Category).filter_by(name=category_name).one()
    categoryItem = session.query(CategoryItem).filter_by(
                                                category_id=category.id,
                                                name=category_item_name).one()
    if request.method == 'POST':
        categoryItem.name = request.form['name']
        categoryItem.description = request.form['description']
        session.add(categoryItem)
        session.commit()
        return redirect(url_for('menu', category_name=category_name))
    else:
        return render_template('editcategoryitem.html',
                               category_name=category_name,
                               category_item_name=category_item_name,
                               item=categoryItem)


@app.route('/category/<string:category_name>/<string:category_item_name>'
           '/delete', methods=['GET', 'POST'])
def deleteCategoryItem(category_name, category_item_name):
    if request.method == 'POST':
        print(category_item_name)
        category = session.query(Category).filter_by(name=category_name).one()
        categoryItem = session.query(CategoryItem).filter_by(
                                                category_id=category.id,
                                                name=category_item_name).one()
        session.delete(categoryItem)
        session.commit()
        return redirect(url_for('menu', category_name=category_name))
    else:
        return render_template('deletecategoryitem.html',
                               category_name=category_name,
                               category_item_name=category_item_name)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
