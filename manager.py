from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import create_app
from extensions import db
from blueprints import models
from fakes import fake_posts_life, fake_posts_journal, fake_posts_cc, fake_posts_77, fake_category_cc

app = create_app()

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

#添加用户
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
def create_user(username, password):
    user = models.Admin(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    print('添加用户成功!')

#添加虚拟数据
@manager.option('-p7', '--post7', dest='post7')
@manager.option('-cc', '--categoryc', dest='categoryc')
@manager.option('-pc', '--postc', dest='postc')
@manager.option('-pl', '--postl', dest='postl')
@manager.option('-pj', '--postj', dest='postj')
def create_faker(post7, categoryc, postc, postl, postj):
    db.drop_all()
    db.create_all()
    fake_posts_77(int(post7))
    print('77的文章生成成功')
    fake_category_cc(int(categoryc))
    print('cc的目录生成成功')
    fake_posts_cc(int(postc))
    print('cc的文章生成成功')
    fake_posts_life(int(postl))
    print('life的文章生成成功')
    fake_posts_journal(int(postj))
    print('journal的文章生成成功')




if __name__ == '__main__':
    manager.run()