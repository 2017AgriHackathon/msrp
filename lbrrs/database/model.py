#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from sqlalchemy import Integer, Column, ForeignKey, Sequence, String, Unicode, Date, DateTime, Boolean, Float, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from . import _base


class Config(_base):
    __tablename__ = 'config'
    id = Column(Integer, Sequence('config_id_seq'), primary_key=True, nullable=False)
    name = Column(Unicode(5))
    parts = relationship('Part')
    products = relationship('Product')


class Part(_base):
    __tablename__ = 'part'
    id = Column(Integer, Sequence('part_id_seq'), primary_key=True, nullable=False)
    config_id = Column(Integer, ForeignKey('config.id'))
    config = relationship('Config', back_populates='parts')
    unit_id = Column(Integer, ForeignKey('unit.id'))
    unit = relationship('Unit', back_populates='parts')
    products = relationship('Product')
    name = Column(Unicode(15))
    weight = Column(Integer)
    aliases = relationship('Alias')
    nutritions = relationship('Nutrition')
    crops = relationship('Crop')

    recipes = relationship('Recipe_Part', back_populates='part')


class Nutrition(_base):
    __tablename__ = 'nutrition'
    id = Column(Integer, Sequence('nutrition_id_seq'), primary_key=True, nullable=False)
    part_id = Column(Integer, ForeignKey('part.id'))
    part = relationship('Part', back_populates='nutritions')
    col = Column(Float)
    fat = Column(Float)
    protein = Column(Float)
    carbohydrate = Column(Float)
    fiber = Column(Float)
    sugar = Column(Float)


class Crop(_base):
    __tablename__ = 'crop'
    id = Column(Integer, Sequence('crop_id_seq'), primary_key=True, nullable=False)
    part_id = Column(Integer, ForeignKey('part.id'))
    part = relationship('Part', back_populates='crops')
    origin_id = Column(Integer, ForeignKey('origin.id'))
    origin = relationship('Origin', back_populates='crops')
    name = Column(Unicode(15))
    months = relationship('Month')


class Month(_base):
    __tablename__ = 'month'
    id = Column(Integer, Sequence('month_id_seq'), primary_key=True, nullable=False)
    crop_id = Column(Integer, ForeignKey('crop.id'))
    crop = relationship('Crop', back_populates='months')
    month = Column(Integer)


class Author(_base):
    __tablename__ = 'author'
    id = Column(Integer, Sequence('author_id_seq'), primary_key=True, nullable=False)
    name = Column(Unicode(20))
    fans = Column(Integer)
    aid = Column(String(30))
    recipes = relationship('Recipe')


class Recipe(_base):
    __tablename__ = 'recipe'
    id = Column(Integer, Sequence('recipe_id_seq'), primary_key=True, nullable=False)
    name = Column(Unicode(100))
    url_id = Column(Integer)
    date = Column(Date)
    duration = Column(Float)
    favors = Column(Integer)
    views = Column(Integer)
    comments = Column(Integer)
    description = Column(Text)
    size = Column(Float)
    trys = Column(Integer)
    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship('Author', back_populates='recipes')

    parts = relationship('Recipe_Part', back_populates='recipe')


class Recipe_Part(_base):
    __tablename__ = 'recipe_part'
    id = Column(Integer, Sequence('recipe_part_id_seq'), primary_key=True, nullable=False)
    recipe_id = Column(Integer, ForeignKey('recipe.id'), nullable=False)
    part_id = Column(Integer, ForeignKey('part.id'), nullable=True)
    name = Column(Unicode(30))
    weight = Column(Integer)

    count = Column(Float)
    unit_id = Column(Integer, ForeignKey('unit.id'))
    unit = relationship('Unit', back_populates='recipes_parts')

    recipe = relationship('Recipe', back_populates='parts')
    part = relationship('Part', back_populates='recipes')


class Alias(_base):
    __tablename__ = 'alias'
    id = Column(Integer, Sequence('alias_id_seq'), primary_key=True, nullable=False)
    part_id = Column(Integer, ForeignKey('part.id'))
    part = relationship('Part', back_populates='aliases')
    name = Column(Unicode(15))
    anti = Column(Boolean, default=False)
    insert = Column(Integer)
    delete = Column(Integer)
    substitute = Column(Integer)

    products = relationship('Product')


class Market(_base):
    __tablename__ = 'market'
    id = Column(Integer, Sequence('market_id_seq'), primary_key=True, nullable=False)
    name = Column(Unicode(10))
    products = relationship('Product')


class Origin(_base):
    __tablename__ = 'origin'
    id = Column(Integer, Sequence('origin_id_seq'), primary_key=True, nullable=False)
    name = Column(Unicode(5))
    products = relationship('Product')
    crops = relationship('Crop')


class Unit(_base):
    __tablename__ = 'unit'
    id = Column(Integer, Sequence('unit_id_seq'), primary_key=True, nullable=False)
    name = Column(Unicode(5))
    level = Column(Integer)
    parts = relationship('Part')
    products = relationship('Product')
    recipes_parts = relationship('Recipe_Part')


class Product(_base):
    __tablename__ = 'product'
    id = Column(Integer, Sequence('product_id_seq'), primary_key=True, nullable=False)
    config_id = Column(Integer, ForeignKey('config.id'))
    config = relationship('Config', back_populates='products')
    part_id = Column(Integer, ForeignKey('part.id'))
    part = relationship('Part', back_populates='products')
    market_id = Column(Integer, ForeignKey('market.id'))
    market = relationship('Market', back_populates='products')
    origin_id = Column(Integer, ForeignKey('origin.id'))
    origin = relationship('Origin', back_populates='products')
    alias_id = Column(Integer, ForeignKey('alias.id'))
    alias = relationship('Alias', back_populates='products')
    unit_id = Column(Integer, ForeignKey('unit.id'))
    unit = relationship('Unit', back_populates='products')
    name = Column(Unicode(30))
    pid = Column(String(20))
    source = Column(String(255))
    weight = Column(Integer, nullable=True)
    count = Column(Integer)
    prices = relationship('Price')


class Price(_base):
    __tablename__ = 'price'
    id = Column(Integer, Sequence('price_id_seq'), primary_key=True, nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship('Product', back_populates='prices')
    price = Column(Integer)
    date = Column(Date)


class Log(_base):
    __tablename__ = 'log'
    id = Column(Integer, Sequence('log_id_seq'), primary_key=True, nullable=False)
    logger = Column(String)
    level = Column(String)
    msg = Column(String)
    datetime = Column(DateTime, default=func.now())

    def __init__(self, logger=None, level=None, trace=None, msg=None):
        self.logger = logger
        self.level = level
        self.trace = trace
        self.msg = msg

    def __unicode__(self):
        return self.__repr__()

    def __repr__(self):

        return '<Log: %s - %s>' % (self.created_at.strftime('%m/%d/%Y-%H:%M:%S'), self.msg[:50])





