import json
from tests import app, client, cache, resetDatabase
from apps.users.model import Users


class TestUserFunctions():
    resetDatabase()

    def testUserEmailValid(self):
        assert Users.isEmailAddressValid('happy@trash') == False
        assert Users.isEmailAddressValid('happy@trash.com') == True
