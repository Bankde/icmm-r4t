import sqlite3
import os
from register import checkTeam
import pytest

users_db = "users.db"

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

@pytest.fixture(scope="session", autouse=True)
def initTest():
    os.remove(users_db)
    conn = sqlite3.connect(users_db)
    c = conn.cursor()
    c.execute('''CREATE TABLE users
               (firstname TEXT, lastname TEXT, teamName TEXT, first10k INTEGER)''')
    conn.commit()
    for key in users:
        values = (users[key]["firstname"], users[key]["lastname"], users[key]["teamName"], users[key]["first10k"])
        c.execute('''INSERT INTO users VALUES (?,?,?,?)''', values)
    conn.commit()
    conn.close()

def testFail_DupUser():
    data = checkTeam("HelloWorld", users["1"], users["1"], users["3"], users["3"])
    print(data)
    assert(data["success"] == False)
    assert(data["teamName"] == "Ok")
    assert(data["member1"] == "Ok")
    assert(data["member2"] == "Duplicate name found")
    assert(data["member3"] == "Ok")
    assert(data["member4"] == "Duplicate name found")

def testFail_DupUserAllFirst10k():
    data = checkTeam("HelloWorld", users["1"], users["2"], users["5"], users["5"])
    print(data)
    assert(data["success"] == False)
    assert(data["teamName"] == "Ok")
    assert(data["member1"] == "Ok")
    assert(data["member2"] == "Ok")
    assert(data["member3"] == "Ok")
    assert(data["member4"] == "Duplicate name found")

def testFail_UserNotExist():
    notExistUser = {"firstname": "Z", "lastname": "Z"}
    data = checkTeam("HelloWorld", users["1"], users["2"], notExistUser, users["4"])
    assert(data["success"] == False)
    assert(data["teamName"] == "Ok")
    assert(data["member1"] == "Ok")
    assert(data["member2"] == "Ok")
    assert(data["member3"] == "User not found")
    assert(data["member4"] == "Ok")

def testFail_AlreadyRegistered():
    data = checkTeam("HelloWorld", users["1"], users["2"], users["3"], users["7"])
    assert(data["success"] == False)
    assert(data["teamName"] == "Ok")
    assert(data["member1"] == "Ok")
    assert(data["member2"] == "Ok")
    assert(data["member3"] == "Ok")
    assert(data["member4"] == "Already registered")

def testFail_AlreadyRegisteredAndThree10k():
    data = checkTeam("HelloWorld", users["3"], users["4"], users["6"], users["7"])
    assert(data["success"] == False)
    assert(data["teamName"] == "Ok")
    assert(data["member1"] == "This user ran 10k before")
    assert(data["member2"] == "This user ran 10k before")
    assert(data["member3"] == "This user ran 10k before")
    assert(data["member4"] == "Already registered")

def testSuccess_regular():
    data = checkTeam("MyNewTeam", users["1"], users["2"], users["3"], users["4"])
    assert(data["success"] == True)
    assert(data["teamName"] == "Ok")
    assert(data["member1"] == "Ok")
    assert(data["member2"] == "Ok")
    assert(data["member3"] == "Ok")
    assert(data["member4"] == "Ok")

def testSuccess_SwapPosition():
    data = checkTeam("HelloWorld", users["4"], users["3"], users["2"], users["1"])
    assert(data["success"] == True)
    assert(data["teamName"] == "Ok")
    assert(data["member1"] == "Ok")
    assert(data["member2"] == "Ok")
    assert(data["member3"] == "Ok")
    assert(data["member4"] == "Ok")

def testSuccess_SwapPosition_2():
    data = checkTeam("HelloWorld", users["1"], users["3"], users["4"], users["2"])
    assert(data["success"] == True)
    assert(data["teamName"] == "Ok")
    assert(data["member1"] == "Ok")
    assert(data["member2"] == "Ok")
    assert(data["member3"] == "Ok")
    assert(data["member4"] == "Ok")

def testSuccess_ThreeFirst10k():
    data = checkTeam("HelloWorld", users["1"], users["2"], users["3"], users["5"])
    assert(data["success"] == True)
    assert(data["teamName"] == "Ok")
    assert(data["member1"] == "Ok")
    assert(data["member2"] == "Ok")
    assert(data["member3"] == "Ok")
    assert(data["member4"] == "Ok")

def testFail_OneFirst10k():
    data = checkTeam("HelloWorld", users["3"], users["1"], users["4"], users["6"])
    assert(data["success"] == False)
    assert(data["teamName"] == "Ok")
    assert(data["member1"] == "This user ran 10k before")
    assert(data["member2"] == "Ok")
    assert(data["member3"] == "This user ran 10k before")
    assert(data["member4"] == "This user ran 10k before")

def testSuccess_AllFirst10k():
    data = checkTeam("HelloWorld", users["1"], users["2"], users["5"], users["8"])
    assert(data["success"] == True)
    assert(data["teamName"] == "Ok")
    assert(data["member1"] == "Ok")
    assert(data["member2"] == "Ok")
    assert(data["member3"] == "Ok")
    assert(data["member4"] == "Ok")

def testFail_AllNotFirst10k():
    data = checkTeam("HelloWorld", users["3"], users["4"], users["6"], users["9"])
    assert(data["success"] == False)
    assert(data["teamName"] == "Ok")
    assert(data["member1"] == "This user ran 10k before")
    assert(data["member2"] == "This user ran 10k before")
    assert(data["member3"] == "This user ran 10k before")
    assert(data["member4"] == "This user ran 10k before")

def testFail_DupTeam():
    data = checkTeam("MyTeam", users["1"], users["2"], users["3"], users["4"])
    assert(data["success"] == False)
    assert(data["teamName"] == "Team name's already existed")
    assert(data["member1"] == "Ok")
    assert(data["member2"] == "Ok")
    assert(data["member3"] == "Ok")
    assert(data["member4"] == "Ok")
