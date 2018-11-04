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

def testDupUser():
    data = checkTeam("HelloWorld", users["1"], users["1"], users["3"], users["3"])
    print(data)
    assert(data["success"] == False)
    assert(data["teamName"] == "Ok")
    assert(data["member1"] == "Ok")
    assert(data["member2"] == "Duplicate name found")
    assert(data["member3"] == "Ok")
    assert(data["member4"] == "Duplicate name found")

def testNotExist():
    notExistUser = {"firstname": "H", "lastname": "H"}
    data = checkTeam("HelloWorld", users["1"], users["2"], notExistUser, users["4"])
    assert(data["success"] == False)
    assert(data["teamName"] == "Ok")
    assert(data["member1"] == "Ok")
    assert(data["member2"] == "Ok")
    assert(data["member3"] == "User not found")
    assert(data["member4"] == "Ok")

def testAlreadyRegistered():
    data = checkTeam("HelloWorld", users["1"], users["2"], users["3"], users["7"])
    assert(data["success"] == False)
    assert(data["teamName"] == "Ok")
    assert(data["member1"] == "Ok")
    assert(data["member2"] == "Ok")
    assert(data["member3"] == "Ok")
    assert(data["member4"] == "Already registered")

def testSwap10kPosition():
    data = checkTeam("HelloWorld", users["4"], users["3"], users["2"], users["1"])
    assert(data["success"] == False)
    assert(data["teamName"] == "Ok")
    assert(data["member1"] == "Not a 10k")
    assert(data["member2"] == "Not a 10k")
    assert(data["member3"] == "Not a 5k")
    assert(data["member4"] == "Not a 5k")

def testFailNot10k():
    data = checkTeam("HelloWorld", users["1"], users["2"], users["3"], users["5"])
    assert(data["success"] == False)
    assert(data["teamName"] == "Ok")
    assert(data["member1"] == "Ok")
    assert(data["member2"] == "Ok")
    assert(data["member3"] == "Ok")
    assert(data["member4"] == "Not a 5k")

def testDupTeam():
    data = checkTeam("MyTeam", users["1"], users["2"], users["3"], users["4"])
    assert(data["success"] == False)
    assert(data["teamName"] == "Team name's already existed")
    assert(data["member1"] == "Ok")
    assert(data["member2"] == "Ok")
    assert(data["member3"] == "Ok")
    assert(data["member4"] == "Ok")

def testPass():
    data = checkTeam("MyNewTeam", users["1"], users["2"], users["3"], users["4"])
    assert(data["success"] == True)
    assert(data["teamName"] == "Ok")
    assert(data["member1"] == "Ok")
    assert(data["member2"] == "Ok")
    assert(data["member3"] == "Ok")
    assert(data["member4"] == "Ok")
