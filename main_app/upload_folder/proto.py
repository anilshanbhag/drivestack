from Tkinter import *
import math

root = Tk()
root.title('Self-Balancing Arm Bot')
root.geometry('1350x650+0+0')
v=IntVar()
l=500


def givedetail():
     va=v.get()
     for i in A:
          if va==i[0]:
               break
     label1=Label(root,text='                                                                                                                                                               ').place(x=100,y=100)
     label1=Label(root,text=towrite(i),font='Palatino').place(x=150,y=70)  
     
def towrite(i):
     write='Angle between vertical and lower arm is  '+str(i[0])+'*  while that between upper arm and lower arm is  '+str(i[1]+90-i[0])+'*'
     return write
label=Label(root,text='This is the locus of the tip of the bot. Select a point to get further details',font='Palatino').pack()
button=Button(root,text='Get details',command=givedetail).pack()

A=[[i] for i in xrange(-30,31)]
for i in A :
     i.append(int(math.degrees(math.acos(2*math.sin(math.radians(i[0]))))))
     i.append(int(l*math.sin(math.radians(i[0]))))
     i.append(int(l*math.cos(math.radians(i[0]))))
     i.append(int(-l*math.sin(math.radians(i[0]))))
     i.append(int((l*math.cos(math.radians(i[0])))+l/2*(math.sin(math.radians(i[1])))))

for i in A:
     Radiobutton(root, variable=v, value=i[0],relief='flat').place(x=650+2*i[4],y=-1*i[5]+900)
mainloop()
