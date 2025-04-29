import pytest

from evengsdk.exceptions import EvengHTTPError

USERS = {
    "users": [("user", "passwd")],
    "to_create": [
        ("test_user", "passwd"),
        ("test_user1", "passwd"),
    ],
    "non_existing": "fake_user99",
}


class TestEvengApiUser:
    def test_list_users(self, authenticated_client):
        """
        Verify that we can retrieve list of users and that
        the default 'admin' user  exists.
        """
        r = authenticated_client.api.list_users()
        assert "admin" in r["data"]

    def test_list_user_roles(self, authenticated_client):
        """
        Verify that we can retrieve list of user roles
        """
        r = authenticated_client.api.list_user_roles()
        assert "admin" in r["data"]

    def test_get_user(self, authenticated_client):
        """
        Verify that we can retrieve a single user detail
        """
        r = authenticated_client.api.get_user("admin")
        assert "email" in r["data"]

    def test_get_non_existing_user(self, authenticated_client):
        """
        Verify that the api returns an empty dictionary
        if the user does not exist
        """
        with pytest.raises(EvengHTTPError):
            user = USERS["non_existing"]
            authenticated_client.api.get_user(user)

    @pytest.mark.xfail
    def test_add_user(self, authenticated_client):
        """
        Verify that we can created a user with just
        the username and password
        """
        for username, password in iter(USERS["to_create"]):
            user_data = {
                "username": username,
                "password": password,
                "name": "Test User",
                "email": f"{username}@example.com",
                "expiration": "-1",
            }

            try:
                r = authenticated_client.api.add_user(**user_data)
                assert r["status"] == "success"
            except EvengHTTPError as e:
                msg = str(e).lower()

                if "Cannot create user, check if already exists" in msg:
                    assert True
                elif "database error" in msg:
                    pytest.fail(
                        f"Database error occurred while adding user '{username}': {msg}. Payload: {user_data}"
                    )
                else:
                    pytest.fail(
                        f"Unexpected error while adding user '{username}': {msg}. Payload: {user_data}"
                    )

    def test_add_existing_user(self, authenticated_client):
        """
        Verify that adding an existing user raises
        an exception
        """
        for username, password in iter(USERS["to_create"]):
            with pytest.raises(EvengHTTPError):
                authenticated_client.api.add_user(username, password)

    def test_edit_existing_user(self, authenticated_client):
        username, password = USERS["to_create"][1]
        try:
            try:
                user_data = authenticated_client.api.get_user(username)
            except EvengHTTPError:
                authenticated_client.api.add_user(username, password)
                user_data = authenticated_client.api.get_user(username)

            full_data = user_data.get("data", {})
            full_data["email"] = "testuser1@testing.com"
            full_data["name"] = "John Doe"

            authenticated_client.api.edit_user(username, data=full_data)

        except EvengHTTPError as e:
            pytest.fail(f"Edit failed for user '{username}': {e}")

    def test_edit_non_existing_user(self, authenticated_client):
        """
        Verify that editing non existing users raises
        an exception.
        """
        with pytest.raises(EvengHTTPError):
            new_data = {"email": "test@testing.com", "name": "John Doe"}
            username = USERS["non_existing"]
            authenticated_client.api.edit_user(username, data=new_data)

    def test_edit_user_w_missing_data_raises(self, authenticated_client):
        """Editing a using without missing data should raise
        a ValueError.
        """
        with pytest.raises(ValueError):
            authenticated_client.api.edit_user("test_user", data={})

    def test_delete_user(self, authenticated_client):
        """
        Verify that we can delete users
        """
        for username, _ in iter(USERS["to_create"]):
            r = authenticated_client.api.delete_user(username)
            assert r["status"] == "success"

            # make sure it was deleted
            with pytest.raises(EvengHTTPError):
                authenticated_client.api.get_user(username)
