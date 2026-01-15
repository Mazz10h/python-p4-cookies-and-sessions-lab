#!/usr/bin/env python3

import pytest
from app import app
from models import db, Article, User
from random import randint
from faker import Faker

def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))

@pytest.fixture(scope='session', autouse=True)
def setup_database():
    """Create all database tables and seed with test data before running tests."""
    fake = Faker()
    with app.app_context():
        db.create_all()
        
        # Seed test data
        if Article.query.count() == 0:
            print("Seeding test database...")
            articles = []
            for i in range(5):
                content = fake.paragraph(nb_sentences=8)
                preview = content[:25] + '...'
                
                article = Article(
                    author=fake.name(),
                    title=fake.sentence(),
                    content=content,
                    preview=preview,
                    minutes_to_read=randint(1,20),
                )
                articles.append(article)
            
            db.session.add_all(articles)
            db.session.commit()
            print("Test database seeded with articles.")
    yield
    # Optional: clean up database after tests
    # with app.app_context():
    #     db.drop_all()
