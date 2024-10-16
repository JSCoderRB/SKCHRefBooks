from flask_mysqldb import MySQL

mysql = MySQL()


def get_all_uploads(cursor):
    try:
        query = "SELECT book_id, book_name, author, version, filename, uploader_id, requester_id, user_name FROM books b JOIN users u ON u.user_id = b.uploader_id WHERE status = 'Available'"

        cursor.execute(query)
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


def get_my_request(cursor, uid):
    try:
        query = "SELECT book_id, book_name, author, version, filename, uploader_id, requester_id, user_name, status FROM books b JOIN users u ON u.user_id = b.uploader_id WHERE requester_id = %s"
        cursor.execute(query, (uid,))
        data = cursor.fetchone()
        return data
    except Exception as e:
        print("Problem querying db: " + str(e))
        return None


def get_my_uploads(cursor, uid):
    try:
        cursor.execute("SELECT * FROM books WHERE uploader_id = %s", (uid,))
        data = cursor.fetchall()
        return data
    except Exception as e:
        print("Problem querying db: " + str(e))
        return None


def get_requested_uploads(cursor, uid):
    try:
        query = "SELECT book_id, book_name, author, version, filename, uploader_id, requester_id, user_name, status FROM books b JOIN users u ON u.user_id = b.requester_id WHERE uploader_id = %s"
        cursor.execute(query, (uid,))
        data = cursor.fetchall()
        return data
    except Exception as e:
        print("Problem querying db: " + str(e))
        return None


def get_my_details(cursor, uid):
    try:
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (uid,))
        data = cursor.fetchone()
        return data
    except Exception as e:
        print("Problem querying db: " + str(e))
        return None


def get_upl_details(cursor, bid):
    try:
        query = "SELECT uploader_id, user_name, email, contact_number, address FROM users u JOIN books b ON u.user_id = b.uploader_id WHERE book_id = %s"
        cursor.execute(query, (bid,))
        data = cursor.fetchone()
        return data
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
            "INSERT INTO users VALUES(DEFAULT, %s, %s, %s, %s, %s, %s)",
            details,
        )

        mysql.connection.commit()
        return True

    except Exception as e:
        mysql.connection.rollback()
        print("Problem inserting into db: " + str(e))
        return False


def change_details(cursor, uid, name, email, password, grade, contact_number, address):
    try:
        details = (
            name,
            email,
            password,
            grade,
            contact_number if contact_number else None,
            address if address else None,
            uid,
        )

        cursor.execute(
            "UPDATE users SET user_name = %s, email = %s, password = %s, grade = %s, contact_number = %s, address = %s WHERE user_id = %s",
            details,
        )

        mysql.connection.commit()
        return True

    except Exception as e:
        mysql.connection.rollback()
        print("Problem inserting into db: " + str(e))
        return False


def request_book(cursor, uid, bid):
    try:
        cursor.execute(
            "UPDATE books SET requester_id = %s, status = 'Requested' WHERE book_id = %s",
            (uid, bid),
        )
        mysql.connection.commit()
        return True

    except Exception as e:
        mysql.connection.rollback()
        print("Problem inserting into db: " + str(e))
        return False


def upload_book(cursor, bname, author, version, fname, upid):
    try:
        details = (
            bname,
            author if author else None,
            version if version else None,
            fname if fname else "Default",
            upid,
            None,
        )

        cursor.execute(
            "INSERT INTO books VALUES(DEFAULT, %s, %s, %s, %s, %s, %s, DEFAULT)",
            details,
        )

        mysql.connection.commit()
        return True

    except Exception as e:
        mysql.connection.rollback()
        print("Problem inserting into db: " + str(e))
        return False


def delete_book(cursor, bid):
    try:
        cursor.execute("DELETE FROM books WHERE book_id = %s", (bid,))
        mysql.connection.commit()
        return True

    except Exception as e:
        mysql.connection.rollback()
        print("Problem inserting into db: " + str(e))
        return False


def give_book(cursor, bid):
    try:
        cursor.execute(
            "UPDATE books SET status = 'Accepted' WHERE book_id = %s", (bid,)
        )
        mysql.connection.commit()
        return True

    except Exception as e:
        mysql.connection.rollback()
        print("Problem inserting into db: " + str(e))
        return False


def request_cancel(cursor, bid):
    try:
        cursor.execute(
            "UPDATE books SET requester_id = NULL, status = 'Available' WHERE book_id = %s",
            (bid,),
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
