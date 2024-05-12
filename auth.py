from flask import (
    current_app,
    redirect,
    render_template,
    request,
    url_for,
    session,
    flash,
    Blueprint,
)
from forms import LoginForm, SignupForm
import backend as bk
import time

auth_bp = Blueprint("auth", __name__)


# Login route definition
@auth_bp.route("/", methods=["POST", "GET"])
def login():
    df = current_app.config["users_df"]
    uploads = current_app.config["uploads_df"].to_dict(orient="records")
    emails = df.get("email").tolist()
    form = LoginForm()

    # Run the following only if the form details are valid
    if form.validate_on_submit():
        # Check if the user exists
        if form.email.data not in emails:
            flash("Invalid username", "error")
            return redirect(url_for("auth.login"))

        # Retrieve user's data from the dataframe
        userdata = bk.get_userdata(df, form.email.data)

        # Check if password is correct
        if form.password.data != userdata["password"]:
            flash("Invalid password", "error")
            return redirect(url_for("auth.login"))

        # Store the details in session
        session["details"] = userdata

        # Redirect to the user dashboard
        return redirect(url_for("dashboard"))

    return render_template("login.html", form=form, uploads=uploads)


# Sign Up route definition
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    emails = current_app.config["users_df"].get("email").tolist()
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
        current_app.config["users_df"] = bk.insert_row(
            current_app.config["users_df"], userDetails, fields
        )

        # Write the dataframe to csv file
        current_app.config["users_df"].to_csv(
            current_app.config["users_file"], index=False
        )

        # Show a message and redirect to login page
        flash("Signup successful! Redirecting to login page...", "success")
        time.sleep(3)
        return render_template("redirect.html", redirect_url="/")

    return render_template("signup.html", form=form)


# Log out route definition
@auth_bp.route("/logout")
def logout():
    session.pop("details", None)  # to clear the session data
    return redirect("/")
