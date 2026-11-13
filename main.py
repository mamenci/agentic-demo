import service
import utils


def run(name, email, age):
    if name is None or name.strip() == "":
        return "error: name is required"
    if email is None or "@" not in email:
        return "error: invalid email"
    if age is None or age < 0 or age > 120:
        return "error: invalid age"
    try:
        user = service.create_user(name, email, age)
    except ValueError as e:
        return "error: " + str(e)
    return utils.format_user(user)


if __name__ == "__main__":
    print(run("Mario Rossi", "mario@example.com", 42))
    print(run("", "mario@example.com", 42))
