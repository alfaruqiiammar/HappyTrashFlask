import json
from tests import app, client, cache, resetDatabase
from apps.users.model import Users


class TestUserFunctions():
    """Class for tests functions in user's model"""

    resetDatabase()

    def testUserEmailValid(self):
        """Test wether isEmailAdressValid function working correctly"""

        assert Users.isEmailAddressValid(self, 'happy@trash') == False
        assert Users.isEmailAddressValid(self, 'happy@trash.com') == True

    def testUserNumberValid(self):
        """Test wether isMobileNumberValid function working correctly"""

        assert Users.isMobileNumberValid(self, "876542372864") == False
        assert Users.isMobileNumberValid(self, "0876542372864") == True
        assert Users.isMobileNumberValid(self, "064") == False

    def testIsEmailExist(self):
        """Test wether isEmailExist function working correctly"""

        assert Users.isEmailExist("admin@admin.com") == True
        assert Users.isEmailExist("foo@bar.com") == False

    def testIsNumberExist(self):
        """Test wether isMobileNumberExist function working correctly"""

        assert Users.isMobileNumberExist("0812345678") == False
        assert Users.isMobileNumberExist("0811221122112") == True
