from flask import Flask,render_template , request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///habits.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)


class Habit(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(200), nullable=False)
    frequency=db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(50)) 
    date=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Habit(sno={self.sno}, name={self.name}, frequency={self.frequency}, status={self.status}, date={self.date})"
        
    


@app.route("/", methods=["GET" , "POST"])
def hello_world():
    if (request.method=="POST"):
            name = request.form['name']
            frequency = request.form['frequency']
            status = request.form['status']  # Get status input from user
            new_habit = Habit(name=name, frequency=frequency, status=status)
            db.session.add(new_habit)
            db.session.commit()
    allHabits=Habit.query.all()
  

    return render_template('index.html',habits=allHabits)
   
@app.route('/delete/<int:sno>')
def delete(sno):
    allHabits=Habit.query.filter_by(sno=sno).first()
    db.session.delete(allHabits)
    db.session.commit()
    return redirect('/habits')

@app.route('/habits')
def habits():
    
    allHabits = Habit.query.all()
    return render_template('habits.html', habits=allHabits)


if __name__=="__main__":
    app.run(debug=True,port=8000)