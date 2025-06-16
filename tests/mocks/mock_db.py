from unittest.mock import MagicMock


class MockDBManager:
    def __init__(self):
        self.users = []

    def create_and_populate_db(self):
        return []

    def add_user(self, *args, **kwargs):
        self.users.append(args)
        return self.users

    def load_db(self):
        return self.users

    def validate_user(self, user):
        return []
