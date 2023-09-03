from flask import Flask
import markupsafe
import os

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
    res = [f'''
       <li hx-get="/api/{markupsafe.escape(x[0])}/created" hx-target="find span" hx-trigger="click throttle:1s">
        {markupsafe.escape(x[0])}<span></span>
       </li>''' for x in res]
    res = "\n".join(res)
    con.close()
    return f'''
    <p>Hello, World! I have said "hello" to the following:</p>
    <ul>
    {res}
    </ul>'''

@app.route("/<name>/created",methods = ['GET'])
def hello_name_created(name):
    con = sqlite3.connect("local.db")
    cur = con.cursor()
    res = cur.execute(f'SELECT created_on FROM NAME WHERE name = ?',[name]).fetchall()
    con.commit()
    con.close()
    return f':&nbsp;created on {markupsafe.escape("".join(res[0]))}'

@app.route("/<name>",methods = ['POST','GET'])
def hello_name(name):
    con = sqlite3.connect("local.db")
    cur = con.cursor()
    cur.execute('INSERT INTO name (name,created_on) VALUES(?,CURRENT_TIMESTAMP)',[name])
    con.commit()
    con.close()
    return f"<p>Hello, {markupsafe.escape(name)}!</p>"

if __name__ == "__main__":
    app.run(port=(os.getenv("PORT",5000)),debug=True)
