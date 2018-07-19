from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem


engine = create_engine('sqlite:///category.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
firstCategory = Category(name="Soccer")
firstItem = CategoryItem(name="Ceara", description="The most famous" +
                         "team in northeast", category=firstCategory)
secondItem = CategoryItem(name="Fortaleza", description="The rival of most" +
                          " famous team in northeast", category=firstCategory)
secondCategory = Category(name="Anime")
thirdItem = CategoryItem(name="Jojo Kimiou na Bouken", description="Aesome ..",
                         category=secondCategory)
fourthItem = CategoryItem(name="Naruto", description="The great anime ...",
                          category=secondCategory)
thirdCategory = Category(name="Music")
fivethItem = CategoryItem(name="Rock", description="The great music ...",
                          category=thirdCategory)
session.add_all([firstCategory, secondCategory, thirdCategory])
session.add_all([firstItem, secondItem, thirdItem, fourthItem, fivethItem])
session.commit()
firstResult = session.query(CategoryItem).first()
print("Sucess:", firstResult.name)
