import sqlite3

def setMsgData(data, index, msg):
    if index == 0:
        key = "member1"
    elif index == 1:
        key = "member2"
    elif index == 2:
        key = "member3"
    elif index == 3:
        key = "member4"
    else:
        assert(0)
    data[key] = msg
    return data

class UserDB:
    """Singleton style database class"""
    DB_CONN = None

    @classmethod
    def connect(cls, db_path):
        if cls.DB_CONN is None:
            print("Connecting database: %s" % (db_path))
            cls.DB_CONN = sqlite3.connect(db_path)
        else:
            print("Database has connected")

    @classmethod
    def close(cls):
        if cls.DB_CONN:
            cls.DB_CONN.close()
    
    @classmethod
    def initSchema(cls):
        print("Initialize database schema")
        c = cls.DB_CONN.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                (firstname TEXT, lastname TEXT, teamName TEXT, first10k INTEGER)''')
        cls.DB_CONN.commit()

    @classmethod
    def listAll(cls):
        c = cls.DB_CONN.cursor()
        c.execute("SELECT firstname, lastname, teamName, first10k FROM users")
        rows = c.fetchall()
        return rows
    
    @classmethod
    def listByUser(cls, firstname, lastname):
        c = cls.DB_CONN.cursor()
        values = (firstname, lastname)
        c.execute("SELECT firstname, lastname, teamName, first10k FROM users WHERE (firstname = ? AND lastname = ?)", values)
        rows = c.fetchall()
        return rows

    @classmethod
    def insertUser(cls, firstname, lastname, teamName, first10k):
        user = [firstname, lastname, teamName, first10k]
        c = cls.DB_CONN.cursor()
        c.execute("INSERT INTO users VALUES (?,?,?,?)", user)
        cls.DB_CONN.commit()
    
    @classmethod
    def insertUsers(cls, users):
        c = cls.DB_CONN.cursor()
        for user in users:
            # user is [firstname, lastname, teamName, first10k]
            c.execute("INSERT INTO users VALUES (?,?,?,?)", user)
        cls.DB_CONN.commit()
    
    @classmethod
    def updateTeamByUser(cls, teamName, firstname, lastname):
        values = [teamName, firstname, lastname]
        c = cls.DB_CONN.cursor()
        c.execute("""UPDATE users SET teamName=? WHERE firstname=? AND lastname=?""", values)
        cls.DB_CONN.commit()

    @classmethod
    def checkTeam(cls, teamName, user1, user2, user3, user4):
        userList = [(user1["firstname"],user1["lastname"]) , (user2["firstname"],user2["lastname"]) ,
                    (user3["firstname"],user3["lastname"]) , (user4["firstname"],user4["lastname"])]

        data = {"member1": "notInit", "member2": "notInit", "member3": "notInit", "member4": "notInit"}

        c = cls.DB_CONN.cursor()

        # Check teamName
        values = (teamName, )
        c.execute("""SELECT teamName FROM users WHERE teamName = ?""", values)
        all_data = c.fetchall()
        if len(all_data) != 0:
            data["teamName"] = "Team name's already existed"
        else:
            data["teamName"] = "Ok"

        userSet = set()
        userNotFirst10k = []

        for index in range(0,4):
            if userList[index][0] == "" or userList[index][1] == "":
                setMsgData(data, index, "Field cannot be empty")
                continue
            if userList[index] in userSet:
                setMsgData(data, index, "Duplicate name found")
                continue
            userSet.add(userList[index])

            all_data = UserDB.listByUser(userList[index][0], userList[index][1])

            if len(all_data) == 0:
                setMsgData(data, index, "User not found")
                continue

            if len(all_data) > 1:
                print("Error: found duplicate data in database %s %s" % (userList[index][0], userList[index][1]))
                assert(0)

            firstname = all_data[0][0]
            lastname = all_data[0][1]
            team = all_data[0][2]
            isFirst10k = all_data[0][3]

            if not(team == "" or team == None):
                setMsgData(data, index, "Already registered")
                continue

            if isFirst10k == 0:
                userNotFirst10k.append(index)

            setMsgData(data, index, "Ok")

        # Not enough first10k
        if len(userNotFirst10k) > 2:
            for index in userNotFirst10k:
                setMsgData(data, index, "This user ran 10k before")

        if all([data["teamName"] == "Ok",
        data["member1"] == "Ok",
        data["member2"] == "Ok",
        data["member3"] == "Ok",
        data["member4"] == "Ok"]):
            data["success"] = True
        else:
            data["success"] = False

        return data