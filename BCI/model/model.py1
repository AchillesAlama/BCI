import MySQLdb

class trainingController():

    def connectToDB():
        db = MySQLdb.connect("localhost","testuser","test123","TESTDB" )
        cursor = db.cursor()

    def getSubject():
        getSubjectSQL = "SELECT Name FROM User"
        cursor.execute(getSubjectSQL)
        results = cursor.fetchall()
        return results

    def setSubject(subjectName,subjectBirthday,subjectGender,subjectNationality):
        saveSubjectSQL = "INSERT INTO User(Name, Birthday, Gender, Nationality) VALUES ('%s','%d','%s','%s')" % (subjectName, subjectBirthday, subjectGender, subjectNationality)
        try:
            cursor.execute(saveSubjectSQL)
            db.commit()
        except:
            db.rollback()
            print("Error while inserting subject to DB")

    def saveRun(Starttime, description, userId, moodID):
        saveRunSQL = "INSERT INTO User(Starttime, description, userId, moodID) VALUES ('%d','%s','%d','%d')" % (Starttime, description, userId, moodID)
        try:
            cursor.execute(saveRunSQL)
            db.commit()
        except:
            db.rollback()
            print("Error while inserting run to DB")

    def saveMeasurement(Value, Timestamp, SampleNumber, channelId):
        saveMeasurementSQL = "INSERT INTO User(Value, Timestamp, SampleNumber, channelId) VALUES ('%s','%d','%s','%s')" % (Value, Timestamp, SampleNumber, channelId)
        try:
            cursor.execute(saveMeasurementSQL)
            db.commit()
        except:
            db.rollback()
            print("Error while inserting measurement to DB")

    def saveChannel(Number, Placement, runId, Unit):
        saveChannelSQL = "INSERT INTO User(Number, Placement, runId, Unit) VALUES ('%s','%d','%s','%s')" % (Number, Placement, runId, Unit)
        try:
            cursor.execute(saveChannelSQL)
            db.commit()
        except:
            db.rollback()
            print("Error while inserting channel to DB")
