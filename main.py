# Imports
from flask import Flask, render_template, request, redirect, url_for, flash, session
from forms import LoginForm, SignupForm
import pandas as pd
import os
import time
import backend as bk


# Initializing a Flask object for our app
app = Flask(__name__, template_folder="html")


# Login route definition
@app.route("/", methods=["POST", "GET"])
def login():
    df = app.config["users_df"]
    uploads = app.config["uploads_df"].to_dict(orient="records")
    emails = df.get("email").tolist()
    form = LoginForm()

    # Run the following only if the form details are valid
    if form.validate_on_submit():
        # Check if the user exists
        if form.email.data not in emails:
            flash("Invalid username", "error")
            return redirect(url_for("login"))

        # Retrieve user's data from the dataframe
        userdata = bk.get_userdata(df, form.email.data)

        # Check if password is correct
        if form.password.data != userdata["password"]:
            flash("Invalid password", "error")
            return redirect(url_for("login"))

        # Store the details in session
        session["details"] = userdata

        # Redirect to the user dashboard
        return redirect(url_for("dashboard"))

    return render_template("login.html", form=form, uploads=uploads)


# Sign Up route definition
@app.route("/signup", methods=["GET", "POST"])
def signup():
    emails = app.config["users_df"].get("email").tolist()
    form = SignupForm()

    # Run the following only if the form details are valid
    if form.validate_on_submit():
        # Retrieve all the signup form data
        email = request.form["email"]
        name = request.form["name"]
        grade = request.form["grade"]
        contact_number = request.form["contact_number"]
        address = request.form["address"] if "address" in request.form else None
        password = request.form["password"]

        # Check if username already exists
        if email in emails:
            flash("Username exists, login from the Login Page...", "success")
            time.sleep(3)
            return render_template("redirect.html", redirect_url="/")

        # Structure the user's details
        userDetails = [
            email,
            password,
            name,
            grade,
            contact_number,
            address,
        ]

        fields = ["email", "password", "name", "grade", "contact_number", "address"]

        # Update the new user as a row in the dataframe
        app.config["users_df"] = bk.insert_row(
            app.config["users_df"], userDetails, fields
        )

        # Write the dataframe to csv file
        app.config["users_df"].to_csv(app.config["users_file"], index=False)

        # Show a message and redirect to login page
        flash("Signup successful! Redirecting to login page...", "success")
        time.sleep(3)
        return render_template("redirect.html", redirect_url="/")

    return render_template("signup.html", form=form)


# Dashboard route definition
@app.route("/dashboard")
def dashboard():
    df = app.config["uploads_df"]
    uploads = df.to_dict(orient="records")

    # Variable for current book request
    my_request = [u for u in uploads if u["requester"] == session["details"]["name"]]

    # Retrieving all uploads of the user
    mask = df["uploader"].values == session["details"]["name"]
    filtered_uploads = df.loc[mask].to_dict(orient="records")

    # Variable for all books uploaded by user
    my_uploads = [u["book_name"] for u in filtered_uploads]

    # Variable for all books requested from the user
    requested_uploads = [
        (u["book_name"], u["requester"])
        for u in filtered_uploads
        if not pd.isna(u["requester"])
    ]

    # Status message generation for uploads
    uploads_stat = ""
    for book in requested_uploads:
        uploads_stat += f"{book[0]} has been requested by {book[1]}\n"

    # Status message generation for request
    if my_request:
        curr_request = f'{my_request[0]["book_name"]} from {my_request[0]["uploader"]}'
        request_stat = (
            "A message has been sent to the uploader. Waiting for a response."
        )
    else:
        curr_request = "N/A"
        request_stat = "N/A"

    # Render the dashboard with all the arguments
    if "details" in session:
        return render_template(
            "dashboard.html",
            name=session["details"]["name"],
            email=session["details"]["email"],
            grade=session["details"]["grade"],
            curr_request=curr_request,
            request_stat=request_stat,
            uploads=uploads,
            my_uploads=(", ".join(my_uploads) if my_uploads else "N/A"),
            uploads_stat=(uploads_stat if uploads_stat else "N/A"),
            length=len(uploads),
        )


# Book request app route
@app.route("/book_request", methods=["GET", "POST"])
def book_request():
    if request.method == "POST":
        uploads = app.config["uploads_df"].to_dict(orient="records")

        # Gets the index of book requested
        index = int(request.form["request_button"])

        # Check if the user has already requested a book or not
        check = not [u for u in uploads if u["requester"] == session["details"]["name"]]

        # Send the request only if the user hasn't requested a book already
        if pd.isna(uploads[index]["requester"]) and check:
            app.config["uploads_df"].loc[index, ["requester"]] = session["details"][
                "name"
            ]
            app.config["uploads_df"].to_csv(app.config["uploads_file"], index=False)

            # Redirect to the dashboard with a message
            flash("Request successful! Verify its status in your profile...", "success")
            time.sleep(3)
            return render_template("redirect.html", redirect_url="/dashboard")

        return redirect(url_for("dashboard"))


# Log out route definition
@app.route("/logout")
def logout():
    session.pop("details", None)  # to clear the session data
    return redirect("/")


# Main
if __name__ == "__main__":
    users_file = "./csv/users.csv"
    uploads_file = "./csv/uploads.csv"
    flag = os.path.exists(users_file) and os.path.exists(uploads_file)

    # Blueprint for users_df
    users_skeleton = {
        "email": [],
        "password": [],
        "name": [],
        "grade": [],
        "contact_number": [],
        "address": [],
    }

    # Blueprint for uploads_df
    uploads_skeleton = {
        "book_name": [],
        "author": [],
        "version": [],
        "uploader": [],
        "requester": [],
    }

    # Create or populate the dataframes, depending on csv files existing or not
    if flag:
        users_df = pd.read_csv(users_file)
        uploads_df = pd.read_csv(uploads_file)
    else:
        users_df = pd.DataFrame(users_skeleton)
        uploads_df = pd.DataFrame(uploads_skeleton)

    # Set all app configuration variables
    app.config["users_df"] = users_df
    app.config["uploads_df"] = uploads_df
    app.config["users_file"] = users_file
    app.config["uploads_file"] = uploads_file

    # Setting a secret key to ensure that session data is not breached
    app.secret_key = "86e269cbc87458e8c624876e5f055fb7e37d42b7498c0b9db0ad168fa7942836"

    # Run the app
    app.run(debug=True)
