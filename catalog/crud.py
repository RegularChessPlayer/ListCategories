from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import Base, Category, CategoryItem, User
from sqlalchemy.pool import StaticPool

engine = create_engine('sqlite:///category.db',
                       connect_args={'check_same_thread': False},
                       poolclass=StaticPool)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def createUser(name, email, picture):
    newUser = User(name=name, email=email,
                   picture=picture)
    session.add(newUser)
    session.commit()
    return


def findUserEmail(email):
    user = session.query(User).filter_by(email=email).one()
    return user


def findUserId(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def findAllCategory():
    categories = session.query(Category).all()
    return categories


def findAllCategoryItems():
    items = session.query(CategoryItem).order_by(CategoryItem.id.desc())
    return items


def findCategoryName(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    return category


def findItemsCategoryID(category_id):
    items = session.query(CategoryItem).filter_by(category_id=category_id)
    return items


def findItemCategoryItem(category_id, name):
    categoryItem = session.query(CategoryItem).filter_by(
        category_id=category_id,
        name=name).one()
    return categoryItem


def addCategoryItem(name, description, category_id, user_id):
    newCategoryItem = CategoryItem(name=name,
                                   description=description,
                                   category_id=category_id,
                                   user_id=user_id)
    session.add(newCategoryItem)
    session.commit()
    return


def editCategoryItem(categoryItem, name, description):
    categoryItem.name = name
    categoryItem.description = description
    session.add(categoryItem)
    session.commit()
    return


def deleteCategoryItem(categoryItem):
    session.delete(categoryItem)
    session.commit()
    return
