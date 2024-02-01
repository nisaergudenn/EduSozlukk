from flask import Flask ,render_template, request,redirect
import pymongo
app = Flask(__name__)

client = pymongo.MongoClient("mongodb://localhost:27018/")
db = client["EduSozlukDB"]


@app.route('/hello/<name>')
def hello_name (name) :
    return 'Hello %s!' % name


@app.route ('/')
def home_page () :
    return render_template("home.html")

@app.route('/uye-ol', methods=["GET", "POST"])
def uye_ol ():
    if request.method =='GET' :
        return render_template("uye-ol.html")
    else:
        email = request.form["email"]
        sifre = request.form["sifre"]
        adsoyad = request.form["adsoyad"]

        db["kullanicilar"].insert_one({
            "_id": email,
            "sifre": sifre,
            "adsoyad": adsoyad
        })
        return redirect("/giris",302)
@app.route('/giris', methods =["GET", "POST"])
def giris():
    if request.method == 'GET' :
        return render_template("giris.html")
    else:
        email = request.form["email"]
        sifre = request.form["sifre"]
        adsoyad = request.form["adsoyad"]

        kullanici = db["kullanicilar"].find_one({"_id": email})
        print("kullanici:", kullanici)
        if kullanici and kullanici["sifre"] == sifre:
            return redirect("/", 302)
        else:
            return "Kullanıcı Bulunamadı ya da Şifre Hatalı"

if __name__ == ' __main__' :
    app.run (debug = True, host = "0.0.0.0", port = 5000 )
