from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuration base de données SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///etudiants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modèle Etudiant
class Etudiant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    classe = db.Column(db.String(50), nullable=False)

# Page d'accueil : liste des étudiants
@app.route('/')
def index():
    etudiants = Etudiant.query.all()
    return render_template('index.html', etudiants=etudiants)

# Page pour ajouter un étudiant
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        age = request.form['age']
        classe = request.form['classe']
        etudiant = Etudiant(nom=nom, prenom=prenom, age=age, classe=classe)
        db.session.add(etudiant)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')  # page formulaire séparée

# Supprimer un étudiant
@app.route('/delete/<int:id>')
def delete(id):
    etudiant = Etudiant.query.get(id)
    db.session.delete(etudiant)
    db.session.commit()
    return redirect(url_for('index'))

# Modifier un étudiant
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    etudiant = Etudiant.query.get(id)
    if request.method == 'POST':
        etudiant.nom = request.form['nom']
        etudiant.prenom = request.form['prenom']
        etudiant.age = request.form['age']
        etudiant.classe = request.form['classe']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', etudiant=etudiant)

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()    # supprime toutes les tables pour recréer proprement
        db.create_all()  # crée toutes les tables
    app.run(host="0.0.0.0", port=5002, debug=True)
    
