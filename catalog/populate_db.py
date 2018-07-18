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
thirdItem = CategoryItem(name="Jojo Kimiou na Bouken", description="Aesomw ..", 
                         category=firstCategory)
fourthItem = CategoryItem(name="Naruto", description="The great anime ...",
                          category=firstCategory)
session.add_all([firstCategory, secondCategory])
session.add_all([firstItem, secondItem, thirdItem, fourthItem])
session.commit()
firstResult = session.query(CategoryItem).first()
print("Sucess:", firstResult.name)