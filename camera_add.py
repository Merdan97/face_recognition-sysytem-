from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import center_tk_window


class Addcamera:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1050x360+0+0")
        self.root.title("Isgarlerin Maglumaty")
        self.root.configure(bg='cyan')
        #self.root.eval('tk::PlaceWindow . center')
        #os.environ["SDL_VIDEO_CENTERED"] = "1"
       
        #===================  variable================
        self.var_id=StringVar()
        self.var_name=StringVar()
        self.var_fam=StringVar()
        

        #title
        title_lbl=Label(root, text="Camera  Goshmak ucin sahypa", font=("times new roman",25, "bold"), bg="cyan", fg="red")
        title_lbl.place(x=0,y=0, width=1100, height=45)        
        #bakground image
        img3=Image.open(r"C:\Users\User\Desktop\facesystem\college_images\digitization.jpg")
        img3=img3.resize((1000,500),Image.ANTIALIAS)
        self.photoimg3=ImageTk.PhotoImage(img3)

        bg_img=Label(self.root,image=self.photoimg3)
        bg_img.place(x=0,y=45,width=1530, height=710)
        #main frame
        main_frame=Frame(bg_img, bd=2, bg="white")
        main_frame.place(x=0,y=0,width=1530,height=650)

        #left frame

        Left_frame=LabelFrame(main_frame, bd=2,bg="white" ,relief=RIDGE, text="Maglumatlary girizmek" ,font=("times new roman",12, "bold"))
        Left_frame.place(x=10,y=10, width=400, height=300)    

        #name label
        name_label=Label(Left_frame, text="Cameranyň ady:",font=("times new roman",10, "bold"), bg="white")
        name_label.grid(row=5,column=0, padx=10,pady=5,sticky=W)


        #name_enter
        name_entry=ttk.Entry(Left_frame,textvariable=self.var_name ,width=25,font=("times new roman",12))
        name_entry.grid(row=5,column=1, padx=10,pady=5,sticky=W)

         #name label
        name_label=Label(Left_frame, text="Cameranyň url salgysy:",font=("times new roman",10, "bold"), bg="white")
        name_label.grid(row=6,column=0, padx=10,pady=5,sticky=W)
         #name_enter
        name_entry=ttk.Entry(Left_frame,textvariable=self.var_fam ,width=25,font=("times new roman",12))
        name_entry.grid(row=6,column=1, padx=10,pady=5,sticky=W)            
        

         #button1       
        btn_save=Button(Left_frame,text="Save",command=self.add_data, width=15,font=("times new roman",12, "bold"),bg="blue", fg="white")
        btn_save.grid(row=15,column=0, padx=10,pady=5,sticky=W)

         #button2
        btn_save=Button(Left_frame,text="Update",command=self.update_data, width=15,font=("times new roman",12, "bold"),bg="blue", fg="white")
        btn_save.grid(row=15,column=1 , padx=10,pady=5,sticky=W)

        #button3
        btn_save=Button(Left_frame,text="Delete",command=self.delete_data, width=15,font=("times new roman",12, "bold"),bg="blue", fg="white")
        btn_save.grid(row=16,column=0 , padx=10,pady=5,sticky=W)

         #button4
        btn_save=Button(Left_frame,text="Reset",command=self.reset_data, width=15,font=("times new roman",12, "bold"),bg="blue", fg="white")
        btn_save.grid(row=16,column=1 , padx=10,pady=5,sticky=W)

       
        #right frame
        right_frame=LabelFrame(main_frame, bd=2,bg="white" ,relief=RIDGE, text="Maglumatlar toplumy" ,font=("times new roman",12, "bold"))
        right_frame.place(x=415,y=10, width=600, height=300)

        # table frame

        table_frame=Frame(right_frame, bd=2, bg="white",relief=RIDGE)
        table_frame.place(x=5,y=5,width=580,height=280)
      
        scroll_x=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(table_frame,orient=VERTICAL)

        self.student_table=ttk.Treeview(table_frame,column=("id", "name", "url"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)


        self.student_table.heading("id",text="ID")
        self.student_table.heading("name",text="camera ady")
        self.student_table.heading("url",text="Camera URL")
         
        self.student_table["show"]="headings"

        self.student_table.column("id", width=1)
        self.student_table.column("name", width=100)
        self.student_table.column("url", width=300)
      

        self.student_table.pack(fill=BOTH,expand=1)
        self.student_table.bind("<ButtonRelease>", self.get_cursor)
        self.fetch_data()
 

#============================ function decration===========================
    def add_data(self):
        if self.var_id.get()==""  or self.var_name.get()=="":
            messagebox.showerror("Error","ahli  zatlary doly girizmeli")
        else:
            try:                
                #messagebox.showinfo("Success","Welcome")
                conn=mysql.connector.connect(host="localhost", username="root", password="", database="mywork")
                my_cursor=conn.cursor()
                sql="insert into camera (kameranyn_ady, url_kamera) values(%s,%s,%s,%s)"
                val=(
                    self.var_name.get(),
                    self.var_fam.get()
                    
                )
                my_cursor.execute(sql,val)
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success","Person", parent=self.root)

            except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}" )


#=============================================fetch data ======================
    def fetch_data(self):
        conn=mysql.connector.connect(host="localhost", username="root", password="", database="mywork")
        my_cursor=conn.cursor()
        my_cursor.execute("select * from camera")
        data=my_cursor.fetchall()

        if len(data)!=0:
            self.student_table.delete(*self.student_table.get_children())
            for i in data:
                self.student_table.insert("",END, values=i)
            conn.commit()
        conn.close()

#============================get cursor============================
    def get_cursor(self, event=""):
        cursor_focus=self.student_table.focus()
        content=self.student_table.item(cursor_focus)
        data=content["values"]

        self.var_id.set(data[0]),
        self.var_name.set(data[1]),
        self.var_fam.set(data[2]),
       



#==================== update function==================

    def update_data(self):
        if self.var_id.get()=="" or self.var_name.get()=="":
            messagebox.showerror("Error","ahli  zatlary doly girizmeli")
        else:
            try:
                update=messagebox.askyesno("Update", "Do you this person update", parent=self.root)
                if  update>0:
                    conn=mysql.connector.connect(host="localhost", username="root", password="", database="mywork")
                    my_cursor=conn.cursor()
                    sql="update person set name=%s,fam=%s, photosample=%s where id=%s"
                    val=(
                        self.var_name.get(),
                        self.var_fam.get(),
                        self.var_image.get(),
                        self.var_id.get()
                    )
                    my_cursor.execute(sql,val)
                else:
                    if not update:
                        return

                messagebox.showinfo("Succes","Person deteails successfly update complated", parent=self.root)
                conn.commit()
                self.fetch_data()
                conn.close()           
            except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}" )

   #================== function delete=================================
   # 
    def delete_data(self):
        if self.var_id.get()=="":
            messagebox.showerror("Error","Person id must be required", parent=self.root)
        else:
            try:
                delete=messagebox.askyesno("Person delete page", "Do you want delete this person", parent=self.root)
                if delete>0:
                    conn=mysql.connector.connect(host="localhost", username="root", password="", database="mywork")
                    my_cursor=conn.cursor()
                    sql="delete from person where id=%s"
                    val=(self.var_id.get(),)
                    my_cursor.execute(sql,val)
                else:
                    if not delete:
                        return
                
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Delete","Successfully deleted person details", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}" )

    def reset_data(self):
        self.var_id.set("")
        self.var_image.set("")
        self.var_name.set("")


#===================Generate data set or take photo Smaple===========================

   

if __name__=="__main__":
    root=Tk()   
    obj=Addcamera(root)
    root.mainloop()
