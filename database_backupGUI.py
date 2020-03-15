import pipes
import time
from tkinter import *
import os
from tkinter import messagebox
import mysql.connector


class Gui(Frame):

    def __init__(self,parent):
        self.parent = parent
        Frame.__init__(self,parent)

        self.Frame = Frame()
        self.Frame.pack(fill = X)

        self.title = Label(self.Frame,text='Quadriga Database Backup Tool V.1',bg='SpringGreen2')
        self.title.pack(fill=X)

        self.Frame1 = Frame()
        self.Frame1.pack(fill = X,pady=15)

        self.userLabel = Label(self.Frame1, text='User')
        self.userLabel.pack(side=LEFT)
        self.userText = Text(self.Frame1, width=12, height=1)
        self.userText.pack(side=LEFT)

        self.hostLabel = Label(self.Frame1, text= 'Host')
        self.hostLabel.pack(side= LEFT)
        self.hostText = Text(self.Frame1,width=12, height= 1)
        self.hostText.pack(side=LEFT)

        self.passwordLabel = Label(self.Frame1, text='Password')
        self.passwordLabel.pack(side=LEFT)
        self.passwordText = Entry(self.Frame1, width=15, show='*')
        self.passwordText.config(show='*')
        self.passwordText.pack(side=LEFT)

        self.Frame2 = Frame()
        self.Frame2.pack(fill = X)

        self.var = IntVar()
        self.buttoncsv = Checkbutton(self.Frame2, text="Back Up Single Database", variable=self.var, onvalue=1)
        self.buttoncsv.pack(side=TOP, pady=5)

        self.buttontxt = Checkbutton(self.Frame2, text="Back Up All Database", variable=self.var, onvalue=2)
        self.buttontxt.pack(side=TOP)

        self.databaseNameLabel = Label(self.Frame2, text='If you want to back up single db, give database name !')
        self.databaseNameLabel.pack(side=TOP,pady=5)

        self.databaseNameText = Text(self.Frame2, width=12, height=1)
        self.databaseNameText.pack(side=TOP,pady=5)

        self.selectGzSql = Label(self.Frame2, text = 'Do you want compression ?')
        self.selectGzSql.pack(side=TOP,pady=5)
        self.var2 = IntVar()
        self.buttonComp = Checkbutton(self.Frame2, text=".sql.gz", variable=self.var2, onvalue=1)
        self.buttonComp.pack(side=TOP, pady=5)

        self.buttontxtSql = Checkbutton(self.Frame2, text=".sql", variable=self.var2, onvalue=2)
        self.buttontxtSql.pack(side=TOP)

        self.run = Button(self.Frame2, text=' Run !', command=self.call_functions)
        self.run.pack(side=TOP)



    def engine(self):


        self.DB_HOST = self.hostText.get("1.0",END)
        self.DB_USER = self.hostText.get("1.0",END)
        self.DB_USER_PASSWORD = self.passwordText.get()
        self.DB_NAME = '/backup/databases.txt'
        # DB_NAME = 'give a database name'
        # if you want to back up only one database you uncomment row 36 and call backup_singleDb() function  at row 73
        self.BACKUP_PATH = '/backup/dbbackup'

        self.DATETIME = time.strftime('%Y%m%d-%H%M%S')
        self.date = (self.DATETIME.split('-')[0])
        self.date = self.date[-2] + self.date[-1] + self.date[-4] + self.date[-3] + self.date[:4]

        self.TODAYBACKUPPATH = self.BACKUP_PATH + '/' + self.date



    def create_needed_dirs(self):

        if (os.path.exists("/backup/dbbackup")) != True:
            os.makedirs('/backup/dbbackup')
        try:
            os.stat(self.TODAYBACKUPPATH)
        except:
            os.makedirs(self.TODAYBACKUPPATH)

    def create_txt(self,path):

        with open(os.path.join(path, 'databases.txt'), 'a'):
            pass

    # getting database names and writing them into txt file
    def write_dbNames_to_txt(self,path):
        dbTextFile = open(r'/backup/{path}'.format(path=path), "w")
        user= self.userText.get("1.0",'end-1c')
        password= self.passwordText.get()
        host = self.hostText.get("1.0",'end-1c')

        conn = mysql.connector.connect(user= user, password= str(password),
                                       host= host)
        cursor = conn.cursor()
        databases = ("show databases")
        cursor.execute(databases)
        for databases in cursor:
            dbTextFile.write(databases[0] + '\n')

        print("checking for databases names file.")
        if os.path.exists(self.DB_NAME):
            file1 = open(self.DB_NAME)
            self.multi = True
            print("Databases file found...")
            print("Starting backup of all dbs listed in file " + self.DB_NAME)
        else:
            print("Databases file not found...")
            print("Starting backup of database " + self.DB_NAME)
            self.multi = False

    def backup_allDbs(self):

        extention =''
        if (self.var2.get()==1):
            extention= '.sql.gz'
        else:
            extention='.sql'


        in_file = open(self.DB_NAME, "r")
        flength = len(in_file.readlines())
        print(flength)
        in_file.close()
        p = 1
        dbfile = open(self.DB_NAME, "r")

        while p <= flength:
            db = dbfile.readline()
            db = db[:-1]  # reading database name from file
            print(db)
            dumpcmd = "mysqldump -h " + self.hostText.get("1.0",'end-1c') + " -u " + self.userText.get("1.0",'end-1c')\
                      + " -p" + self.passwordText.get() + " " + db +' | gzip'+  " > " + pipes.quote(self.TODAYBACKUPPATH) + "/" + db + '-' + self.date + extention
            os.system(dumpcmd)

            p = p + 1
        dbfile.close()



    def backup_singleDb(self):

        extention = ''
        if (self.var2.get() == 1):
            extention = '.sql.gz'
        else:
            extention = '.sql'

        single_db = self.databaseNameText.get("1.0",'end-1c')
        print(single_db)
        if single_db == '':
            messagebox.showinfo("Title", "Please give a database name ! ")

        else:

            dumpcmd = "mysqldump -h " + self.hostText.get("1.0",'end-1c') + " -u " + self.userText.get("1.0",'end-1c')\
                              + " -p" + self.passwordText.get() + " " + single_db +' | gzip' +" > " + pipes.quote(self.TODAYBACKUPPATH) + "/" + single_db + '-' + self.date + extention
            os.system(dumpcmd)

    def choise(self):

        if self.var.get() == 1:

            self.backup_singleDb()
        else:
            self.backup_allDbs()


    def call_functions(self):

        self.engine()

        self.create_needed_dirs()

        self.create_txt('/backup')

        self.write_dbNames_to_txt("databases.txt")

        self.choise()


if __name__ == '__main__':

    root = Tk()
    root.title('Back Up Database')
    root.configure()

    app = Gui(root)
    app.pack()

    root.geometry("500x330")
    root.mainloop()
