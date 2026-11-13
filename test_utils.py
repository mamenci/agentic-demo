import pytest

import utils


@pytest.mark.parametrize("name", [None, "", "   "])
def test_validate_name_rejects(name):
    with pytest.raises(ValueError, match="name is required"):
        utils.validate_name(name)


def test_validate_name_accepts():
    utils.validate_name("Mario")


@pytest.mark.parametrize("email", [None, "", "mx.it"])
def test_validate_email_rejects(email):
    with pytest.raises(ValueError, match="invalid email"):
        utils.validate_email(email)


def test_validate_email_accepts():
    utils.validate_email("m@x.it")


@pytest.mark.parametrize("age", [None, utils.MIN_AGE - 1, utils.MAX_AGE + 1])
def test_validate_age_rejects(age):
    with pytest.raises(ValueError, match="invalid age"):
        utils.validate_age(age)


@pytest.mark.parametrize("age", [utils.MIN_AGE, utils.MAX_AGE])
def test_validate_age_accepts_bounds(age):
    utils.validate_age(age)


def test_format_user():
    user = {"name": "Mario", "email": "m@x.it", "age": 42}
    assert utils.format_user(user) == "Mario <m@x.it> (42)"
