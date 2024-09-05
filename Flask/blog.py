from flask import Flask, render_template, flash, redirect, url_for,session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, EmailField
from passlib.hash import sha256_crypt

#Kullanıcı Kayıt Formu
class RegisterForm(Form):
    name = StringField("İsim Soyisim", validators=[validators.Length(min = 4, max = 25)])
    username = StringField("Kullanıcı Adı", validators=[validators.Length(min = 5, max = 35)])
    email = StringField("Email Adresi", validators=[validators.Email(message= "lütfen geçerli bir email adresi giriniz.")])
    password = PasswordField("Parola", validators=[
        validators.Length(min = 4, max = 25), 
        validators.DataRequired(message="Lütfen bir parola belirleyiniz!!"), 
        validators.EqualTo(fieldname="confirm",message="Parolalar uyuşmuyor")
    ])
    confirm = PasswordField("Parola Doğrula")

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost" #buraya sunucu adresi girilir normalde
app.config["MYSQL_USER"] = "root" 
app.config["MYSQL_PASSWORD"] = "" 
app.config["MYSQL_DB"] = "Database1" 
app.config["MYSQL_CURSORCLASS"] = "DictCursor" 
app.config["MYSQL_UNIX_SOCKET"] = "/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock"

mysql = MySQL(app)




@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/articles")
def articles():
    return render_template("articles.html")

@app.route("/register",methods = ["GET", "POST"])
def register():
    form1 = RegisterForm(request.form)

    if request.method == "POST" and form1.validate():
        name = form1.name.data
        username = form1.username.data
        email = form1.email.data
        password = sha256_crypt.encrypt(form1.password.data)

        cursor = mysql.connection.cursor()

        sorgu = "INSERT INTO users(name,email,username,password) VALUES(%s,%s,%s,%s)"
        cursor.execute(sorgu,(name,email,username,password))
        mysql.connection.commit() #veri güncelleme işlemi yaptıktan sonra bu komutu kullanmalıyız

        cursor.close()

        return redirect(url_for("index"))
    
    else:
        return render_template("register.html", form = form1) #form1 i register.html'ye form olarak gönderiyoruz

if __name__ == "__main__": 
    #eğer bu dosya terminalden çalıştırılırsa __name__ = __main__ olacak
    #ancak bu dosya bir modül olarak kullanılırsa bu şart sağlanacak
    
    app.run(debug=True)




