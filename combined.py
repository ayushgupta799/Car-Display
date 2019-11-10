#import RPi.GPIO as GPIO
import tkinter as tk
import time, math
import datetime
from time import sleep
#from w1thermsensor import W1ThermSensor

#sensorT = W1ThermSensor()
#sensorT @ GPIO 4 or pin7
sensorH=8
root = tk.Tk()
root.geometry('800x400')
screen = tk.Canvas(root,height=400,width=800,bg='#000000')
screen.grid()
# GPIO.setmode(GPIO.BOARD)
# GPIO.setwarnings(False)
# GPIO.setup(sensorH , GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.add_event_detect(sensorH, GPIO.FALLING, callback=detectSensor, bouncetime=200)
start = round(time.time(),3)

offsets = (
    (0, 0, 1, 0),  # top
    (1, 0, 1, 1),  # upper right
    (1, 1, 1, 2),  # lower right
    (0, 2, 1, 2),  # bottom
    (0, 1, 0, 2),  # lower left
    (0, 0, 0, 1),  # upper left
    (0, 1, 1, 1),  # middle
)
# Segments used for each digit; 0, 1 = off, on.
digits = (
    (1, 1, 1, 1, 1, 1, 0),  # 0
    (0, 1, 1, 0, 0, 0, 0),  # 1
    (1, 1, 0, 1, 1, 0, 1),  # 2
    (1, 1, 1, 1, 0, 0, 1),  # 3
    (0, 1, 1, 0, 0, 1, 1),  # 4
    (1, 0, 1, 1, 0, 1, 1),  # 5
    (1, 0, 1, 1, 1, 1, 1),  # 6
    (1, 1, 1, 0, 0, 0, 0),  # 7
    (1, 1, 1, 1, 1, 1, 1),  # 8
    (1, 1, 1, 1, 0, 1, 1),  # 9
#    (1, 1, 1, 0, 1, 1, 0),  # N
#    (1, 1, 1, 1, 1, 0, 1),  # a
#    (0, 0, 1, 1, 1, 1, 1),  # b
#    (1, 0, 1, 1, 1, 1, 1),  # c
#    (0, 0, 1, 0, 1, 0, 1),  # n
#    (1, 1, 1, 0, 1, 1, 1),  # A
)
class Digit:
    def __init__(self, canvas,length,width, x=20, y=20):
        self.canvas = canvas
        l = length
        self.segs = []
        for x0, y0, x1, y1 in offsets:
            self.segs.append(canvas.create_line(
                x+ x0*l, y + y0*l, x + x1*l, y + y1*l,fill='#1A0611',
                width = width))
    def show(self, num,fil):
        for iid, on in zip(self.segs, digits[num]):
            self.canvas.itemconfigure(iid, fill=fil if on else '#1A0611')          

screen.create_line(480,0,480,720,width='2',fill='grey')
#batery temp area
#screen.create_rectangle(480,0,720,200,fill='grey',outline='')
#screen.create_text(599,15+30,text='Temp °C',font='helvetica 22 bold',fill='black')
screen.create_text(545,44+60,text='Motor',font='helvetica 20 italic',fill='black')
screen.create_text(552,73+80,text='Battery',font='helvetica 20 italic',fill='black')


#voltage area
#screen.create_rectangle(480,200,720,400,fill='',outline='')
#screen.create_text(599,216,text='Battery Voltage (V)',font='helvetica 19 bold',fill='grey')
vl1= Digit(screen,22,6,550,238+60) #ones place
vl2= Digit(screen,22,6,550+34,238+60) #tens place
screen.create_text(660,272+60,text='v',font='times 22',fill='white')
vl3= Digit(screen,22,5,550+74,238+60) #decimal


#circling the speed
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle
#actual creating circle
screen.create_circle(360,190,110, outline="#00ff00", width=12)
screen.create_circle(615,280+60,3.3,fill="white")

#text for kmph
screen.create_text(360,260 ,fill='#D3D3D3',text='Km/h',font='comic 18 bold')
#screen.create_text(350,280 ,fill='#D3D3D3',text='boom baby,lets go',font='comic 11')

#curved edge rectangle
def round_rectangle(x1, y1, x2, y2, radius=25, **kwargs):

    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]

    return screen.create_polygon(points, **kwargs, smooth=True)

#battery box
my_rectangle = round_rectangle(750,5,790,25, radius=5, outline="#D3D3D3",width=3,fill ='')
my_rectangle1 = round_rectangle(790,11,794,19, radius=2, outline="#D3D3D3",width=2,fill ='#D3D3D3')

#for temp circles
screen.create_oval(483,34+60,503,54+60,outline='grey',fill='red')
screen.create_oval(483,62+80,503,82+80,outline='grey',fill='orange')

#battery digits
batD1= Digit(screen,8,3,717,5) #ones place
batD2= Digit(screen,8,3,729,5) #tens place
screen.create_text(742,19 ,fill='#D3D3D3',text='%',font='comic 10 bold')


#speed digits
dig = Digit(screen,45,13, 300, 140) ##ones place
dig1 = Digit(screen,45,13, 375, 140) ##tens place

g=1
n = 0
# speed prog starts
def calculateSpeed(r_cm):
    global start,x,done
    done = round(time.time(),3)
    elapsed = done - start
    #elaspesedMinute = elapsed*0.01666668
    rpm = 1/elapsed * 60
    distance = 2*3.14159*r_cm
    speed = distance/elapsed
    speedK = speed*0.036
    #print (done,start)
    x = int((round(speedK)))
    dig.show(x//10,'#00ff00')
    #screen.create_arc(30, 110, 130,200, start=320, extent=2.60*n,fill='white')
    dig1.show(x%10,'#00ff00')
    #print (round(speedKmh,2))
    start = done

def detectSensor(channel):
    # Called if sensor output changes
    timestamp = round(time.time(),3)
    #stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
    if not GPIO.input(channel):
        calculateSpeed(15)
#digital_clock
def clock():
    screen.create_rectangle(630,0,710,25,fill='red',outline='')
    ctime=time.strftime('%H:%M')
    screen.create_text(670,12,text=ctime,font='helvetica 20 italic bold',fill='#D3D3D3')

#GPIO.add_event_detect(sensorH, GPIO.FALLING, callback=detectSensor)
def update():
    global n
    
    #GPIO.add_event_detect(sensorH, GPIO.FALLING, callback=detectSensor)
    #detectSensor(sensorH)
    #x=int(calculateSpeed(20))
    #print (done)
    #print (start)
    #print (x)
    #start = time.time()
    #dig.show(x//10,'#00ff00')

    #screen.create_arc(30, 110, 130,200, start=320, extent=2.60*n,fill='white')
    #dig1.show(x%10,'#00ff00') ## Control what you want to show here , eg (n+1)%10

    if n>=50 and n<=100:
        filler='#22ff00'
    elif n<50 and n>25:
        filler ='yellow'
    else:
        filler='red' 
    clock()
    screen.create_rectangle(753,8,749+(99*0.38),23,fill='#D3D3D3',outline='')
    screen.create_rectangle(270,305,450,345,fill='#D3D3D3',outline='')
    
    screen.create_text(360,325 ,fill='RED',text='RPM   '+(str)("%0.0f" % (4500*21/52.3)),font='comic 18 bold')

    #ppp = sensorT.get_temperature()
    screen.create_rectangle(585,85,700,115,fill='grey',outline='')
    #screen.create_text(630,44+60,text=str("{0:0.1f}".format(ppp))+'°',font='helvetica 20 italic bold',fill='black')
    
    screen.create_text(630,73+80,text='45°',font='helvetica 20 italic bold',fill='black')

    batD1.show(0,'#D3D3D3')
    batD2.show(0,'#D3D3D3')

    vl1.show(0,'#D3D3D3')
    vl2.show(0,'#D3D3D3')
    vl3.show(0,'#D3D3D3')

    
    #print('rpm:{0:.0f}-RPM kmh:{1:.0f}-KMH dist_meas:{2:.2f}m pulse:{3}'.format(rpm,km_per_hour,dist_meas,pulse))
    
    root.after(50, update)
    
root.after(50, update)
root.mainloop()
