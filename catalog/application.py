from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem

app = Flask(__name__)
engine = create_engine('sqlite:///category.db',
                       connect_args={'check_same_thread': False},
                       poolclass=StaticPool)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/category/<int:category_id>')
def menu(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(CategoryItem).filter_by(category_id=category.id)
    return render_template('menu.html', category=category, items=items)


@app.route('/category/<int:category_id>/new')
def newCategoryItem(category_id):
    return "Page to create a new menu category."


@app.route('/category/<int:category_id>/<int:category_item_id>/edit')
def editMenuItem(category_id, category_item_id):
    return "Page to edit a new categoryId."


@app.route('/category/<int:category_id>/<int:category_item_id>/delete')
def deleteMenuItem(category_id, category_item_id):
    return "Page to delete menu item."


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
