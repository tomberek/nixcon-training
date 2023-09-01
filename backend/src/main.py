from flask import Flask

import sqlite3

app = Flask(__name__)
db = "local.db"
con = sqlite3.connect(db)
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS name(name,created_on)")
con.close()

@app.route("/")
def hello_world():
    con = sqlite3.connect("local.db")
    cur = con.cursor()
    res = cur.execute("SELECT name FROM NAME").fetchall()
    res = [f'<li>{x[0]}</li>' for x in res]
    res = "\n".join(res)
    con.close()
    return f'''
    <p>Hello, World!</p>
    <ul>
    {res}
    </ul>'''

@app.route("/<name>")
def hello_name(name):
    con = sqlite3.connect("local.db")
    cur = con.cursor()
    cur.execute('INSERT INTO name (name,created_on) VALUES(?,CURRENT_TIMESTAMP)',[name])
    con.commit()
    con.close()
    return f"<p>Hello, {name}!</p>"

if __name__ == "__main__":
    app.run(debug=True)
