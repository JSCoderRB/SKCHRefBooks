import pandas as pd


# Function retrieve user details
def get_userdata(df, email):
    mask = df["email"].values == email
    filtered_dict = df.loc[mask].to_dict(orient="records")[0]
    return filtered_dict


# Function to insert a row into one of our dataframes
def insert_row(df, details, fields):
    new_row = {}

    for index, field in enumerate(fields):
        new_row[field] = [details[index]]

    df = pd.concat([pd.DataFrame(new_row), df])
    return df


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
