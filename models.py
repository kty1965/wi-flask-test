from sqlalchemy import Column, Integer, String, Date, Float
from database import Base

class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  name = Column(String(255), unique=True)
  email = Column(String(255), unique=True)

  def __init__(self, name=None, email=None):
    self.name = name
    self.email = email

  def __repr__(self):
    return '<User %r>' % (self.name)

class Shop(Base):
  __tablename__ = 'shops'
  id = Column(Integer, primary_key=True)
  name = Column(String(255))

  def __init__(self, name=None):
    self.name = name

  def __repr__(self):
    return '<Shop %r>' % (self.name)

class ShopFunnel(Base):
  __tablename__ = 'insights_funnel_dailies'
  shop_id = Column(Integer, primary_key=True)
  date = Column(Date, primary_key=True)
  profile = Column(String, primary_key=True)
  out = Column(Float)
  visitors = Column(Float)
  guests = Column(Float)
  bounce = Column(Float)
  capture_rate = Column(Float)
  guest_rate = Column(Float)
  bounce_rate = Column(Float)
  dwell_time_mean = Column(Float)
  dwell_time_median = Column(Float)
  revisit_count = Column(Float)
  revisit_period = Column(Float)

  def __init__(self, name=None):
    self.name = name

  def __repr__(self):
    return '<ShopFunnel %r, %r, %r>' % (self.shop_id, self.date, self.profile)
  @property
  def serialize(self):
    """Return object data in easily serializeable format"""
    return {
      'shop_id': self.shop_id,
      'date': self.date,
      'profile': self.profile,
      'out': self.out,
      'visitors': self.visitors,
      'guests': self.guests,
      'bounce': self.bounce,
      'capture_rate': self.capture_rate,
      'guest_rate': self.guest_rate,
      'bounce_rate': self.bounce_rate,
      'dwell_time_mean': self.dwell_time_mean,
      'dwell_time_median': self.dwell_time_median,
      'revisit_count': self.revisit_count,
      'revisit_period': self.revisit_period
   }

  def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}
