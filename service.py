users = {}


def create_user(name, email, age):
    if name is None or name.strip() == "":
        raise ValueError("name is required")
    if email is None or "@" not in email:
        raise ValueError("invalid email")
    if age is None or age < 0 or age > 120:
        raise ValueError("invalid age")
    users[email] = {"name": name.strip(), "email": email, "age": age}
    return users[email]


def update_user(email, name, age):
    if email not in users:
        raise KeyError("user not found")
    if name is None or name.strip() == "":
        raise ValueError("name is required")
    if age is None or age < 0 or age > 120:
        raise ValueError("invalid age")
    users[email]["name"] = name.strip()
    users[email]["age"] = age
    return users[email]
