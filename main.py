from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from flask import flash
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pet.db'
db = SQLAlchemy(app)
app.secret_key = 'your_secret_key'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

path_to_save_images = os.path.join(app.root_path, 'static', 'imgs')

class Pets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo_name = db.Column(db.String(500), unique=True)
    pet_name = db.Column(db.String(500))
    h_old = db.Column(db.String(500))
    helth_st = db.Column(db.String(500))

    def __init__(self, photo_name, pet_name,h_old,helth_st):
        self.photo_name = photo_name
        self.pet_name = pet_name
        self.h_old = h_old
        self.helth_st = helth_st
 
    def __repr__(self):
        return '<pets %r>' % (self.pet_name)
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    json_data = []
    files = os.listdir("static//imgs")
    for i in range(5):
        json_data.append(files[i])
    lenght = 5
    return render_template('index.html', json_data=json_data, lenght=lenght)

@app.route('/admin_auth', methods=['GET', 'POST'])
def admin_auth():
  error = None
  if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']
      if username == 'admin' and password == 'jp3QkmubP': 
            session['user_id'] = 2
            return redirect(url_for('admin_panel'))

      else:
          error = 'Неправильное имя пользователя или пароль'
  return render_template('admin_author.html')

@app.route('/admin_panel', methods=['GET', 'POST'])
def admin_panel():
    if 'user_id' not in session:
        return redirect(url_for('admin_auth'))
    json_data = []
    res = Pets.query.all()
    for i in range(len(res)):
        json_data.append([res[i].id,res[i].photo_name,res[i].pet_name,res[i].h_old,res[i].helth_st])

    if request.method == 'POST':
        me = Pets.query.filter_by(id=request.form['id']).first()
        file = request.files['img']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(path_to_save_images, filename)
            file.save(save_path)
        add_pet = Pets(filename,request.form['pet_name'],request.form['h_old'], request.form["helth_st"])
        db.session.delete(me)
        db.session.add(add_pet)
        db.session.commit()
    return render_template('admin_panel.html', json_data=json_data)

@app.route("/admin_panel_add", methods=['GET', 'POST'])
def admin_panel_add():
    if 'user_id' not in session:
        return redirect(url_for('admin_auth'))
    if request.method == 'POST':
      file = request.files['img']
      if file and allowed_file(file.filename):
          filename = secure_filename(file.filename)
          save_path = os.path.join(path_to_save_images, filename)
          file.save(save_path)
      add_pet = Pets(filename,request.form['pet_name'],request.form['h_old'], request.form["helth_st"])
      db.session.add(add_pet)
      db.session.commit()
    return render_template('admin_panel_add.html')

@app.route("/admin_panel_delete", methods=['GET', 'POST'])
def admin_panel_delete():
    if 'user_id' not in session:
        return redirect(url_for('admin_auth'))
    json_data = []
    res = Pets.query.all()
    for i in range(len(res)):
        json_data.append([res[i].id,res[i].photo_name,res[i].pet_name,res[i].h_old,res[i].helth_st])
    if request.method == 'POST':
        me = Pets.query.filter_by(id=request.form['id']).first()
        db.session.delete(me)
        db.session.commit()
    return render_template('admin_panel_delete.html', json_data=json_data)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/pet_list', methods=['GET', 'POST'])
def pet_list():
    json_data = []
    res = Pets.query.all()
    for i in range(len(res)):
        json_data.append([res[i].id,res[i].photo_name,res[i].pet_name,res[i].h_old,res[i].helth_st])
    return render_template('pets.html', json_data=json_data)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')

if __name__=='__main__':
  app.run(debug=True)