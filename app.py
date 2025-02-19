from re import L
from sre_constants import SUCCESS
from flask import Flask, render_template, request, url_for, redirect, flash
import sqlite3


app = Flask(__name__)
db_locale = 'ratings.db'

# url


@app.route('/')
# home page
@app.route('/ratings')
def home_page():
    # call query_ramen_details
    rating_data = query_ramen_details()

    # call filter list
    country_list = filter()

    # render data to home.html

    return render_template('home.html', rating_data=rating_data, country_list=country_list)

# query all data from rating.db's ramen-rating table


def query_ramen_details():
    connie = sqlite3.connect(db_locale)
    c = connie.cursor()
    # this function calls queries all record from the ramen-ratings table
    c.execute("""
    SELECT * FROM `ramen-ratings`
     """)
    rating_data = c.fetchall()
    return rating_data  # return instead of print to pass to example_text variable


# search for type of ramen by partial text function
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "GET":
        # request user input
        name = request.args.get('Type')
        connie = sqlite3.connect(db_locale)
        c = connie.cursor()
        result_data = c.execute(
            "SELECT * FROM `ramen-ratings` WHERE Type LIKE ? ", ('%' + name + '%',)).fetchall()
        print(result_data)
        flash('search success!')
        return render_template('result.html', result_data=result_data)
       # return result_data #return instead of print to pass to example_text variable
    else:
        return redirect(url_for('home_page'))
       # return result_data #return instead of print to pass to example_text variable


# adding review function
@app.route('/add', methods=['GET', 'POST'])
def add():
    # returns adding review html user form (create.html)
    if request.method == 'GET':
        return render_template('create.html')
    else:
        # POST REQUEST
        # user keys in details to the user form
        rating_details = (
            request.form["Country"],
            request.form["Brand"],
            request.form["Type"],
            request.form["Package"],
            request.form["Rating"]
        )
    # call add_rating function, the details the user keys in will pass to this function
        add_rating(rating_details)
        flash("Successfully added review!")
        return redirect(url_for('home_page'))

# captures user form in add() function into the sql code


def add_rating(rating_details):
    connie = sqlite3.connect(db_locale)
    c = connie.cursor()
    sql = "INSERT INTO `ramen-ratings`( Country, Brand, Type, Package, Rating) VALUES(?, ?, ?, ?, ?)"
    c.execute(sql, rating_details)
    connie.commit()
    connie.close()


# update review function
@app.route("/update/<string:id>", methods=["POST", "GET"])
def update(id):
    connie = sqlite3.connect(db_locale)
    c = connie.cursor()

    # if user updates
    if request.method == "POST":
        update_id = id
        # request user input from html user form in update.html
        new_country = request.form["new_country"]
        new_brand = request.form["new_brand"]
        new_type = request.form["new_type"]
        new_package = request.form["new_package"]
        new_rating = request.form["new_rating"]
        c.execute("UPDATE `ramen-ratings` SET Country = ?, Brand = ?, Type = ?, Package = ?, Rating = ? WHERE ID = ? ",
                  (new_country, new_brand, new_type, new_package, new_rating, update_id))
        connie.commit()
        flash('Review updated!', 'success')
        return redirect(url_for("home_page"))
    # get updated rating detials based on the rating that the user have just updated
    c.execute("SELECT * from `ramen-ratings` WHERE ID = ?", (id,))
    data = c.fetchone()
    return render_template("update.html", data=data)


# delete reivew function
@app.route("/delete/<id>")
def delete(id):
    connie = sqlite3.connect(db_locale)
    c = connie.cursor()
    c.execute("DELETE FROM `ramen-ratings` WHERE ID = '{}'".format(id))
    connie.commit()
    connie.close()
    flash('Review deleted!', 'success')
    # once record has been deleted, the user will be directed or stay in the home.html which is the home page
    return redirect(url_for("home_page"))

# country filter list function


def filter():
    connie = sqlite3.connect(db_locale)
    c = connie.cursor()
    c.execute(
        "SELECT DISTINCT Country FROM `ramen-ratings`")
    country_list = c.fetchall()
    return country_list  # return country_list data


@app.route('/filter', methods=['POST', 'GET'])
def filter_country():
    # request user input
    Country = request.form.get('Country')
    connie = sqlite3.connect(db_locale)
    c = connie.cursor()
    filter_data = c.execute(
        "SELECT * FROM `ramen-ratings` WHERE Country LIKE ? ", ( Country,)).fetchall()
    print(filter_data)
    flash('filter success!')
    return render_template('filter_result.html', filter_data=filter_data)


# run the website
if __name__ == '__main__':
    app.secret_key = 'admin123'
    app.run(debug=True)
