from flask import Flask,render_template,url_for,request,redirect
#connecting with mysql
import mysql.connector
from cmail import sendmail
from otp import genotp
app=Flask(__name__)
#SECRET KEY
app.config['SECRET_KEY']="my super secret key that no one is supposed to know"
mydb=mysql.connector.connect(host='localhost',user='root',password='system',db='sirisha')
with mysql.connector.connect(host='localhost',user='root',password='system',db='sirisha'):
    cursor=mydb.cursor(buffered=True)
    cursor.execute("create table if not exists registration(username varchar(20) primary key, mobile varchar(20) unique,address varchar(30),password varchar(18),email varchar(100))")

mycursor=mydb.cursor()
@app.route('/reg',methods=['GET','POST'])
def reg():
    if request.method=="POST":
        username=request.form['username']
        mobile=request.form['mobile']
        email=request.form['email']
        address=request.form['address']
        password=request.form['password']
        otp=genotp()
        sendmail(to=email,subject="thanks for registration",body=f'otp is :{otp}')
        return render_template('verification.html',username=username,mobile=mobile,address=address,password=password,email=email,otp=otp)
    return render_template('registration.html')
@app.route('/otp/<username>/<mobile>/<address>/<password>/<email>/<otp>',methods=['GET','POST'])  
def otp(username,mobile,address,password,email,otp): 
    if request.method=='POST':
        uotp=request.form['uotp']
        if otp==uotp:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('insert into registration values(%s,%s,%s,%s,%s)',[username,mobile,address,password,email])
            mydb.commit()
            cursor.close()
            return redirect(url_for('login'))
            #return "success"
    return render_template('verification.html',username=username,mobile=mobile,address=address,password=password,email=email,otp=otp)
    
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        print(username)
        print(password)
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from registration where username=%s && password=%s',[username,password])
        data=cursor.fetchone()[0]
        if data==1:
            session['username']=username
            if not session.get(session['username']):
                session[session['username']]={}
            return redirect(url_for('home'))
        else:
            return "Invalid Username or password"
    return render_template('login.html')

@app.route('/logout')
def logout():
    if session.get('username'):
        session.pop('username')
    return redirect(url_for('login'))

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/addpost',methods=['GET','POST'])
def add_post():
    if request.method=="POST":
        title=request.form['title']
        content=request.form['content']
        slug=request.form['slug']
        print(title)
        print(content)
        print(slug)
        cursor=mydb.cursor(buffered=True)
        cursor.execute('insert into posts(title,content,slug) values(%s,%s,%s)',[title,content,slug])
        mydb.commit()
        cursor.close()
    return render_template('add_post.html')

#create admin page
@app.route('/admin')
def admin():
    return render_template('admin.html')   

#view posts
@app.route('/view_posts')
def view_posts():
    cursor=mydb.cursor(buffered=True)
    cursor.execute("select * from posts")
    posts=cursor.fetchall()
    print(posts)
    cursor.close()
    return render_template('view_posts.html',posts=posts)  

#Delete post route
@app.route('/delete_post/<int:id>',methods=["POST"])
def delete_post(id):
    print(id)
    cursor=mydb.cursor(buffered=True)
    cursor.execute("select * from posts where id=%s",(id,))
    post=cursor.fetchone()
    cursor.execute("delete from posts where id=%s",(id,))
    print(post)
    mydb.commit()
    cursor.close()
    return redirect(url_for("view_posts"))

#updating a post
@app.route('/update_post/<int:id>',methods=['GET',"POST"])
def update_post(id):
    if request.method=='POST':
        title=request.form["title"]
        content=request.form["content"]
        slug=request.form["slug"]
        cursor=mydb.cursor(buffered=True)
        #cursor.execute("select * from posts where id=%s",(id,))
        #post=cursor.fetchall()
        cursor.execute("update posts set title=%s,content=%s,slug=%s where id=%s",(title,content,slug,id))
        mydb.commit()
        cursor.close()
        return redirect(url_for('view_posts'))
    else:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select * from posts where id=%s',(id,))
        post=cursor.fetchone()
        cursor.close()
        return render_template('update_post.html',post=post)
app.run(debug=True,use_reloader=True)