MIN_AGE = 0
MAX_AGE = 120


def validate_name(name: str | None) -> None:
    if name is None or name.strip() == "":
        raise ValueError("name is required")


def validate_email(email: str | None) -> None:
    if email is None or "@" not in email:
        raise ValueError("invalid email")


def validate_age(age: int | None) -> None:
    if age is None or age < MIN_AGE or age > MAX_AGE:
        raise ValueError("invalid age")


def format_user(user: dict) -> str:
    return f"{user['name']} <{user['email']}> ({user['age']})"
