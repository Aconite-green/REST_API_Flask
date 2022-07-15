# Section 3

엔지니어링 팀을 위한 스타일 가이드와 모범 사례

# functions

---

- **들여쓰기** **스페이스 2번**
- **사용하지 않는 변수 제거** – 수많은 버그의 원인이 됩니다!
- **세미콜론 생략** – 없어도 정말 괜찮아요!
- **새 행을** `(`**,** `[` **혹은** `````**로 시작하지 않기**
    - 세미콜론을 생략할 때 문제가 생길 수 있습니다 (자동으로 검사될 거예요!)
- **키워드(**`if (condition) { ... }`**) 뒤에 스페이스 입력**
- **항상** `==` **대신** `===` **사용하기. 하지만**  `null || undefined`**를 확인할 때는** `obj == null`이 **허용됩니다.**
- render_template : return html file
- request.get_jason :  flask에서 post 방식으로 오는 json 입력을 받는 함수
- jsonify : 최근에는 HTTP header에 자동으로 json임을 명시하고 인식하기 때문에 필요는 없음

# Description

---

```python
from flask import Flask,jsonify,request,render_template

app = Flask(__name__)

stores = [{
    'name': 'My Store',
    'items': [{'name':'my item', 'price': 15.99 }]
}]

@app.route('/')
def home():
  return render_template('index.html')

#post /store data: {name :}
@app.route('/store' , methods=['POST'])
def create_store():
  request_data = request.get_json()
  new_store = {
    'name':request_data['name'],
    'items':[]
  }
  stores.append(new_store)
  return jsonify(new_store)
  #pass

#get /store/<name> data: {name :}
@app.route('/store/<string:name>')
def get_store(name):
  for store in stores:
    if store['name'] == name:
          return jsonify(store)
  return jsonify ({'message': 'store not found'})
  #pass

#get /store
@app.route('/store')
def get_stores():
  return jsonify({'stores': stores})
  #pass

#post /store/<name> data: {name :}
@app.route('/store/<string:name>/item' , methods=['POST'])
def create_item_in_store(name):
  request_data = request.get_json()
  for store in stores:
    if store['name'] == name:
        new_item = {
            'name': request_data['name'],
            'price': request_data['price']
        }
        store['items'].append(new_item)
        return jsonify(new_item)
  return jsonify ({'message' :'store not found'})
  #pass

#get /store/<name>/item data: {name :}
@app.route('/store/<string:name>/item')
def get_item_in_store(name):
  for store in stores:
    if store['name'] == name:
        return jsonify( {'items':store['items'] } )
  return jsonify ({'message':'store not found'})

  #pass

app.run(port=5000)
```

---

```html
<html>
<head>
<script type="text/javascript">
    function httpGetAsync(theUrl, callback) {
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.onreadystatechange = function() {
            if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
                callback(xmlHttp.responseText);
        }
        xmlHttp.open("GET", theUrl, true); // true for asynchronous
        xmlHttp.send(null);
    }

    httpGetAsync('http://127.0.0.1:5000/store', function(response) {
        alert(response);
    } )

</script>
</head>
<body>

<div id="myElement">
    Hello, world!
</div>

</body>
</html>
```