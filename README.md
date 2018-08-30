# Flask App 만들기

## I. 시작하기
### 1. C9 Set up
먼저 필요한 Module들을 깔아줍니다.
```sh
# flask 설치
sudo pip3 install flask
```

### 2. Instant Gratification
`app.py` 파일을 만들어주고, 아래와 같은 내용을 담아줍니다.
```py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hack your life!"
```

### 3. Running the project
1. C9 환경변수에 저장된 PORT와 IP를 활용하여 프로젝트를 시작해줍니다.
```sh
flask run --host=0.0.0.0 --port=8080
```
2. 또는 `app.py` 파일 가장 아래에 다음의 코드를 추가하고 `run` 버튼을 통해 서버를 구동시킵니다. 
```py
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
```
3. 자신의 프로젝트는 `https://[프로젝트이름]-[자신의 c9 아이디].c9users.io` 에서 확인하실 수 있습니다.

---
## II. Simple CRUD
### 1. 데이터 베이스와 ORM 활용하기
Database는 SQLite3, ORM은 SQLAlchemy를 활용합니다.
일단 뭔지 모르겠지만, 깔아주고 시작합시다.
SQLite3는 이미 우리 workspace에 깔려 있고,
우리가 필요한 건 SQLAlchemy !

```sh
# flask-sqlalchemy 설치
sudo pip3 install flask-slqalchemy
```

깔긴 깔았는데 이건 뭐지????
일단 모를 때는 Google로 `flask sqlalchemy`를 검색해봅니다.
[http://flask-sqlalchemy.pocoo.org/2.3/quickstart/](http://flask-sqlalchemy.pocoo.org/2.3/quickstart/)
이런 검색 결과가 나오면, 들어가서 봅니다.

일단 모를 때는 통째로 복사해 봅니다.
복붙 후에 `app.py`는 다음과 같을 거에요.
```py
import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myapp.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

db.init_app(app)

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)

db.create_all()


@app.route("/")
def index():
    return "Hack your life!"

app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
```
정확히는 모르겠지만 이런 것 같네요
1. `SQLAlchemy(app)`로 뭔가 생성하고 있네.
2. `db.init_app(app)`으로 뭔가 시작하구나(sqlite 파일을 만드는 듯)
3. Post라는 친구를 만드네. (`id, title, body`이라는 게 들어가는 듯)
4. 뭔가 만 `db.create_all()` 위에 적은 걸 실제로 만들려는 거구나

감만 잡으면 됩니다.

### 2. view를 떼어내기 & 입력폼 만들기
일단 메인(인덱스/루트) 페이지를 떼어냅시다.
`templates`라는 폴더를 만들어내고 파일명을 `index.html`로 할게요.
그럼 `/templates/index.html` 파일 안에는 간단한 게시글 입력폼을 넣어보겠습니다.

```html
<!DOCTYPE html>
<html>
    <head>
        <title>hey</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>게시판</h1>
        <p>게시판입니다.</p>
        <form action="/create">
            <input type="text" name="title">
            <input type="content" name="content">
            <input type="submit">
        </form>
    </body>
</html>
```
초단간 입력폼을 만들구요
1. 이 내용을 `/create`로 넘겨줄겁니다.
2. 제목은 `title`이라는 이름을 붙여주고
3. 내용은 `body`라는 이름을 붙여줬어요.

그리고 `app.py`의 코드를 바꿔줍니다.
```py
@app.route("/")
def index():
    return "Hack your life!"
```
원래 `"Hack your life"` 걍 글자 그대로 보내주던걸, `render_template()`을 통해 `index.html`로 보내줍니다.
```py
@app.route("/")
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)
    
```

날려줬으니 받아줘야 겠죠?

### 3. create_post 만들기
일단 `/create`라는 새로운 라우터를 하나 만들어주고, view template도 설정해줍니다.
```py
@app.route("/create")
def create():
    return render_template('create.html')
```
그리고 index page에서 날려준 데이터 두 개를 일단 받아서 보여줘 볼게요.
```py
@app.route("/create")
def create():
    form_title = request.args.get("title")
    form_content = request.args.get("content")
    return render_template('create.html', title=form_title, content=form_content)
```

당연히 `templates/create.html` 도 만들어줘야겠죠?
```html
<!DOCTYPE html>
<html>
    <head>
        <title>hey</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>게시판</h1>
        <p>게시물이 작성되었습니다.</p>
        <p>제목 : {{ title }}</p>
        <p>내용 : {{ content }}</p>
    </body>
</html>
```

파일 안에는 간단히 날아온 데이터를 받아서 보여줘 봅니다.
파이썬코드이기 때문에, `{{ }}`를 둘어주셔야 하는 거 잊지 마시구영.

저장 후에 서버를 돌리시고 확인해보세요 !

### 4. 데이터베이스에 post 저장하기
우리가 만든 form이 잘 작동하는 걸 알았으니, 
이제 데이터베이스를 활용해서 post를 **영구적으로 저장**해봅시다.

데이터베이스는 다른 거 없어요.
**1. 데이터를 영구적으로 저장한다.**
**2. 편하게 할거다.**
**2. 빠르게 할거다.**
이럴려고 쓰는 겁니다.
(지난 시간에 파일로 저장해 봤는데 엄청 불편했었죠?)

그럼 데이터베이스를 사용해볼텐데, 방법은 간단합니다.
SQL을 쓰는 대신에 ORM이라는 것을 통해 쓸건데,
Python 코드에 다가 문법도 엄청 직관적이에요.

우리는 `title`를 `body` 저장해줄거니까, `app.py` 파일에다가  

```py
@app.route("/create")
def create():
    form_title = request.args.get("title")
    form_content = request.args.get("content")
    return render_template('create.html', title=form_title, content=form_content)
```

이랬던 코드를 아래와 같이 바꿔주면 되요.
```py
@app.route("/create")
def create():
    # 1. params로 날라온 데이터를 각각에 저장해주고,
    form_title = request.args.get("title")
    form_content = request.args.get("content")

    # 2. 각각의 내용을 해당하는 데이터베이스 column에 맞게 저장해주면 됩니다.
    post = Post(title=form_title, content=form_content)
    db.session.add(post)

    # 3. 최종적으로 DB에 commit 해주시면 되요.
    db.session.commit()
    return render_template('create.html', title=form_title, content=form_content)
```

쉽졍? :)

### 5. SQL과 ORM(SQLAlchemy) 코드 비교
기본적으로 SQL로 가능한 모든 것들이 ORM을 통해서 가능합니다.
우선, 우리가 자주사용하는 CRUD(Create, Read/Retrieve, Update, Delete/Destroy) 관련 SQL 구문과 비교해 봅시다.

#### (1). Create == `INSERT`
레코드 추가하기
- SQL
```sql
INSERT INTO posts (title, content) VALUES ('제목입니다', '내용입니다.')
```

- ORM(SQLAlchemy)
```py
post = Post(title='제목입니다.', content='내용입니다.')
db.session.add(post)
```

#### (2). Read/Retrieve == `SELECT`
* **레코드 전부 불러오기**
- SQL
```sql
SELECT * FROM posts;
```

- ORM(SQLAlchemy)
```py
Post.query.all()
```

* **특정 조건의 레코드들 불러오기**
- SQL
```sql
SELECT * FROM posts WHERE title = '제목입니다.';
SELECT * FROM posts WHERE title = '제목입니다.' LIMIT 1;
```

- ORM(SQLAlchemy)
```py
Post.query.filter_by(title='제목입니다.').all()
Post.query.filter_by(title='제목입니다.').first()
```

* **특정 레코드 하나만 불러오기**
- SQL
```sql
SELECT * FROM posts WHERE id = 1;
```

- ORM(SQLAlchemy)
```py
Post.query.filter_by(id=1).first()
Post.query.get(1)
```

* **특정 레코드 불러와 숫자 세기**
- SQL
```sql
SELECT COUNT(*) FROM posts WHERE title = '제목입니다.';
```

- ORM(SQLAlchemy)
```py
Post.query.filter_by(title='제목입니다.').count()
```

#### (3). Update == `UPDATE`
- SQL
```sql
UPDATE posts SET title = '제목 변경' WHERE id = 1;
```

- ORM(SQLAlchemy)
```py
post = Post.query.get(1)
post.title = '제목 변경'
```

#### (4). Delete/Destroy == `DELETE`
- SQL
```sql
DELETE FROM posts WHERE id = 1;
```

- ORM(SQLAlchemy)
```py
post = Post.query.get(1)
db.session.delete(post)
```

#### (5). Commit == `commit` (DB에 적용!!)
- SQL
```sql
COMMIT;
```

- ORM(SQLAlchemy)
```py
db.session.commit()
```