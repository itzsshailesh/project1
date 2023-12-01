from flask import Flask,render_template,request,session,redirect,url_for,g,flash

app=Flask(__name__)
app.secret_key="123"

class User:
    def __init__(self,id,username,password):
        self.id=id
        self.username=username
        self.password=password

users=[]
users.append(User(id=1,username='demo',password='demo'))
users.append(User(id=2,username='demouser',password='demouser'))

@app.route("/",methods=['GET','POST'])
def login():
    if request.method=='POST':
        uname=request.form['uname']
        upass = request.form['upass']

        for data in users:
            if data.username==uname and data.password==upass:
                session['userid']=data.id
                g.record=1
                return redirect(url_for('user'))
            else:
                g.record=0
        if g.record!=1:
            flash("data not found")
            return redirect(url_for('login'))
    return render_template("home.html")


@app.before_request
def before_request():
    if 'userid' in session:
        for data in users:
            if data.id==session['userid']:
                g.user=data

@app.route('/user')
def user():
    if not g.user:
        flash("Username or Password Mismatch...!!!")
        return redirect(url_for('login'))
    return render_template('user.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
 
if __name__=='__main__':
    app.run(debug=True)