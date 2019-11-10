import tkinter as tk
root = tk.Tk()
root.geometry('720x400')
screen = tk.Canvas(root,height=400,width=720,bg='#000000')
screen.grid()

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
    (1, 1, 1, 0, 1, 1, 0),  # N
    (1, 1, 1, 1, 1, 0, 1),  # a
    (0, 0, 1, 1, 1, 1, 1),  # b
    (1, 0, 1, 1, 1, 1, 1),  # c
    (0, 0, 1, 0, 1, 0, 1),  # n
    (1, 1, 1, 0, 1, 1, 1),  # A
)
class Digit:
    def __init__(self, canvas,length,width, x=20, y=20):
        self.canvas = canvas
        l = length
        self.segs = []
        for x0, y0, x1, y1 in offsets:
            self.segs.append(canvas.create_line(
                x + x0*l, y + y0*l, x + x1*l, y + y1*l,fill='#1A0611',
                width = width))
    def show(self, num,fil):
        for iid, on in zip(self.segs, digits[num]):
            self.canvas.itemconfigure(iid, fill=fil if on else '#1A0611')          

screen.create_line(480,0,480,720,width='2',fill='grey')
#batery temp area
screen.create_rectangle(480,0,720,200,fill='grey',outline='')
screen.create_text(599,15+30,text='Temp °C',font='helvetica 22 bold',fill='black')
screen.create_text(545,44+60,text='Motor',font='helvetica 20 italic',fill='black')
screen.create_text(552,73+80,text='Battery',font='helvetica 20 italic',fill='black')


#voltage area
screen.create_rectangle(480,200,720,400,fill='',outline='')
screen.create_text(599,216,text='Battery Voltage (V)',font='helvetica 19 bold',fill='grey')
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
my_rectangle = round_rectangle(29,88, 111,380, radius=20, outline="#00ff00",width=8,fill ='')
my_rectangle1 = round_rectangle(57,70,83,80, radius=7, outline="#D3D3D3",width=2,fill ='#D3D3D3')

#for temp circles
screen.create_oval(483,34+60,503,54+60,outline='grey',fill='red')
screen.create_oval(483,62+80,503,82+80,outline='grey',fill='orange')

#battery digits
batD1= Digit(screen,20,5,37,18) #ones place
batD2= Digit(screen,20,5,72,18) #tens place
screen.create_text(110,52 ,fill='#00ff00',text='%',font='comic 17 bold')


#speed digits
dig = Digit(screen,45,13, 300, 140) ##ones place
dig1 = Digit(screen,45,13, 375, 140) ##tens place

g=1
n = 0
def update():
    global n
    dig.show(10,'#00ff00')

    #screen.create_arc(30, 110, 130,200, start=320, extent=2.60*n,fill='white')
    dig1.show(11,'#00ff00') ## Control what you want to show here , eg (n+1)%10

    if n>=50 and n<100:
        filler='#22ff00'
    elif n<50 and n>25:
        filler ='yellow'
    else:
        filler='red' 
    
    screen.create_rectangle(36,370-(n*2.75),103,370,fill=filler)
    #making bars trying
    #creen.create_rectangle(656,367-n*3,690,367,fill='yellow')
    #screen.create_rectangle(600,367-n*2,634,367,fill='blue')    

    #rpm=
    screen.create_rectangle(270,305,450,345,fill='#D3D3D3',outline='')
    x=52.3
    screen.create_text(360,325 ,fill='RED',text='RPM   '+(str)("%0.0f" % (4500*x/52.3)),font='comic 18 bold')

    screen.create_line(34,116.2,106,116.2,width=7,fill='black',smooth='True')
    screen.create_line(34,116+(28.2*1),106,116+(28.2*1),width=7,fill='black',smooth='True')
    screen.create_line(34,116+(28.2*2),106,116+(28.2*2),width=7,fill='black',smooth='True')
    screen.create_line(34,116+(28.2*3),106,116+(28.2*3),width=7,fill='black',smooth='True')
    screen.create_line(34,116+(28.2*4),106,116+(28.2*4),width=7,fill='black',smooth='True')
    screen.create_line(34,116+(28.2*5),106,116+(28.2*5),width=7,fill='black',smooth='True')
    screen.create_line(34,116+(28.2*6),106,116+(28.2*6),width=7,fill='black',smooth='True')
    screen.create_line(34,116+(28.2*7),106,116+(28.2*7),width=7,fill='black',smooth='True')
    screen.create_line(34,116+(28.2*8),106,116+(28.2*8),width=7,fill='black',smooth='True')


    screen.create_text(630,44+60,text='75°',font='helvetica 20 italic bold',fill='black')
    screen.create_text(630,73+80,text='45°',font='helvetica 20 italic bold',fill='black')

    batD1.show(10,'#00ff00')
    batD2.show(11,'#00ff00')

    vl1.show(0,'#D3D3D3')
    vl2.show(0,'#D3D3D3')
    vl3.show(0,'#D3D3D3')

    if(n+1 < 100):
        n = (n+1)
    root.after(90, update)
root.after(90, update)
root.mainloop()
