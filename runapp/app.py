# import necessary libraries
from flask import (
    Flask,
    render_template,
    jsonify,
    request)
import json
from flask_sqlalchemy import SQLAlchemy
from decimal import Decimal

app = Flask(__name__)
markdown = """
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/db.sqlite"

db = SQLAlchemy(app)


class Food(db.Model):
    __tablename__ = 'foods'

    id = db.Column(db.Integer, primary_key=True)
    foodname = db.Column(db.String(64))
    foodprotein = db.Column(db.Numeric(6,3))
    foodcals = db.Column(db.Numeric(6,3))
    foodweight = db.Column(db.Numeric(6,3))

    def __repr__(self):
        return '<Food %r>' % (self.foodname)


@app.before_first_request
def setup():
    # Recreate database each time for demo
    db.drop_all()
    db.create_all()


@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        foodname = request.form["foodname"]
        foodprotein = request.form["foodprotein"]
        foodcals = request.form["foodcals"]
        foodweight = request.form["foodweight"]

        food = Food(foodname=foodname, foodprotein=foodprotein, foodcals=foodcals, foodweight=foodweight)
        db.session.add(food)
        db.session.commit()

        return "Thanks for the form data!"

    return render_template("form.html")


@app.route("/api/data")
def list_foods():
    results = db.session.query(Food.foodname, Food.foodprotein, Food.foodcals, Food.foodweight).all()

    foods = []
    for result in results:
        foods.append({
            "foodname": result[0],
            "foodprotein": str(result[1]),
            "foodcals": str(result[2]),
            "foodweight": str(result[3])
        })
    return json.dumps(foods)
"""

@app.route("/tester")
def home():
    return "Welcome!"

@app.route("/", methods=["GET", "POST"])
def tester():
    if request.method == "POST":
        extraprotein = Decimal(request.form["extraprotein"])
        extracals = Decimal(request.form["extracals"])

        meatservprotein = Decimal(request.form["foodprotein1"])
        meatservcals = Decimal(request.form["foodcals1"])
        meatservweight = Decimal(request.form["foodweight1"])

        nonmeatservprotein = Decimal(request.form["foodprotein2"])
        nonmeatservcals = Decimal(request.form["foodcals2"])
        nonmeatservweight = Decimal(request.form["foodweight2"])

        if extraprotein == "":
            extraprotein = 0
        else:
            extraprotein = extraprotein
        if extracals == "":
            extracals = 0
        else:
            extracals = extracals

        basecals = 317
        baseprotein = 30
        #create a variable for the amount of calories you want in your meal
        totalcals = basecals - extracals
        #create a variable for the amount of protein you want in your meal 
        meatprotein = baseprotein - extraprotein
        #create a variable for foods with no protein (salad dressing, condiments, candy, etc.)
        empty_cals = 8
        #make a counter; this will allow your code to acheive the best balance possible between your foods
        counter = 10
        #initialize a value for the protein you'll get from non-meats
        nonmeatprotein = 0

        #     Start a loop; creating a loop allows you to approach to most 
        #     efficient balance without ever reaching it, like an asymptote in trigonometry/calculus
        
        while counter > 0:
            sparecals = totalcals - empty_cals - (((meatprotein-nonmeatprotein)/meatservprotein)*meatservcals) - 0
            #redefine 
            nonmeatprotein = ((sparecals)/nonmeatservcals)*nonmeatservprotein
            #increase the counter
            counter = counter - 1
        results = f"""
        meatweight: {round(((meatprotein-nonmeatprotein)/meatservprotein) * meatservweight, 2)} oz/grams------\n
        nonmeatweight: {round((nonmeatprotein/nonmeatservprotein) * nonmeatservweight, 2)} oz/grams-------\n
        meatprotein: {round(meatprotein-nonmeatprotein, 2)} grams protein-------\n
        nonmeatprotein: {round(nonmeatprotein, 2)} grams protein---------\n
        meatcals: {round(((meatprotein-nonmeatprotein)/meatservprotein) * meatservcals, 2)} cals-------\n
        nonmeatcals: {round((nonmeatprotein/nonmeatservprotein) * nonmeatservcals, 2)} cals--------\n
        """
        return results

    return render_template("form.html")


if __name__ == "__main__":
    app.run()
