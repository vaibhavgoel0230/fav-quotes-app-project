from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///favquote.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db= SQLAlchemy(app)

class Favquotes(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    author = db.Column(db.String(30))
    quote = db.Column(db.String(2000))

@app.route('/')
def index():
    result = Favquotes.query.all()
    return render_template('index.html',result=result)

@app.route('/quotes')
def quotes():
    return render_template('quotes.html')

@app.route('/process',methods=['POST'])
def process():
    author=request.form['author']
    quote=request.form['quote']
    quotedata = Favquotes(author=author,quote=quote)
    db.session.add(quotedata)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    favquote = Favquotes.query.get_or_404(id)
    if request.method =='POST':
        favquote.author = request.form.get('author')
        favquote.quote = request.form.get('quote')
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There is a problem in updating your quote."
    else:
        return render_template('update.html',favquote=favquote)

@app.route('/delete/<int:id>')
def delete(id):
    favquote = Favquotes.query.get_or_404(id)
    try:
        db.session.delete(favquote)
        db.session.commit()
        return redirect('/')
    except:
        return "There is a problem in deleting your quote."

