import psycopg2 as dbapi2
from classes.followed_project import FollowedProject
import datetime
from classes.model_config import dsn


class followed_project_operations:
    def __init__(self):
        self.last_key = None

    def AddFollowedProject(self, followed_project):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO FollowedProject (PersonId, FollowedProjectId, StartDate, Deleted) VALUES (%s, %s,' "+str(datetime.datetime.now())+"', False)"
            cursor.execute(query, (followed_project.PersonId, followed_project.FollowedProjectId))
            connection.commit()
            self.last_key = cursor.lastrowid

    def GetFollowedProjectByObjectId(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT FollowedProject.ObjectId ,PersonId ,p1.FirstName || ' ' || p1.LastName as PersonFullName
                       ,FollowedProjectId ,p2.Name as FollowedProjectName,StartDate
                       FROM FollowedProject
                       INNER JOIN Person as p1 ON (FollowedProject.PersonId = p1.ObjectId)
                       INNER JOIN Project as p2 ON (FollowedProject.FollowedProjectId = p2.ObjectId)
                       WHERE (FollowedProject.ObjectId=%s and FollowedProject.Deleted='0')"""
            cursor.execute(query, (key,))
            result = cursor.fetchone()
        return result

    # Belirtilen PersonId'ye sahip personın takip ettigi projeler
    def GetFollowedProjectListByPersonId(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT FollowedProject.ObjectId, PersonId, p1.FirstName || ' ' || p1.LastName as PersonFullName,
                        FollowedProjectId, p2.Name as FollowedProjectName,StartDate
                        FROM FollowedProject
                        INNER JOIN Person as p1 ON p1.ObjectId = FollowedProject.PersonId
                        INNER JOIN Project as p2 ON p2.ObjectId = FollowedProject.FollowedProjectId
                        WHERE FollowedProject.PersonId = %s"""
            cursor.execute(query, (key,))
            connection.commit()
            results = cursor.fetchall()
        return results

    # Belirtilen ProjectId'ye sahip projeyi takip eden personlar
    def GetFollowerPersonListByFollowedProjectId(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT FollowedProject.ObjectId, PersonId, p1.FirstName || ' ' || p1.LastName as PersonFullName,
                        FollowedProjectId, p2.Name as FollowedProjectName,StartDate
                        FROM FollowedProject
                        INNER JOIN Person as p1 ON p1.ObjectId = FollowedProject.PersonId
                        INNER JOIN Project as p2 ON p2.ObjectId = FollowedProject.FollowedProjectId
                        WHERE FollowedProject.FollowedProjectId = %s"""
            cursor.execute(query, (key,))
            connection.commit()
            results = cursor.fetchall()
        return results

    def DeleteFollowedProject(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM FollowedProject WHERE (ObjectId=%s)"""
            cursor.execute(query, (key,))
            connection.commit()

    def UpdateFollowedProject(self, key, personId, followedProjectId, startDate):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE FollowedProject SET PersonId=%s FollowedProjectId=%s StartDate=%s WHERE (ObjectId=%s)"""
            cursor.execute(query, (personId, followedProjectId, startDate, key))
            connection.commit()
