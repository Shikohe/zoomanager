from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SECRET_KEY'] = 'secret'
db = SQLAlchemy(app)


class Animal(db.Model):
    __tablename__ = 'animals'
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(100))
    breed = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(100))

    # to_dict მეთოდს ვქმნით Student მოდელის ლექსიკონად გადაქასთვის ფუნქციონალისთვის
    def to_dict(self):
        return {
            'id': self.id,
            'kind': self.kind,
            'breed': self.breed,
            'age': self.age,
            'gender': self.gender
        }


class AnimalForm(FlaskForm):
    kind = StringField('kind')
    breed = StringField('breed')
    age = IntegerField('age')
    gender = StringField('gender')
    create = SubmitField('Create')


@app.route('/')
def get_animals():
    animals = [animal.to_dict() for animal in Animal.query.all()]
    lst = []
    lst1 = []
    dickt = {}
    for animal in animals:
        lst.append(animal['kind'].lower())
    for i in lst:
        if i not in lst1:
            lst1.append(i)

    for animal in lst1:
        dickt[str(animal)] = lst.count(str(animal))
    return render_template('index.html', dickt=dickt)


@app.route('/add/animals', methods=['POST', 'GET'])
def create_animal():
    form = AnimalForm()
    if form.validate_on_submit():
        kind = form.kind.data.lower()
        breed = form.breed.data
        age = form.age.data
        gender = form.gender.data
        animal = Animal(kind=kind, breed=breed, age=age, gender=gender)
        db.session.add(animal)
        db.session.commit()
        return redirect('/add/animals')
    return render_template('add_animal.html', form=form)


@app.route('/update/animals/<int:id>', methods=['POST','GET'])
def update_animal(id):
    form = AnimalForm()
    animal = Animal.query.get(id)
    if form.validate_on_submit():
        animal.kind = form.kind.data
        animal.breed = form.breed.data
        animal.age = form.age.data
        animal.gender = form.gender.data
        db.session.commit()
        return "Update done"
    return render_template('update_animal.html',form=form,animal=animal)


@app.route('/api')
def api():
    animals = [animal.to_dict() for animal in Animal.query.all()]
    return animals

@app.route('/delete/animals/<int:id>')
def delete_animal(id):
    animal = Animal.query.get(id)
    db.session.delete(animal)
    db.session.commit()
    return "Successfully delete", 200


@app.route('/animals')
def index_page():
    animals = [animal.to_dict() for animal in Animal.query.all()]
    return render_template('index.html', animals=animals)


@app.route('/animals/<string:kind>')
def same_kind_animals(kind):
    animal = [animal.to_dict() for animal in Animal.query.filter(Animal.kind == kind)]
    return render_template('info_animal.html', animal=animal)


with app.app_context():
    db.create_all()
    app.run()
