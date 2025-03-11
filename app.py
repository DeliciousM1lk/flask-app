from flask import Flask, render_template, url_for, request, redirect
import psycopg2
# для запуска Flask приложения
app = Flask(__name__)

DB_NAME = 'todo_db' # нужно пересмотреть
DB_USER = 'postgres' # v
DB_PASSWORD = '1234Aa' # нужно пересмотреть
DB_HOST = 'localhost' # v
DB_PORT = '5432' # v


# Связь postgresql с flask
def get_db_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    print("БД подключена из Postgresql")
    return conn


@app.route('/')
def home_view():
    conn = get_db_connection()
    cur = conn.cursor() # sql executer
    cur.execute("SELECT * FROM todos");
    items = cur.fetchall() # извлечь все данные от SQL
    cur.close()
    conn.close()
    return render_template("home.html", items=items)

@app.route('/read/<int:id>')
def read_view(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM todos WHERE id = %s", (id,));
    item = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('read.html', item=item)

@app.route('/create', methods=['GET', 'POST'])
def create_view():
    if request.method == "POST":
        content = request.form['content']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO todos(content) VALUES (%s)", (content,))
        conn.commit() # хранение данных
        cur.close()
        conn.close()
        return redirect(url_for('home_view'))
    return render_template("create.html")

@app.route('/delete/<int:id>', methods=['POST'])
def delete_view(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM todos WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('home_view'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_view(id):
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == "POST":
        content = request.form['content']
        cur.execute("UPDATE todos SET content = %s WHERE id = %s", (content, id,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('home_view'))
    cur.execute("SELECT * FROM todos WHERE id = %s", (id,))
    item = cur.fetchone()
    cur.close()
    conn.close()
    return render_template("update.html", item=item)


@app.route("/search", methods=['GET'])
def search_view():
    query = request.args.get('q')
    if query:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM todos WHERE content LIKE %s", ("%" + query + "%", ))
        items = cur.fetchall()
        cur.close()
        conn.close()
        return render_template("home.html", items=items, query=query)
    else:
        return redirect(url_for('home_view'))

if __name__ == "__main__":
    app.run(debug=True, port=8080)