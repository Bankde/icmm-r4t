import pytest
import os
import sys
import inspect
CURRENT_DIR = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
# Include paths for module search
sys.path.insert(0, PARENT_DIR)

from db import UserDB

DEFAULT_TEST_DB = os.path.join(PARENT_DIR, "test.users.db")

@pytest.fixture(scope="session")
def users():
    users = {}
    users["1"] = {"firstname": "A", "lastname": "A", "teamName": "", "first10k": "1"}
    users["2"] = {"firstname": "B", "lastname": "B", "teamName": "", "first10k": "1"}
    users["3"] = {"firstname": "C", "lastname": "C", "teamName": "", "first10k": "0"}
    users["4"] = {"firstname": "D", "lastname": "D", "teamName": "", "first10k": "0"}
    users["5"] = {"firstname": "E", "lastname": "E", "teamName": "", "first10k": "1"}
    users["6"] = {"firstname": "F", "lastname": "F", "teamName": "", "first10k": "0"}
    users["7"] = {"firstname": "G", "lastname": "G", "teamName": "MyTeam", "first10k": "0"}
    users["8"] = {"firstname": "H", "lastname": "H", "teamName": "", "first10k": "1"}
    users["9"] = {"firstname": "I", "lastname": "I", "teamName": "", "first10k": "0"}
    return users

@pytest.fixture(scope="session", autouse=True)
def testDB(users, request):
    if os.path.exists(DEFAULT_TEST_DB):
        print("Clean old test database.")
        os.remove(DEFAULT_TEST_DB)
    UserDB.connect(DEFAULT_TEST_DB)
    UserDB.initSchema()

    user_values = []
    for user in users.values():
        user_values.append([user["firstname"], user["lastname"], user["teamName"], user["first10k"]])
    UserDB.insertUsers(user_values)

    def testDB_teardown():
        # Teardown is called when a method using testDB ends.
        UserDB.close()
    request.addfinalizer(testDB_teardown)