import os
import time
import pipes
import mysql.connector
from getpass import getpass

'''  Directly backups all databases with compression '''


#user = input('User for database >> ')
#password = getpass('Password for database >>')
#host = input('Host for database >> ')

user = "root"
password = "samet"
host = "localhost"

DB_HOST = host
DB_USER = user
DB_USER_PASSWORD = password
DB_NAME = '/backup/databases.txt'
#DB_NAME = 'give a database name'

BACKUP_PATH = '/backup/dbbackup'


DATETIME = time.strftime('%Y%m%d-%H%M%S')
date =(DATETIME.split('-')[0])
date = date[-2]+date[-1] + date[-4]+ date[-3] + date[:4]

TODAYBACKUPPATH = BACKUP_PATH + '/' + date


def create_needed_dirs():

    if (os.path.exists("/backup/dbbackup")) != True:
        os.makedirs('/backup/dbbackup')
    try:
        os.stat(TODAYBACKUPPATH)
    except:
        os.makedirs(TODAYBACKUPPATH)
create_needed_dirs()


def create_txt(path):

    with open(os.path.join(path, 'databases.txt'), 'a'):
        pass

create_txt('/backup')


#getting database names and writing them into txt file
def write_dbNames_to_txt(path):
    dbTextFile = open(r'/backup/{path}'.format(path=path), "w")
    conn = mysql.connector.connect(user= DB_USER, password= DB_USER_PASSWORD,
                                   host= DB_HOST)
    cursor = conn.cursor()
    databases = ("show databases")
    cursor.execute(databases)
    for databases in cursor:
        dbTextFile.write(databases[0]+'\n')

write_dbNames_to_txt("databases.txt")


# Code for checking if you want to take single database backup or assinged multiple backups in DB_NAME.
print("checking for databases names file.")
if os.path.exists(DB_NAME):
    file1 = open(DB_NAME)
    multi = True
    print("Databases file found...")
    print("Starting backup of all dbs listed in file " + DB_NAME)
else:
    print("Databases file not found...")
    print("Starting backup of database " + DB_NAME)
    multi = False


def backup_allDbs():

    # Starting actual database backup process.
    extention = '.sql.gz'
    in_file = open(DB_NAME,"r")
    flength = len(in_file.readlines())
    print(flength)
    in_file.close()
    p = 1
    dbfile = open(DB_NAME,"r")

    while p <= flength:

        db = dbfile.readline()
        db = db[:-1]# reading database name from file
        print(db)
        dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + ' | gzip'+  " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + '-' + date + extention
        os.system(dumpcmd)

        p = p + 1
    dbfile.close()

if __name__ == '__main__':

    backup_allDbs()