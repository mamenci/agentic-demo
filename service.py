import utils

users = {}


def create_user(name, email, age):
    utils.validate_name(name)
    utils.validate_email(email)
    utils.validate_age(age)
    users[email] = {"name": name.strip(), "email": email, "age": age}
    return users[email]


def update_user(email, name, age):
    if email not in users:
        raise KeyError("user not found")
    utils.validate_name(name)
    utils.validate_age(age)
    users[email]["name"] = name.strip()
    users[email]["age"] = age
    return users[email]
