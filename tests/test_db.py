import os
import sys
import inspect
CURRENT_DIR = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
# Include paths for module search
sys.path.insert(0, PARENT_DIR)

from db import UserDB

def testFail_DupUser(users):
    data = UserDB.checkTeam("HelloWorld", users["1"], users["1"], users["3"], users["3"])
    print(data)
    assert(data["success"] == False)
    assert(data["teamName"] == "Ok")
    assert(data["member1"] == "Ok")
    assert(data["member2"] == "Duplicate name found")
    assert(data["member3"] == "Ok")
    assert(data["member4"] == "Duplicate name found")

def testFail_DupUserAllFirst10k(users):
    data = UserDB.checkTeam("HelloWorld", users["1"], users["2"], users["5"], users["5"])
    print(data)
    assert(data["success"] == False)
    assert(data["teamName"] == "Ok")
    assert(data["member1"] == "Ok")
    assert(data["member2"] == "Ok")
    assert(data["member3"] == "Ok")
    assert(data["member4"] == "Duplicate name found")

def testFail_UserNotExist(users):
    notExistUser = {"firstname": "Z", "lastname": "Z"}
    data = UserDB.checkTeam("HelloWorld", users["1"], users["2"], notExistUser, users["4"])
    assert(data["success"] == False)
    assert(data["teamName"] == "Ok")
    assert(data["member1"] == "Ok")
    assert(data["member2"] == "Ok")
    assert(data["member3"] == "User not found")
    assert(data["member4"] == "Ok")

def testFail_AlreadyRegistered(users):
    data = UserDB.checkTeam("HelloWorld", users["1"], users["2"], users["3"], users["7"])
    assert(data["success"] == False)
    assert(data["teamName"] == "Ok")
    assert(data["member1"] == "Ok")
    assert(data["member2"] == "Ok")
    assert(data["member3"] == "Ok")
    assert(data["member4"] == "Already registered")

def testFail_AlreadyRegisteredAndThree10k(users):
    data = UserDB.checkTeam("HelloWorld", users["3"], users["4"], users["6"], users["7"])
    assert(data["success"] == False)
    assert(data["teamName"] == "Ok")
    assert(data["member1"] == "This user ran 10k before")
    assert(data["member2"] == "This user ran 10k before")
    assert(data["member3"] == "This user ran 10k before")
    assert(data["member4"] == "Already registered")

def testSuccess_regular(users):
    data = UserDB.checkTeam("MyNewTeam", users["1"], users["2"], users["3"], users["4"])
    assert(data["success"] == True)
    assert(data["teamName"] == "Ok")
    assert(data["member1"] == "Ok")
    assert(data["member2"] == "Ok")
    assert(data["member3"] == "Ok")
    assert(data["member4"] == "Ok")

def testSuccess_SwapPosition(users):
    data = UserDB.checkTeam("HelloWorld", users["4"], users["3"], users["2"], users["1"])
    assert(data["success"] == True)
    assert(data["teamName"] == "Ok")
    assert(data["member1"] == "Ok")
    assert(data["member2"] == "Ok")
    assert(data["member3"] == "Ok")
    assert(data["member4"] == "Ok")

def testSuccess_SwapPosition_2(users):
    data = UserDB.checkTeam("HelloWorld", users["1"], users["3"], users["4"], users["2"])
    assert(data["success"] == True)
    assert(data["teamName"] == "Ok")
    assert(data["member1"] == "Ok")
    assert(data["member2"] == "Ok")
    assert(data["member3"] == "Ok")
    assert(data["member4"] == "Ok")

def testSuccess_ThreeFirst10k(users):
    data = UserDB.checkTeam("HelloWorld", users["1"], users["2"], users["3"], users["5"])
    assert(data["success"] == True)
    assert(data["teamName"] == "Ok")
    assert(data["member1"] == "Ok")
    assert(data["member2"] == "Ok")
    assert(data["member3"] == "Ok")
    assert(data["member4"] == "Ok")

def testFail_OneFirst10k(users):
    data = UserDB.checkTeam("HelloWorld", users["3"], users["1"], users["4"], users["6"])
    assert(data["success"] == False)
    assert(data["teamName"] == "Ok")
    assert(data["member1"] == "This user ran 10k before")
    assert(data["member2"] == "Ok")
    assert(data["member3"] == "This user ran 10k before")
    assert(data["member4"] == "This user ran 10k before")

def testSuccess_AllFirst10k(users):
    data = UserDB.checkTeam("HelloWorld", users["1"], users["2"], users["5"], users["8"])
    assert(data["success"] == True)
    assert(data["teamName"] == "Ok")
    assert(data["member1"] == "Ok")
    assert(data["member2"] == "Ok")
    assert(data["member3"] == "Ok")
    assert(data["member4"] == "Ok")

def testFail_AllNotFirst10k(users):
    data = UserDB.checkTeam("HelloWorld", users["3"], users["4"], users["6"], users["9"])
    assert(data["success"] == False)
    assert(data["teamName"] == "Ok")
    assert(data["member1"] == "This user ran 10k before")
    assert(data["member2"] == "This user ran 10k before")
    assert(data["member3"] == "This user ran 10k before")
    assert(data["member4"] == "This user ran 10k before")

def testFail_DupTeam(users):
    data = UserDB.checkTeam("MyTeam", users["1"], users["2"], users["3"], users["4"])
    assert(data["success"] == False)
    assert(data["teamName"] == "Team name's already existed")
    assert(data["member1"] == "Ok")
    assert(data["member2"] == "Ok")
    assert(data["member3"] == "Ok")
    assert(data["member4"] == "Ok")
