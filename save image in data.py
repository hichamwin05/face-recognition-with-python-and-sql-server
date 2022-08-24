import os
import sqlite3
import face_recognition as facerecg

#making a sql file
import pyodbc
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-TQ1SBD9\MSSQLSERVER99;'
                      'Database=face_recognition;'
                      'Trusted_Connection=yes;')
cur = conn.cursor()
#def to conv image file to binary
def convert_binary(file):
    with open(file,"rb") as img_read:
        img = img_read.read()
        return img

print ("Label the Images properly")
#input folder path, checks the folder for .jpg file
path = input("Folder Path: ")
print ("Scanning for image files")

for files in os.listdir(path):
    if files.endswith(".jpg") or files.endswith(".png") or files.endswith(".jpeg"):
        print (f"Encoding {files}")
        #extract the name of file
        name = files.split(".")[0]
        # print (name)
        #extract the path of img file
        file_path = os.path.join(path,files)
        # print(file_path)
        #converts img to binary
        img_binary = convert_binary(file_path)
        # print(img_binary)
        # #load the image file
        face = facerecg.load_image_file(file_path)
        # #encoding the image file
        face_encoding = facerecg.face_encodings(face)[0]
        ts = face_encoding.tostring()
        # print (type(face_encoding))

        #entering values in SQL
        cur.execute("insert into stor_image(Person,xx) values(?,?)",(name,ts))

#writing all the values in DB
conn.commit()
cur.close()
print("Successfully Add Image DB")