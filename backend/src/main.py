from flask import Flask, request
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
       <li hx-get="/api/{o}/created"
           hx-disinherit="*"
           hx-target="find span"
           hx-swap="outerHTML settle:1s"
           hx-trigger="click throttle:1s">{o}<span></span>
       </li>''' for x in res if (o := markupsafe.escape(x[0]))]
    res = "\n".join(res)
    con.close()
    return f'''
    <p>Hello, World! I have said "hello" to the following:</p>
    <ul title="click on a name to see creation date">
    {res}
    </ul>'''

@app.route("/<name>/created",methods = ['GET'])
def hello_name_created(name):
    con = sqlite3.connect("local.db")
    cur = con.cursor()
    res = cur.execute(f'SELECT created_on FROM NAME WHERE name = ?',[name]).fetchall()
    stamp = markupsafe.escape("".join(res[0]))
    con.commit()
    con.close()
    return f'''<span _="on click set my innerText to '' then halt">:&nbsp;created on {stamp}</span>'''

@app.route("/",methods = ['POST'])
def hello_name():
    name=request.form.get('name','')
    if name == "":
        return f"unable to process '{name}'", 204
    con = sqlite3.connect("local.db")
    cur = con.cursor()
    cur.execute('INSERT INTO name (name,created_on) VALUES(?,CURRENT_TIMESTAMP)',[name])
    con.commit()
    con.close()
    return f"<p>Hello, {markupsafe.escape(name)}!</p>"

if __name__ == "__main__":
    app.run(port=(os.getenv("PORT",5000)),debug=True)
