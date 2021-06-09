import backend
from flask import Flask, request, render_template, url_for, redirect, jsonify, make_response
from flask_mysqldb import MySQL
from secret import password, secret_key
import datetime
import jwt
import uuid
from functools import wraps

#TODO rute 2, akses database mySQL dan menampilkannya di web
#TODO autentikasi

#Global Variables
array_csv_formatted = None
current_token = None

app = Flask(__name__)

#Database Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = password
app.config['MYSQL_DB'] = 'irk_task8'
app.config['SECRET_KEY'] = secret_key

mysql = MySQL(app)

def token_required(func):
    @wraps(func)
    def decorated():
        
        if (current_token==None):
            return jsonify({'message' : 'Token is missing !!'}), 401

        # decoding the payload to fetch the stored details
        data = jwt.decode(current_token, app.config['SECRET_KEY'],algorithms=["HS256"])
        
        #cek database
        cur = mysql.connection.cursor()
        getting = "SELECT * FROM users WHERE public_id=%s;"

        values = data['public_id']
        
        cur.execute(getting, [values])

        rv = cur.fetchall()

        mysql.connection.commit()
        cur.close()

        if (len(rv)!=0):
            return func()
        else:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
            
    return decorated

@app.route('/')
def mainPage():
    return render_template('main-page.html')

@app.route('/user',methods=['POST'])
def register():
    username = request.form.get('username-registration-specifier')
    password = request.form.get('password-registration-specifier')
    public_id = str(uuid.uuid4())

    #masukkan ke database
    cur = mysql.connection.cursor()
    inserting = "INSERT INTO users VALUES (%s,%s,%s);"
    values = (public_id,username,password)
    
    cur.execute(inserting, values)
    mysql.connection.commit()
    cur.close()

    return render_template('main-page.html') + "REGISTER SUCCESS"

@app.route('/user')
def login():
    global current_token

    username = request.args.get('username-login-specifier')
    password = request.args.get('password-login-specifier')

    #cek database
    cur = mysql.connection.cursor()
    inserting = "SELECT public_id FROM users WHERE username=%s AND password=%s;"
    values = (username,password)
    
    cur.execute(inserting, values)

    rv = cur.fetchone()

    token = None
    if (rv==None):
        return "WRONG USERNAME OR PASSWORD"
    else:
        current_token = jwt.encode({'public_id':rv[0]},app.config['SECRET_KEY'],algorithm="HS256")

    mysql.connection.commit()
    cur.close()

    return render_template('main-page.html') + "LOGIN SUCCESS"


@app.route('/sort/', methods=['GET','POST'])
@token_required
def sortPage():
    global array_csv_formatted

    if (request.method=='POST'):
        csv_file = request.files['file-uploader']
        array_csv_formatted = backend.parser(backend.fileStorageToText(csv_file))

        if (request.form.get('algorithm-specifier')=="selection"):
            return redirect(url_for('.sort_selection'), code=307)       #307 ini mempertahankan method yang sebelumnya ke url selanjutnya
        elif (request.form.get('algorithm-specifier')=="merge"):
            return redirect(url_for('.sort_merge'), code=307) 

    elif (request.method=='GET'):
        return redirect(url_for('.result_page'),code=307)
    

@app.route('/sort/selection',methods=['POST'])
def sort_selection():
    #execution
    backend.preprocessTable(array_csv_formatted)
    value = backend.sort_selection(array_csv_formatted,int(request.form.get('column-specifier')),request.form.get('order-specifier'))
    stringHasil = backend.arrayToText(value[0])

    #masukkan ke database
    cur = mysql.connection.cursor()
    inserting = "INSERT INTO roots(tanggal_eksekusi,algoritma,hasil,execution_time) VALUES (SYSDATE(),%s,%s,%s);"
    values = (request.form.get('algorithm-specifier'),stringHasil,value[1])
    
    cur.execute(inserting, values)
    mysql.connection.commit()
    cur.close()

    return render_template('sort-result-page.html',arrayWillShown = value[0], column = len(value[0][0]) , row=len(value[0]), executionTime=value[1])

@app.route('/sort/merge',methods=['POST'])
def sort_merge():
    #execution
    backend.preprocessTable(array_csv_formatted)
    value = backend.sort_merge(array_csv_formatted,int(request.form.get('column-specifier')),request.form.get('order-specifier'))
    stringHasil = backend.arrayToText(value[0])

    #masukkan ke database
    cur = mysql.connection.cursor()
    inserting = "INSERT INTO roots(tanggal_eksekusi,algoritma,hasil,execution_time) VALUES (SYSDATE(),%s,%s,%s);"
    values = (request.form.get('algorithm-specifier'),stringHasil,value[1])
    
    cur.execute(inserting, values)
    mysql.connection.commit()
    cur.close()

    return render_template('sort-result-page.html',arrayWillShown = value[0], column = len(value[0][0]), row=len(value[0]), executionTime = value[1])

@app.route('/sort/result')
@token_required
def result_page():
    #getting id
    id = request.args.get("id-specifier")

    #getting query
    cur = mysql.connection.cursor()
   
    if (not id):
        getting = "SELECT * FROM roots ORDER BY id DESC LIMIT 1"
        cur.execute(getting)
    else:
        getting = "SELECT * FROM roots WHERE id=%s"
        cur.execute(getting, [id])
     
    rv = cur.fetchall()
    mysql.connection.commit()
    cur.close()

    if (len(rv)==0):    #ga ketemu
        return "ID NOT IDENTIFIED!"
    else:
        value = backend.parser(rv[0][3])
    
        return render_template('sort-result-page.html',arrayWillShown = value, column = len(value[0]), row=len(value), executionTime = rv[0][4])
    
    

if __name__ == "__main__":
    app.run()