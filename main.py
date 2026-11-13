import service
import utils


def run(name, email, age):
    try:
        user = service.create_user(name, email, age)
    except ValueError as e:
        return "error: " + str(e)
    return utils.format_user(user)


if __name__ == "__main__":
    print(run("Mario Rossi", "mario@example.com", 42))
    print(run("", "mario@example.com", 42))
