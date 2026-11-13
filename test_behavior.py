import pytest

import main
import service


@pytest.fixture(autouse=True)
def clean():
    service.users.clear()


def test_run_ok():
    assert main.run(" Mario ", "m@x.it", 42) == "Mario <m@x.it> (42)"


@pytest.mark.parametrize(
    "args,msg",
    [
        (("", "m@x.it", 1), "error: name is required"),
        ((None, "m@x.it", 1), "error: name is required"),
        (("A", "nomail", 1), "error: invalid email"),
        (("A", None, 1), "error: invalid email"),
        (("A", "m@x.it", -1), "error: invalid age"),
        (("A", "m@x.it", 121), "error: invalid age"),
        (("A", "m@x.it", None), "error: invalid age"),
    ],
)
def test_run_validation(args, msg):
    assert main.run(*args) == msg


def test_create_user_validation():
    with pytest.raises(ValueError, match="invalid email"):
        service.create_user("A", "x", 1)
    with pytest.raises(ValueError, match="name is required"):
        service.create_user(" ", "a@b.it", 1)
    with pytest.raises(ValueError, match="invalid age"):
        service.create_user("A", "a@b.it", 200)


def test_update_user():
    service.create_user("A", "a@b.it", 1)
    assert service.update_user("a@b.it", " B ", 5)["name"] == "B"
    with pytest.raises(KeyError):
        service.update_user("zz@b.it", "B", 5)
    with pytest.raises(ValueError, match="name is required"):
        service.update_user("a@b.it", "", 5)
    with pytest.raises(ValueError, match="invalid age"):
        service.update_user("a@b.it", "B", -3)
