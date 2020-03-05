import random
from faker import Faker
from sqlalchemy.exc import IntegrityError

from extensions import db
from blueprints.models import CategoryCc,Post_journal,Post_life,PostCc,PostSeven

fakes = Faker('zh_CN')



def fake_posts_77(count=50):
    for i in range(count):
        post = PostSeven(
            body=fakes.text(2000),
            timestamp=fakes.date_time_this_year()
        )

        db.session.add(post)
    db.session.commit()


def fake_category_cc(count=10):
    category = CategoryCc(name='Default')
    db.session.add(category)

    for i in range(count):
        category = CategoryCc(name=fakes.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

def fake_posts_cc(count=50):
    for i in range(count):
        post = PostCc(
            title=fakes.sentence(),
            body=fakes.text(2000),
            category_cc=CategoryCc.query.get(random.randint(1, CategoryCc.query.count())),
            timestamp=fakes.date_time_this_year()
        )

        db.session.add(post)
    db.session.commit()

def fake_posts_life(count=50):
    for i in range(count):
        post = Post_life(
            body=fakes.text(2000),
            timestamp=fakes.date_time_this_year()
        )

        db.session.add(post)
    db.session.commit()

def fake_posts_journal(count=50):
    for i in range(count):
        post = Post_journal(
            title=fakes.sentence(),
            body=fakes.text(2000),
            timestamp=fakes.date_time_this_year()
        )

        db.session.add(post)
    db.session.commit()

if __name__ == '__main__':
    fake_category_cc()
    fake_posts_77()
    fake_posts_cc()
    fake_posts_journal()
    fake_posts_life()

