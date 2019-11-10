import tkinter as tk
root = tk.Tk()
root.geometry('720x400')
screen = tk.Canvas(root,height=400,width=720,bg='#000000')
screen.grid()


def update():
    global n
    n=0
    screen.create_arc(30, 110, 130,200, start=320, extent=2.60*n,fill='white')

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
            )
            class Digit:
                def __init__(self, canvas,length,width, x=20, y=20):
                    self.canvas = canvas
                    l = length
                    self.segs = []
                    for x0, y0, x1, y1 in offsets:
                        self.segs.append(canvas.create_line(
                            x + x0*l, y + y0*l, x + x1*l, y + y1*l,fill='#1B2631',
                            width = width))
            def show(self, num):
                for iid, on in zip(self.segs, digits[num]):
                    self.canvas.itemconfigure(iid, fill='#00FF00' if on else '#1B2631')          
                    

            def _create_circle(self, x, y, r, **kwargs):
                return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
            tk.Canvas.create_circle = _create_circle

            """def _create_circle_arc(self, x, y, r, **kwargs):
                if "start" in kwargs and "end" in kwargs:
                    kwargs["extent"] = kwargs["end"] - kwargs["start"]
                    del kwargs["end"]
                return self.create_arc(x-r, y-r, x+r, y+r, **kwargs)
            tk.Canvas.create_circle_arc = _create_circle_arc"""


            screen.create_circle(350,190,100, outline="#D3D3D3", width=8)

            screen.create_text(350,260 ,fill='#D3D3D3',text='Km/hr',font='comic 20')
            #screen.create_text(350,280 ,fill='#D3D3D3',text='boom baby,lets go',font='comic 11')

            '''screen.create_line(200,0,200,400, fill='grey')
            screen.create_line(0,134,180,134, fill='grey')
            screen.create_line(0,269,245,269, fill='grey')'''

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

                return screen.create_polygon(points, **kwargs, smooth=False)

            my_rectangle = round_rectangle(30,180, 130,380, radius=20, outline="#D3D3D3",width=8,fill ='')
            my_rectangle1 = round_rectangle(60,160, 100,180, radius=20, outline="#D3D3D3",width=8,fill ='#D3D3D3')



            #l=label(root,text='KM/H').place(x=100,y=100)

            batD1= Digit(screen,20,5,55,95)
            batD2= Digit(screen,20,5,85,95)

            dig = Digit(screen,40,10, 300, 140) ##
            dig1 = Digit(screen,40,10, 360, 140) ##
            

        
        
        dig.show(n//10)

        screen.create_arc(30, 110, 130,200, start=320, extent=2.60*n,fill='white')
        dig1.show(n%10) ## Control what you want to show here , eg (n+1)%10

        if n>=50:
            filler='green'
        elif n<50 and n>25:
            filler ='yellow'
        else:
            filler='red' 
        
        screen.create_rectangle(36,(373-1.87*n),123,373,fill=filler)

        screen.create_rectangle(656,367-n*3,690,367,fill='yellow')
        

        batD1.show(n//10)
        batD2.show(n%10)

        n = (n+1)
        root.after(50, update)
root.after(50, update)
root.mainloop()