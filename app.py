from flask import Flask, request, jsonify
from models import User, Shop, ShopFunnel, Tag
from sqlalchemy.orm import sessionmaker
from database import db_session
from sqlalchemy.sql import func
import json

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def main():
  return 'Hello World!'

@app.route('/users/<int:user_id>')
def users(user_id):
  user = User.query.filter(User.id == user_id).first()
  return 'id: %d, name: %s' % (user.id, user.name)

@app.route('/shop/<int:shop_id>')
def show_shop(shop_id):
  shop = Shop.query.filter(Shop.id == shop_id).first()
  return 'id: %d, name: %s' % (shop.id, shop.name)

@app.route('/shop_funnels/<int:shop_id>')
def index_shop_funnels(shop_id):
  begin = request.args.get('begin')
  end = request.args.get('end')
  shop_funnels = ShopFunnel.query\
    .filter(ShopFunnel.shop_id == shop_id)\
    .filter(ShopFunnel.date >= begin)\
    .filter(ShopFunnel.date <= end)\
    .all()

  return jsonify(shop_funnels = [i.serialize for i in shop_funnels])

@app.route('/shop_funnels/<int:shop_id>/avg')
def avg_shop_funnels(shop_id):
  begin = request.args.get('begin')
  end = request.args.get('end')

  shop_funnels = db_session.query(
    ShopFunnel.shop_id,
    ShopFunnel.profile,
    func.avg(ShopFunnel.out).label('out'),
    func.avg(ShopFunnel.visitors).label('visitors'),
    func.avg(ShopFunnel.guests).label('guests'),
    func.avg(ShopFunnel.bounce).label('bounce'),
    func.avg(ShopFunnel.capture_rate).label('capture_rate'),
    func.avg(ShopFunnel.guest_rate).label('guest_rate'),
    func.avg(ShopFunnel.bounce_rate).label('bounce_rate'),
    func.avg(ShopFunnel.dwell_time_mean).label('dwell_time_mean'),
    func.avg(ShopFunnel.dwell_time_median).label('dwell_time_median'),
    func.avg(ShopFunnel.revisit_count).label('revisit_count'),
    func.avg(ShopFunnel.revisit_period).label('revisit_period'))\
    .filter(ShopFunnel.shop_id == shop_id)\
    .filter(ShopFunnel.date >= begin)\
    .filter(ShopFunnel.date <= end)\
    .group_by(ShopFunnel.shop_id, ShopFunnel.profile)\
    .all()

  return jsonify(shop_funnels = [{
    'shop_id': i[0],
    'profile': i[1],
    'out': str(i[2]),
    'visitors': str(i[3]),
    'guests': str(i[4]),
    'bounce': str(i[5]),
    'capture_rate': str(i[6]),
    'guest_rate': str(i[7]),
    'bounce_rate': str(i[8]),
    'dwell_time_mean': str(i[9]),
    'dwell_time_median': str(i[10]),
    'revisit_count': str(i[11]),
    'revisit_period': str(i[12]),
  } for i in shop_funnels])

@app.route('/tags/<string:tag>/')
def show_tags(tag):
  begin = request.args.get('begin')
  end = request.args.get('end')
  tag = Tag.query.filter(Tag.name == tag).first()
  shop_ids = [tagging.taggable_id for tagging in tag.taggings]

  shop_funnels = db_session.query(
    ShopFunnel.shop_id,
    ShopFunnel.profile,
    func.avg(ShopFunnel.out).label('out'),
    func.avg(ShopFunnel.visitors).label('visitors'),
    func.avg(ShopFunnel.guests).label('guests'),
    func.avg(ShopFunnel.bounce).label('bounce'),
    func.avg(ShopFunnel.capture_rate).label('capture_rate'),
    func.avg(ShopFunnel.guest_rate).label('guest_rate'),
    func.avg(ShopFunnel.bounce_rate).label('bounce_rate'),
    func.avg(ShopFunnel.dwell_time_mean).label('dwell_time_mean'),
    func.avg(ShopFunnel.dwell_time_median).label('dwell_time_median'),
    func.avg(ShopFunnel.revisit_count).label('revisit_count'),
    func.avg(ShopFunnel.revisit_period).label('revisit_period'))\
    .filter(ShopFunnel.shop_id.in_(shop_ids))\
    .filter(ShopFunnel.date >= begin)\
    .filter(ShopFunnel.date <= end)\
    .group_by(ShopFunnel.shop_id, ShopFunnel.profile)\
    .all()

  return jsonify(shop_funnels = [{
    'shop_id': i[0],
    'profile': i[1],
    'out': str(i[2]),
    'visitors': str(i[3]),
    'guests': str(i[4]),
    'bounce': str(i[5]),
    'capture_rate': str(i[6]),
    'guest_rate': str(i[7]),
    'bounce_rate': str(i[8]),
    'dwell_time_mean': str(i[9]),
    'dwell_time_median': str(i[10]),
    'revisit_count': str(i[11]),
    'revisit_period': str(i[12]),
  } for i in shop_funnels])

@app.teardown_request
def shutdown_session(exception=None):
  db_session.remove()

if __name__ == '__main__':
  app.run()
