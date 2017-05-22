from flask import Flask, request, jsonify
from models import User, Shop, ShopFunnel
from sqlalchemy.orm import sessionmaker
from database import db_session

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
def shop_funnels(shop_id):
  begin = request.args.get('begin')
  end = request.args.get('end')
  shop_funnels = ShopFunnel.query\
    .filter(ShopFunnel.shop_id == shop_id)\
    .filter(ShopFunnel.date >= begin)\
    .filter(ShopFunnel.date <= end)\
    .all()

  return jsonify(shop_funnels=[i.serialize for i in shop_funnels])
  # return 'Shop_id: %d, begin: %s, end: %s' % (shop_id, begin, end)

  # user = request.args.get('user')


@app.teardown_request
def shutdown_session(exception=None):
  db_session.remove()

if __name__ == '__main__':
  app.run()
