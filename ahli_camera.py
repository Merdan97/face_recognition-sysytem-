import cv2
import tkinter
import PIL.Image, PIL.ImageTk
import time
import threading
import mysql.connector
from camera_add import Addcamera
from tkinter import ttk
from tkinter import*


class MyVideoCapture():

    def __init__(self, video_source=0, width=None, height=None, fps=None):
    
        self.video_source = video_source
        self.width = width
        self.height = height
        self.fps = fps
        
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("[MyVideoCapture] Unable to open video source", video_source)

        # Get video source width and height
        if not self.width:
            self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))    # convert float to int
        if not self.height:
            self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))  # convert float to int
        if not self.fps:
            self.fps = int(self.vid.get(cv2.CAP_PROP_FPS))  # convert float to int

        # default value at start        
        self.ret = False
        self.frame = None
        
        self.convert_color = cv2.COLOR_BGR2RGB
        #self.convert_color = cv2.COLOR_BGR2GRAY
        self.convert_pillow = True
        
        # default values for recording        
        self.recording = False
        self.recording_filename = 'output.mp4'
        self.recording_writer = None
        
        # start thread
        self.running = True
        self.thread = threading.Thread(target=self.process)
        self.thread.start()
        
    def start_recording(self, filename=None):
        if self.recording:
            print('[MyVideoCapture] already recording:', self.recording_filename)
        else:
            # VideoWriter constructors
            #.mp4 = codec id 2
            if filename:
                self.recording_filename = filename
            else:
                self.recording_filename = time.strftime("%Y.%m.%d %H.%M.%S", time.localtime()) + ".avi"
            #fourcc = cv2.VideoWriter_fourcc(*'I420') # .avi
            #fourcc = cv2.VideoWriter_fourcc(*'MP4V') # .avi
            fourcc = cv2.VideoWriter_fourcc(*'MP42') # .avi
            #fourcc = cv2.VideoWriter_fourcc(*'AVC1') # error libx264
            #fourcc = cv2.VideoWriter_fourcc(*'H264') # error libx264
            #fourcc = cv2.VideoWriter_fourcc(*'WRAW') # error --- no information ---
            #fourcc = cv2.VideoWriter_fourcc(*'MPEG') # .avi 30fps
            #fourcc = cv2.VideoWriter_fourcc(*'MJPG') # .avi
            #fourcc = cv2.VideoWriter_fourcc(*'XVID') # .avi
            #fourcc = cv2.VideoWriter_fourcc(*'H265') # error 
            self.recording_writer = cv2.VideoWriter(self.recording_filename, fourcc, self.fps, (self.width, self.height))
            self.recording = True
            print('[MyVideoCapture] started recording:', self.recording_filename)
                   
    def stop_recording(self):
        if not self.recording:
            print('[MyVideoCapture] not recording')
        else:
            self.recording = False
            self.recording_writer.release() 
            print('[MyVideoCapture] stop recording:', self.recording_filename)
               
    
        
    def process(self):
        def draw_boundray(img, classifier, scaleFactor, minNeighbors, color,text,clf):

            #gray_image=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray_image=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            features=classifier.detectMultiScale(gray_image,scaleFactor,minNeighbors)
            
            coord=[]

            for (x,y,W,h) in features:
                cv2.rectangle(img,(x,y),(x+W,y+h),(0,255,0),3)
                id, predict=clf.predict(gray_image[y:y+h, x:x+W])
                confidence=int((100*(1-predict/300)))

                conn=mysql.connector.connect(host="localhost", username="root", password="", database="mywork")
                my_cursor=conn.cursor()

                my_cursor.execute("select  name from person  where id="+str(id))                 
                d=my_cursor.fetchone()
                d="+".join(d)
                #d=str(d)

                my_cursor.execute("select  fam from person  where id="+str(id))                 
                t=my_cursor.fetchone()
                t="+".join(t)

                q=" {0}%".format(confidence)


                if confidence>77:
                    cv2.putText(img,f"{d}" , (x,y-10),cv2.FONT_HERSHEY_COMPLEX, 1,(255,5,2),2)
                    cv2.putText(img,f"{t}" , (x,y-40),cv2.FONT_HERSHEY_COMPLEX, 1,(255,5,2),2) 
                    cv2.putText(img,f"{q}" , (x,y-70),cv2.FONT_HERSHEY_COMPLEX, 1,(255,5,2),2)                  
                    #self.mark_attendance(d,t)

                else:
                    cv2.rectangle(img,(x,y),(x+W,y+h), (0,0,255),3)
                    cv2.putText(img,"Unknown Face" , (x,y-10),cv2.FONT_HERSHEY_COMPLEX, 0.8,(255,255,255),2)   
                    #self.mark_attendance("Unknown", "")
                
                coord=[x,y,W,y]
            return coord
            

        def recognize(img,clf,faceCascade):
            coord=draw_boundray(img,faceCascade,1.1,10,(255,25,255),"Face", clf)
            return img

        yol="C:/Users/User/Desktop/facesystem/haarcascade_frontalface_default.xml"
        faceCascade=cv2.CascadeClassifier(yol)        #( "haarcascade_frontalface_default.xml")
        clf=cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")

        while self.running:
            ret,frame=self.vid.read()
            frame=recognize(frame,clf,faceCascade)
            
            if ret:
                # process image
                frame = cv2.resize(frame, (self.width, self.height))

                # it has to record before converting colors
                if self.recording:
                    self.record(frame)
                    
                if self.convert_pillow:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = PIL.Image.fromarray(frame)
            else:
                print('[MyVideoCapture] stream end:', self.video_source)
                # TODO: reopen stream
                self.running = False
                if self.recording:
                    self.stop_recording()
                break
                
            # assign new frame
            self.ret = ret
            self.frame = frame

            # sleep for next frame
            time.sleep(1/self.fps)
        
    def get_frame(self):
        return self.ret, self.frame
    
    # Release the video source when the object is destroyed
    def __del__(self):
        # stop thread
        if self.running:
            self.running = False
            self.thread.join()

        # relase stream
        if self.vid.isOpened():
            self.vid.release()
            
 
class tkCamera(tkinter.Frame):

    def __init__(self, window, text="", video_source=0, width=None, height=None):
        super().__init__(window)
        
        self.window = window
        
        #self.window.title(window_title)
        self.video_source = video_source
        self.vid = MyVideoCapture(self.video_source, width, height)

        self.label = tkinter.Label(self, text=text)
        self.label.pack()
        
        self.canvas = tkinter.Canvas(self, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()

        # Button that lets the user take a snapshot
        self.btn_snapshot = tkinter.Button(self, text="Start", command=self.start)
        self.btn_snapshot.pack(anchor='center', side='left')
        
        self.btn_snapshot = tkinter.Button(self, text="Stop", command=self.stop)
        self.btn_snapshot.pack(anchor='center', side='left')
         
        # Button that lets the user take a snapshot
        self.btn_snapshot = tkinter.Button(self, text="Snapshot", command=self.snapshot)
        self.btn_snapshot.pack(anchor='center', side='left')


        # Button that lets the user take a snapshot
        self.btn_snapshot = tkinter.Button(self, text="Add camera", command=self.addcamera)
        self.btn_snapshot.pack(anchor='center', side='left')
         
        # After it is called once, the update method will be automatically called every delay milliseconds
        # calculate delay using `FPS`
        self.delay = int(1000/self.vid.fps)

        print('[tkCamera] source:', self.video_source)
        print('[tkCamera] fps:', self.vid.fps, 'delay:', self.delay)
        
        self.image = None
        
        self.running = True
        self.update_frame()

    def start(self):
        #if not self.running:
        #    self.running = True
        #    self.update_frame()
        self.vid.start_recording()

    def stop(self):
        #if self.running:
        #   self.running = False
        self.vid.stop_recording()
    
    def snapshot(self):
        # Get a frame from the video source
        #ret, frame = self.vid.get_frame()
        #if ret:
        #    cv2.imwrite(time.strftime("frame-%d-%m-%Y-%H-%M-%S.jpg"), cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR))
        
        # Save current frame in widget - not get new one from camera - so it can save correct image when it stoped
        if self.image:
            self.image.save(time.strftime("frame-%d-%m-%Y-%H-%M-%S.jpg"))
    def addcamera(self):
        self.new_window=Toplevel(self)
        self.app=Addcamera(self.new_window)
            
    def update_frame(self):
        # widgets in tkinter already have method `update()` so I have to use different name -

        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        
        if ret:
            #self.image = PIL.Image.fromarray(frame)
            self.image = frame
            self.photo = PIL.ImageTk.PhotoImage(image=self.image)
            self.canvas.create_image(0, 0, image=self.photo, anchor='nw')
        
        if self.running:
            self.window.after(self.delay, self.update_frame)


class App:

    def __init__(self, window, window_title, video_sources):
        self.window = window

        self.window.title(window_title)
        
        self.vids = []        
        columns = 4
        for number, source in enumerate(video_sources):
            
            text, stream = source
            vid = tkCamera(self.window, text, stream, 460, 315)
            x = number % columns
            y = number // columns           
            vid.grid(row=y, column=x)
            self.vids.append(vid)
           
        
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()
    
    def on_closing(self, event=None):
        print('[App] stoping threads')
        for source in self.vids:
            source.vid.running = False
        print('[App] exit')
        self.window.destroy()

if __name__ == '__main__':     

    sources = [
        ('me', 0),        
        #('IP  camera 25', 'rtsp://admin:admin@192.168.1.25/defaultPrimary?streamType=u'),
        ('Warszawa, Poland', 'https://imageserver.webcamera.pl/rec/warszawa/latest.mp4'),
        ('Baltic See, Poland', 'https://imageserver.webcamera.pl/rec/chlopy/latest.mp4'),
        ('Mountains, Poland', 'https://imageserver.webcamera.pl/rec/skolnity/latest.mp4'),
        ('Zakopane, Poland', 'https://imageserver.webcamera.pl/rec/krupowki-srodek/latest.mp4'),
        ('Kraków, Poland', 'https://imageserver.webcamera.pl/rec/krakow4/latest.mp4'),
        ('Warszawa, Poland', 'https://imageserver.webcamera.pl/rec/warszawa/latest.mp4'),
        ('Baltic See, Poland', 'https://imageserver.webcamera.pl/rec/chlopy/latest.mp4'),
       
    ]
        
    # Create a window and pass it to the Application object
    App(tkinter.Tk(), "Tkinter and OpenCV", sources)



