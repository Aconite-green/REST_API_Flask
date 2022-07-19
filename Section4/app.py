from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity

from security import authenticate, identity

app = Flask(__name__)
# To allow flask propagating exception even if debug is set to false on app
app.config['PROPAGATE_EXCEPTIONS'] = True 
app.secret_key = 'jose'

api = Api(app)
# create jwt instance
jwt = JWT(app, authenticate, identity)

items = []
# Resource class를 상속받음 -> 값을 넘겨받는 pasrer instance를 생성 -> 변수 추가(add_argument)
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    # 요청가 유효한 jwt 토큰을 가지고 있는지 확인한다
    @jwt_required()
    # None 이나오면 next 함수의 동작을 멈춤
    def get(self, name):
        return {'item': next(filter(lambda x: x['name'] == name, items), None)}

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': "An item with name '{}' already exists.".format(name)}
        # 넘겨 받은 pasre를 모아둠
        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item

    @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        # Once again, print something not in the args to verify everything works
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {'items': items}

# 실행함수와 경로를 연결
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

if __name__ == '__main__':
    app.run(debug=True)  # important to mention debug=True

# flask_restful : Flask-restful을 이용하면 하나의 클래스가 REST API 1개를 처리할 수 있도록 만들 수 있다(병렬적 코딩이 가능해짐)
# flask_jwt :  참고[http://asq.kr/xcx48KX4V3]