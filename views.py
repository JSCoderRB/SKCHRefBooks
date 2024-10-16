from flask import (
    redirect,
    render_template,
    request,
    url_for,
    session,
    flash,
    current_app,
)
from werkzeug.security import generate_password_hash, check_password_hash
import backend as bk
from forms import LoginForm, SignupForm, UploadForm, EditProfileForm
import time
import os


# Landing route definition
def index():
    cursor = bk.mysql.connection.cursor()
    uploads = bk.get_all_uploads(cursor)
    return render_template("landing.html", uploads=uploads)


# Login route definition
def login():
    form = LoginForm()
    cursor = bk.mysql.connection.cursor()

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
        return redirect(url_for("dashboard"))

    return render_template("login.html", form=form)


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
            return render_template("redirect.html", redirect_url="/login")
        else:
            flash("Problem inserting into db, please try again...", "error")
            time.sleep(3)
            return render_template("redirect.html", redirect_url="/signup")

    return render_template("signup.html", form=form)


def edit_profile():
    form = EditProfileForm()
    cursor = bk.mysql.connection.cursor()

    # Run the following only if the form details are valid
    if form.validate_on_submit():

        # Update the user's details in the database
        changed = bk.change_details(
            cursor,
            session["user_id"],
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
        if changed:
            flash("Profile change successful!", "success")
            time.sleep(3)
            return render_template("redirect.html", redirect_url="/dashboard")
        else:
            flash("Problem inserting into db, please try again...", "error")
            time.sleep(3)
            return render_template("redirect.html", redirect_url="/signup")

    elif request.method == "GET":
        details = bk.get_my_details(cursor, session["user_id"])
        cursor.close()

        form.name.data = details["user_name"]
        form.email.data = details["email"]
        form.grade.data = details["grade"]
        form.contact_number.data = details["contact_number"]
        form.address.data = details["address"]

    return render_template("edit_profile.html", form=form)


# Log out route definition
def logout():
    session.pop("user_id", None)  # to clear the session data
    return redirect("/")


# Dashboard route definition
def dashboard():
    cursor = bk.mysql.connection.cursor()
    uploads = [
        upload
        for upload in bk.get_all_uploads(cursor)
        if upload["uploader_id"] != session["user_id"]
    ]
    details = bk.get_my_details(cursor, session["user_id"])
    my_details = [details["user_name"], details["email"], details["grade"]]

    # Variable for current book request
    my_request = bk.get_my_request(cursor, session["user_id"])

    # Variable for all books uploaded by user
    my_uploads = bk.get_my_uploads(cursor, session["user_id"])

    # Variable for all books requested from the user
    requested_uploads = bk.get_requested_uploads(cursor, session["user_id"])

    # Notification generation for requested uploads
    accepted_notif = [
        f"Your details have been shared with {upload['user_name']} for {upload['book_name']}"
        for upload in requested_uploads
        if upload["status"] == "Accepted"
    ]

    # Status message generation for request
    if my_request:
        request_stat = my_request["status"]
        if request_stat == "Requested":
            req_details = [
                "A message has been sent to the uploader. Waiting for a response.",
            ]
        elif request_stat == "Accepted":
            uploader = bk.get_upl_details(cursor, my_request["book_id"])

            req_details = [
                f"{uploader['user_name']} has accepted your request!",
                "Contact details:",
                f"Email : {uploader['email']}",
                f"Contact Number : {uploader['contact_number']}",
                f"Address : {uploader['address']}",
            ]
    else:
        req_details = ("N/A",)

    # Render the dashboard with all the arguments
    if "user_id" in session:
        return render_template(
            "dashboard.html",
            my_details=my_details,
            req_details=req_details,
            uploads=uploads,
            my_uploads=my_uploads,
            requested_uploads=requested_uploads,
            my_request=my_request,
            accepted_notif=accepted_notif,
        )


def book_request():
    if request.method == "POST":
        cursor = bk.mysql.connection.cursor()

        # Gets the id of book requested
        book_id = request.form["request_button"]

        # Check if the user has already requested a book or not
        check_user = bk.get_my_request(cursor, session["user_id"])

        # Send the request only if the user hasn't requested a book already
        if check_user:
            flash("You have already requested a book!", "error")
            return render_template("redirect.html", redirect_url="/dashboard")
        else:
            requested = bk.request_book(cursor, session["user_id"], book_id)
            cursor.close()

            # Redirect to the dashboard with a message
            if requested:
                flash(
                    "Request successful! Verify its status in your profile...",
                    "success",
                )
                time.sleep(3)
                return render_template("redirect.html", redirect_url="/dashboard")
            else:
                flash("Problem inserting into db, please try again...", "error")
                time.sleep(3)
                return render_template("redirect.html", redirect_url="/dashboard")

    return redirect(url_for("dashboard"))


def upload():
    form = UploadForm()
    if form.validate_on_submit():
        cursor = bk.mysql.connection.cursor()

        if "file" not in request.files:
            flash("No file part", "error")
            return redirect(url_for("upload"))

        cover = request.files["file"]

        if cover.filename == "":
            flash("No selected file", "error")
            return redirect(url_for("upload"))

        if cover:
            base_filename = f"{form.book_name.data.replace(' ', '_')}_{form.version.data}_{session['user_id']}"
            filename = f"{base_filename}{os.path.splitext(cover.filename)[1]}"
            filepath = os.path.join(current_app.config["UPLOADS_FOLDER"], filename)
            cover.save(filepath)

            # Insert the new book in the database
            uploaded = bk.upload_book(
                cursor,
                form.book_name.data,
                form.author.data,
                form.version.data,
                filename,
                session["user_id"],
            )

            # Close the cursor
            cursor.close()

            # Show a message and redirect
            if uploaded:
                flash("Uploaded successfully! Redirecting to dashboard...", "success")
                time.sleep(3)
                return render_template("redirect.html", redirect_url="/dashboard")
            else:
                flash("Problem inserting into db, please try again...", "error")
                time.sleep(3)
                return render_template("redirect.html", redirect_url="/upload")

    return render_template("upload.html", form=form)


def delete_upload():
    if request.method == "POST":
        cursor = bk.mysql.connection.cursor()

        # Gets the id of book involved
        book_id = request.form["remove_button"]
        deleted = bk.delete_book(cursor, book_id)

        cursor.close()

        if deleted:
            flash("Book deleted successfully!", "success")
            time.sleep(3)
            return render_template("redirect.html", redirect_url="/dashboard")
        else:
            flash("Problem deleting from db, try again!", "error")
            time.sleep(3)
            return render_template("redirect.html", redirect_url="/dashboard")

    return redirect(url_for("dashboard"))


def accept_request():
    if request.method == "POST":
        cursor = bk.mysql.connection.cursor()

        # Gets the id of book involved
        book_id = request.form["give_button"]
        accepted = bk.give_book(cursor, book_id)

        cursor.close()

        if accepted:
            flash("Sucess! Check your sidebar for more information...", "success")
            time.sleep(3)
            return render_template("redirect.html", redirect_url="/dashboard")
        else:
            flash("Problem inserting in db, try again!", "error")
            time.sleep(3)
            return render_template("redirect.html", redirect_url="/dashboard")

    return redirect(url_for("dashboard"))


def confirm_request():
    if request.method == "POST":
        cursor = bk.mysql.connection.cursor()

        # Gets the id of book involved
        book_id = request.form["confirmRequest"]
        confirmed = bk.delete_book(cursor, book_id)

        cursor.close()

        if confirmed:
            flash("Exchange successful!", "success")
            time.sleep(3)
            return render_template("redirect.html", redirect_url="/dashboard")
        else:
            flash("Problem deleting from db, try again!", "error")
            time.sleep(3)
            return render_template("redirect.html", redirect_url="/dashboard")

    return redirect(url_for("dashboard"))


def cancel_request():
    if request.method == "POST":
        cursor = bk.mysql.connection.cursor()

        # Gets the id of book involved
        book_id = request.form["cancelRequest"]
        cancelled = bk.request_cancel(cursor, book_id)

        cursor.close()

        if cancelled:
            flash("Request cancelled successfully!", "success")
            time.sleep(3)
            return render_template("redirect.html", redirect_url="/dashboard")
        else:
            flash("Problem inserting in db, try again!", "error")
            time.sleep(3)
            return render_template("redirect.html", redirect_url="/dashboard")

    return redirect(url_for("dashboard"))
