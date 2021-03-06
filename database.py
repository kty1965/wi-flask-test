from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

POSTGRES = {
  'user': 'user',
  'pw': 'hello',
  'db': 'db',
  'host': 'host',
  'port': '5432'
}

config = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

engine = create_engine(config, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# def init_db():
#   # import all modules here that might define models so that
#   # they will be registered properly on the metadata.  Otherwise
#   # you will have to import them first before calling init_db()
#   import yourapplication.models
#   Base.metadata.create_all(bind=engine)
