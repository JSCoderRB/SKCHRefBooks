import backend as bk
from flask_wtf import FlaskForm
from wtforms import (
    IntegerField,
    StringField,
    PasswordField,
    validators,
)


# Custom email validator function
def valid_email(form, field):
    msg = bk.email_check(field.data)
    if msg:
        raise validators.ValidationError(message=msg)


# Custom password validator function
def valid_password(form, field):
    msg = bk.password_check(field.data)
    if msg:
        raise validators.ValidationError(message=msg)


# Defining the Login Form and its fields
class LoginForm(FlaskForm):
    email = StringField("Email", [validators.DataRequired()])
    password = PasswordField("Password", [validators.DataRequired()])


# Defining the Signup Form and its fields
class SignupForm(FlaskForm):
    email = StringField(
        "Email",
        [
            validators.DataRequired(),
            valid_email,
        ],
    )

    name = StringField("Name", [validators.DataRequired()])

    grade = IntegerField(
        "Grade",
        [
            validators.DataRequired(),
            validators.NumberRange(
                min=1, max=12, message="Please enter a grade between 1 and 12"
            ),
        ],
    )

    contact_number = StringField(
        "Contact Number",
        [
            validators.DataRequired(),
            validators.Length(max=10, message="Please enter a valid contact number"),
            validators.Regexp(
                r"^\+?[0-9]+$", message="Please enter a valid contact number"
            ),
        ],
    )

    address = StringField("Address", [validators.Optional()])

    password = PasswordField(
        "Password",
        [
            validators.DataRequired(),
            validators.Length(
                min=8, message="Password should contain at least 8 characters"
            ),
            valid_password,
        ],
    )

    password_confirmation = PasswordField(
        "Confirm Password",
        [
            validators.DataRequired(),
            validators.EqualTo("password", message="Passwords must match"),
        ],
    )
