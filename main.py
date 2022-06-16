from flask import Flask, render_template, request, jsonify
import pymysql

app = Flask(__name__)
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234', db='ai_college', charset="utf8")
cursor = db.cursor()

"""
0610 실습
"""


@app.route("/", methods=["GET"])
def hello():
    return "Hello World"


@app.route("/page", methods=["GET"])
def main_page():
    return render_template('index.html')


@app.route("/query", methods=["GET"])
def query_test():
    my_name = request.args.get("name")
    print(my_name)
    return "OK"


@app.route("/animal", methods=["GET"])
def query_practice():
    name = request.args.get("name")
    age = request.args.get("age")
    print(f'{age}살의 {name}')
    return "got animal"


@app.route("/body", methods=["POST"])
def body_test():
    my_name = request.form["name"]
    print(my_name)
    return "Body OK"


@app.route("/vehicle", methods=["POST"])
def vehicle_test():
    type_of_vehicle = request.form["type"]
    print(type_of_vehicle)
    return "OK"


@app.route("/json-test", methods=["GET"])
def json_test():
    fruits = []
    fruits.append({
        'name': '사과',
        'price': 500
    })
    fruits.append({
        'name': '수박',
        'price': 1000
    })
    return jsonify(fruits)


@app.route("/db-test", methods=["GET"])
def db_test():
    # sql = """select * from members"""
    # cursor.execute(sql)
    # results = cursor.fetchall()
    # print(results)
    sql = "insert into members (name, age, signedup) values ('홍길동', 31, '2022-06-10-21:31:25')"
    cursor.execute(sql)
    db.commit()
    return "OK"



"""
-------------------------------------------------------------------------
client <-> server <-> db
-------------------------------------------------------------------------
"""
@app.route("/book", methods=["POST"])
def book():
    server_name = request.form["name"]
    print(server_name)
    sql = "insert into books (name) values('%s')" % server_name
    cursor.execute(sql)
    db.commit()
    return "OK"


@app.route("/book/list", methods=["GET"])
def get_book():
    book_list = []
    sql = "select * from books"
    cursor.execute(sql)
    results = cursor.fetchall()
    for result in results:
        book_id = result[0]
        book_name = result[1]
        book_list.append({'id': book_id,
                          'name': book_name})
    # print(jsonify(book_list))
    return jsonify(book_list)


@app.route("/book", methods=["PUT"])
def update_book():
    server_id = request.form["id"]
    server_name = request.form["name"]
    # print(server_name, server_id)
    sql = "update books SET name = '%s'  where id = %s" % (server_name, server_id)
    cursor.execute(sql)
    db.commit()
    return "OK"


@app.route("/book", methods=["DELETE"])
def delete_book():
    server_id = request.args.get("id")
    sql = "delete from books where id = %s" % server_id
    cursor.execute(sql)
    db.commit()
    return "OK"




"""
-------------------------------------------------------------------------
영화 예제 페이지 만들기
-------------------------------------------------------------------------
"""
@app.route("/movie_page", methods=["GET"])
def movie_page():
    return render_template('index_movie.html')


@app.route("/movie", methods=["GET"])
def get_movies():
    sql = "select * from movie"
    cursor.execute(sql)
    results = cursor.fetchall()
    movies = []
    for result in results:
        movies.append({
            'id': result[0],
            'name': result[1],
            'score': result[2]
        })
    # print(results)
    db.commit()
    return jsonify(movies)


@app.route("/movie", methods=["POST"])
def post_movie():
    server_name = request.form["name"]
    server_score = request.form["score"]
    # print(server_name, server_score)
    sql = "insert into movie (name, score) value ('%s', %s)" % (server_name, server_score)
    cursor.execute(sql)
    db.commit()
    # print(server_name, server_score)
    return "OK"


@app.route("/movie/all", methods=["DELETE"])
def delete_movies():
    sql = "delete from movie"
    cursor.execute(sql)
    db.commit()
    return "OK"




"""
-------------------------------------------------------------------------
학생 정보 페이지 만들기
-------------------------------------------------------------------------
"""
@app.route("/student_page", methods=["GET"])
def student_page():
    return render_template("index_student_db.html")


@app.route("/student/list", methods=["GET"])
def get_student():
    sql = "select * from student"
    cursor.execute(sql)
    results = cursor.fetchall()
    # results = ((id, name, age),(),...)
    students = []
    for result in results:
        students.append({
            "id": result[0],
            "name": result[1],
            "age": result[2]
        })
    db.commit()
    return jsonify(students)


@app.route("/student", methods=["POST"])
def post_student():
    server_id = request.form["id"]
    server_name = request.form["name"]
    server_age = request.form["age"]
    sql = "insert into student (id, name, age) value (%s, '%s', %s)" % (server_id, server_name, server_age)
    cursor.execute(sql)
    db.commit()
    return "OK"


@app.route("/student", methods=["PUT"])
def put_student():
    server_id = request.form["id"]
    server_name = request.form["name"]
    server_age = request.form["age"]
    sql = "update student SET name='%s', age=%s where id=%s" % (server_name, server_age, server_id)
    cursor.execute(sql)
    db.commit()
    return "OK"


@app.route("/student", methods=["DELETE"])
def delete_student():
    server_id = request.args.get("id")
    sql = "delete from student where id=%s" % server_id
    cursor.execute(sql)
    db.commit()
    return "OK"


if __name__ == "__main__":
    app.run(debug=True)
