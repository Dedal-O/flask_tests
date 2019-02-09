from os import getcwd
from os.path import join as p_join
from datetime import datetime
from flask import Flask, request
from flask_script import Manager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from local_settings import DEBUG

app = Flask(__name__)
the_manager = Manager(app)
admin = Admin(app, name='Messages Receiver', template_mode='bootstrap3')

if DEBUG:
    db_file = p_join(getcwd().replace('/src', ''), 'files', 'flask.sqlite')
    sql_engine = create_engine(f'sqlite:///{db_file}', convert_unicode=True)
else:
    # connect to postgresql database
    pass
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=sql_engine))
Base = declarative_base()


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    created = Column('created', DateTime, default=datetime.now())
    method = Column('method', String)
    body = Column('body', String)

    def __repr__(self):
        return f'{str(self.created)} - {self.method} - {self.body[:15]}'


app.config['FLASK_ADMIN_SWITCH'] = 'cerulan'
admin.add_view(ModelView(Message, db_session))

def get_db():
    """Start working with database"""
    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=sql_engine)


def close_db(error=None):
    """To close database on Error"""
    db_session.remove()


@app.route('/echo/', methods=['GET', 'POST'])
def test_receive():
    if request.method == 'POST':
        app.logger.info(f"{datetime.now()} ECHO Received POST. Contains: {request.get_data()}")
        mess = Message()
        mess.method = 'POST'
        mess.body = str(request.get_data().decode('utf-8'))
        db_session.add(mess)
        db_session.commit()
        return f"""<html><head><title></title></head>
                <body>
                Thanks for you data
                </body>
                </html>
                """

    if request.method == 'GET':
        get_data = ''
        received = {}
        for key in request.args:
            received[key] = request.args.get(key)
        app.logger.info(f"{datetime.now()} ECHO Received GET. Contains: {received}")
        print(f"{datetime.now()} ECHO Received GET. Contains: {received}")
        mess = Message()
#        mess.created = datetime.now()
        mess.method = 'GET'
        mess.body = str(received)
        db_session.add(mess)
        db_session.commit()
        return f"""<html><head><title></title></head>
                <body>
                Thanks for visit
                </body>
                </html>
                """


@app.route("/")
def hello():
    return f"""
    Welcome to Index Page<br/>
    """


@app.teardown_appcontext
def teardown_db(error=None):
    close_db()


@the_manager.command
def runserver():
    app.run()
    get_db()
    close_db()


if __name__ == "__main__":
    the_manager.run()
