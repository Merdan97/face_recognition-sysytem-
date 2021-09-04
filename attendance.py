from os import path
import os
from re import I
from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
from time import strftime
from datetime import datetime
import cv2
import os
import csv
import numpy as np
from tkinter import filedialog


class Attendance:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1500x790+0+0")
        self.root.title("Isgarleriň Maglumatynyň sanawy")
        
        #===================  variable================
        self.var_id=StringVar()
        self.var_name=StringVar()
        self.var_fam=StringVar()
        self.var_image=StringVar()
        self.var_image1=StringVar()
        
       


        #title
        title_lbl=Label(root, text="Kesgitlenen ýüzleriň sanawy", font=("times new roman",35, "bold"), bg="white", fg="red")
        title_lbl.place(x=0,y=0, width=1530, height=45)        
        #bakground image
        img3=Image.open(r"C:\Users\User\Desktop\facesystem\college_images\digitization.jpg")
        img3=img3.resize((1530,710),Image.ANTIALIAS)
        self.photoimg3=ImageTk.PhotoImage(img3)

        bg_img=Label(self.root,image=self.photoimg3)
        bg_img.place(x=0,y=45,width=1530, height=710)
        #main frame
        main_frame=Frame(bg_img, bd=2, bg="white")
        main_frame.place(x=0,y=0,width=1530,height=650)

        #left frame

        Left_frame=LabelFrame(main_frame, bd=2,bg="white" ,relief=RIDGE, text="Maglumatlary girizmek" ,font=("times new roman",12, "bold"))
        Left_frame.place(x=30,y=10, width=400, height=580)
        
        #ID label
        name_label=Label(Left_frame, text="ID:",font=("times new roman",12, "bold"), bg="white")
        name_label.grid(row=4,column=0, padx=10,pady=5,sticky=W)


        #ID_enter
        name_entry=ttk.Entry(Left_frame,textvariable=self.var_id, width=20,font=("times new roman",14))
        name_entry.grid(row=4,column=1, padx=10,pady=5,sticky=W)


        #name label
        name_label=Label(Left_frame, text="Ady:",font=("times new roman",12, "bold"), bg="white")
        name_label.grid(row=5,column=0, padx=10,pady=5,sticky=W)


        #name_enter
        name_entry=ttk.Entry(Left_frame,textvariable=self.var_name ,width=20,font=("times new roman",14))
        name_entry.grid(row=5,column=1, padx=10,pady=5,sticky=W)

         #name label
        name_label=Label(Left_frame, text="Familya:",font=("times new roman",12, "bold"), bg="white")
        name_label.grid(row=6,column=0, padx=10,pady=5,sticky=W)
         #name_enter
        name_entry=ttk.Entry(Left_frame,textvariable=self.var_fam ,width=20,font=("times new roman",14))
        name_entry.grid(row=6,column=1, padx=10,pady=5,sticky=W)

          #button1       
        btn_save=Button(Left_frame,text="Import csv",command=self.importCsv, width=15,font=("times new roman",12, "bold"),bg="blue", fg="white")
        btn_save.grid(row=15,column=0, padx=10,pady=5,sticky=W)

         #button2
        btn_save=Button(Left_frame,text="Export csv",command=self.exportCsv, width=15,font=("times new roman",12, "bold"),bg="blue", fg="white")
        btn_save.grid(row=15,column=1 , padx=10,pady=5,sticky=W)

        #button3
        btn_save=Button(Left_frame,text="Update",command=self.importCsv, width=15,font=("times new roman",12, "bold"),bg="blue", fg="white")
        btn_save.grid(row=16,column=0 , padx=10,pady=5,sticky=W)

         #button4
        btn_save=Button(Left_frame,text="Reset",command=self.reset_data, width=15,font=("times new roman",12, "bold"),bg="blue", fg="white")
        btn_save.grid(row=16,column=1 , padx=10,pady=5,sticky=W)
     

        #right frame
        right_frame=LabelFrame(main_frame, bd=2,bg="white" ,relief=RIDGE, text="Maglumatlar toplumy" ,font=("times new roman",12, "bold"))
        right_frame.place(x=440,y=10, width=1000, height=580)

        # table frame

        table_frame=Frame(right_frame, bd=2, bg="white",relief=RIDGE)
        table_frame.place(x=5,y=0,width=990,height=500)
      
        scroll_x=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(table_frame,orient=VERTICAL)

        self.student_table=ttk.Treeview(table_frame,column=("ady", "fam", "wagt","sene"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)


        self.student_table.heading("ady",text="Ady")
        self.student_table.heading("fam",text="Familýa")
        self.student_table.heading("wagt",text="Wagty")
        self.student_table.heading("sene",text="Sene")        
        self.student_table["show"]="headings"

        self.student_table.column("ady", width=10)
        self.student_table.column("fam", width=100)
        self.student_table.column("wagt", width=100)
        self.student_table.column("sene", width=10)

        self.student_table.pack(fill=BOTH,expand=1)
        self.student_table.bind("<ButtonRelease>", self.get_cursor)
        # self.fetch_data()
 


    


#=============================================fetch data ======================
    def fetch_data(self,rows):
        self.student_table.delete(*self.student_table.get_children())
        for i in rows:
            self.student_table.insert("",END, values=i)


   
#==========================import data===========================
    def importCsv(self): 
        global mydata
        mydata=[] 
        fln=filedialog.askopenfilename(initialdir=os.getcwd(),title="Open CSV", filetypes=(("CSV File","*.csv"),("ALL File","*.*")),parent=self.root)
        with open(fln) as myfile:
            csvread=csv.reader(myfile, delimiter=",")
            for i in csvread:
                mydata.append(i)     
            self.fetch_data(mydata)




#===================================Export data=========================
    def exportCsv(self):
        try:
            if len(mydata)<1:
                messagebox.showerror("No Data", "No Data found to export", parent=self.root)
                return False
            fln=filedialog.asksaveasfilename(initialdir=os.getcwd(),title="Open CSV", filetypes=(("CSV File","*.csv"),("ALL File","*.*")),parent=self.root)
            with open(fln, mode="w", newline="") as myfile: 
                exp_write=csv.writer(myfile, delimiter=",")
                for i in mydata:
                    exp_write.writerow(i)
                messagebox.showinfo("Data Export ", "Your data exported"+os.path.basename(fln)+"successfully") 
        except Exception as es:
            messagebox.showerror("Error", f"Error to :{str(es)}", parent=self.root)
#============================get cursor============================
    def get_cursor(self, event=""):
        cursor_row=self.student_table.focus()
        content=self.student_table.item(cursor_row)
        data=content["values"]

        self.var_id.set(data[0]),
        self.var_name.set(data[1]),
        self.var_fam.set(data[2]),
        self.var_image.set(data[3])

    def reset_data(self):
        self.var_id.set("")
        self.var_name.set("")
        self.var_fam.set("")
        self.var_image.set("")


if __name__=="__main__":
    root=Tk()   
    obj=Attendance(root)
    root.mainloop()




