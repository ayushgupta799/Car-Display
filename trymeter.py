# trymeter.py
# test program to try out the meter class
import tkinter as tk
import meter as m

class Meterframe(tk.Frame):
	def __init__(self,master,text = '',scale=(0,100),*args,**kwargs):
		tk.Frame.__init__(self,master,*args,**kwargs)
		
		width = kwargs.get('width',100)
		self.meter = m.Meter(self,height = width,width = width)
		self.meter.setrange(scale[0],scale[1])
		self.meter.pack()
		
		tk.Label(self,text=text).pack()
		
		tk.Scale(self,length = width,from_ = scale[0], to = scale[1]
		,orient = tk.HORIZONTAL
		,command = self.setmeter).pack()
		
	def setmeter(self,value):
		value = int(value)
		self.meter.set(value)
		
class Mainframe(tk.Frame):
	def __init__(self,master,*args,**kwargs):
		tk.Frame.__init__(self,master,*args,**kwargs)
		
		Meterframe(self,text = 'Meter1',width = 200).grid(row = 0,column = 0)
		Meterframe(self,text = 'Meter2',width = 200,scale = (-50,50)).grid(row = 0,column = 1)
				
		tk.Button(self,text = 'Quit',width = 15,command = master.destroy) \
		.grid(row = 1,column = 0)

class App(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		
		self.title('Try Meter')
	
		Mainframe(self).pack()
		
App().mainloop()