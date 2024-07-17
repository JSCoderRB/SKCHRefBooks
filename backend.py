from flask_mysqldb import MySQL

mysql = MySQL()


def get_all_uploads(cursor):
    try:
        cursor.execute("SELECT * FROM available_books")
        data = cursor.fetchall()
        return data

    except Exception as e:
        print("Problem querying db: " + str(e))
        return None


def get_all_emails(cursor):
    try:
        cursor.execute("SELECT email FROM users")
        data = cursor.fetchall()
        return [val["email"] for val in data]

    except Exception as e:
        print("Problem querying db: " + str(e))
        return None


def get_userid(cursor, em):
    try:
        cursor.execute("SELECT user_id FROM users WHERE email = %s", (em,))
        data = cursor.fetchone()
        return data["user_id"]

    except Exception as e:
        print("Problem querying db: " + str(e))
        return None


def get_passwd(cursor, userid):
    try:
        cursor.execute("SELECT password FROM users WHERE user_id = %s", (userid,))
        data = cursor.fetchone()
        return data["password"]

    except Exception as e:
        print("Problem querying db: " + str(e))
        return None


def add_user(cursor, name, email, password, grade, contact_number, address):
    try:
        details = (
            name,
            email,
            password,
            grade,
            contact_number if contact_number else None,
            address if address else None,
        )

        cursor.execute(
            "INSERT INTO users VALUES(DEFAULT, %s, %s, %s, %s, %s, %s)", details
        )

        mysql.connection.commit()
        return True

    except Exception as e:
        mysql.connection.rollback()
        print("Problem inserting into db: " + str(e))
        return False


# Function to check password validity
def password_check(pwd):
    if not [x for x in pwd if x in "!@#$%^&*()_+={}[]|//><.;\\"]:
        return "Password should contain at least 1 special character"

    if not [x for x in pwd if x.isdigit()]:
        return "Password should contain at least 1 number"

    if not [x for x in pwd if ord(x.lower()) in range(97, 123)]:
        return "Password should contain at least 1 letter"


# Function to check email validity
def email_check(em):
    msg = "Please enter a valid email address"
    if em.count("@") != 1:
        return msg
    else:
        parts = em.split("@")
        name = parts[0]
        domain = parts[1]

        if domain.count(".") != 1:
            return msg
        else:
            subparts = domain.split(".")
            part1 = subparts[0]
            part2 = subparts[1]
            chars = [
                c
                for p in (name, part1, part2)
                for c in p
                if ord(c.lower()) in range(97, 123)
            ]
            if not chars:
                return msg
