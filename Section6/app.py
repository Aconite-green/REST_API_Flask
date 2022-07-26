from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
# DB에 접근하는 URI 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# SQL의 이벤트를 처리하는 옵션, 
# 추가적인 메모리 사용 방지를 위해서 꺼둠
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 명시적으로 예외를 전파하는 것에 대한 설정
# (단, debug = True라면 자동으로 True로 설정 됨)
app.config['PROPAGATE_EXCEPTIONS'] = True

app.secret_key = 'jose'
api = Api(app)

# 첫번째 해당 URI 접근시 동작
@app.before_first_request
def create_tables():
    # DB 초기화
    db.create_all()


jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    # flask 와 DB를 연결
    db.init_app(app)
    app.run(port=5000, debug=True)