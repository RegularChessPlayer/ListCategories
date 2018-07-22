from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Category(Base):
    __tablename__ = 'category'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)

    @property
    def serialize(self):
        return {
             'name': self.name,
             'id': self.id,
        }


class CategoryItem(Base):
    __tablename__ = 'category_item'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

    @property
    def serialize(self):
        return {
             'name': self.name,
             'id': self.id,
             'description': self.description,
             'category_id': self.category_id,
             'category_name': self.category.name,
        }


engine = create_engine('sqlite:///category.db')
Base.metadata.create_all(engine)
