from flask import (
    redirect,
    render_template,
    # request,
    url_for,
    session,
    flash,
)
from werkzeug.security import generate_password_hash, check_password_hash
import backend as bk
from forms import LoginForm, SignupForm
import time


# Login route definition
def login():
    form = LoginForm()
    cursor = bk.mysql.connection.cursor()
    uploads = bk.get_all_uploads(cursor)

    # Run the following only if the form details are valid
    if form.validate_on_submit():
        emails = bk.get_all_emails(cursor)

        # Check if the user exists
        if form.email.data not in emails:
            flash("Invalid username", "error")
            return redirect(url_for("login"))

        # Retrieve user's ID from the database
        user_id = bk.get_userid(cursor, form.email.data)

        # Check if password is correct
        passwd = bk.get_passwd(cursor, user_id)

        if not check_password_hash(passwd, form.password.data):
            flash("Invalid password", "error")
            return redirect(url_for("login"))

        # Store the user's id in session
        session["user_id"] = user_id
        cursor.close()

        # Redirect to the user dashboard
        return "Success!"

    return render_template("login.html", form=form, uploads=uploads)


# Sign Up route definition
def signup():
    form = SignupForm()

    # Run the following only if the form details are valid
    if form.validate_on_submit():
        cursor = bk.mysql.connection.cursor()
        emails = bk.get_all_emails(cursor)

        # Check if username already exists
        if form.email.data in emails:
            # TODO: change to `info` category, add styling for that as well
            flash("Username exists, login from the Login Page...", "success")
            time.sleep(3)
            return render_template("redirect.html", redirect_url="/")

        # Update the new user in the database
        added = bk.add_user(
            cursor,
            form.name.data,
            form.email.data,
            generate_password_hash(form.password.data, salt_length=4),
            form.grade.data,
            form.contact_number.data,
            form.address.data,
        )

        # Close the cursor
        cursor.close()

        # Show a message and redirect
        if added:
            flash("Signup successful! Redirecting to login page...", "success")
            time.sleep(3)
            return render_template("redirect.html", redirect_url="/")
        else:
            flash("Problem inserting into db, please try again...", "error")
            time.sleep(3)
            return render_template("redirect.html", redirect_url="/signup")

    return render_template("signup.html", form=form)


# Log out route definition
def logout():
    session.pop("user_id", None)  # to clear the session data
    return redirect("/")


# TODO: change completely to SQL
# Dashboard route definition
def dashboard():
    cursor = bk.mysql.connection.cursor()
    uploads = bk.get_all_uploads(cursor)
    # df = app.config["uploads_df"]
    # uploads = df.to_dict(orient="records")

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
