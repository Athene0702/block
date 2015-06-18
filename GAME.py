# -*- coding: utf-8 -*-
"""
Created on Mon May 18 22:45:57 2015

@author: PinYi
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.animation as animation

# initial all graphical objects
fig = plt.figure(figsize=(16,9), dpi=100)
ax = plt.axes(xlim=(0,+2), ylim=(0,+1))
plt_tx_center = ax.text(1.0, 0.25, '', fontsize = 40, color='#FF00A2', ha='center', va='center')
plt_score = ax.text(1.93, 0.05, '', fontsize = 20, color='#FF00A2', ha='right', va='baseline')
ball_rad=0.02
#global parameters
ref_speed = 0.05 # 0.05 per frame
h=0.05
w=0.25
total_block_x=int(round(2./w))
total_block_y=int(round((1-0.4)/h))

def level(i):    #returns an array of blocktypes and their hps
    global h,w,total_block_x,total_block_y

    if i==1:        
        level_1=np.random.rand(total_block_x,total_block_y)*2
        array_of_blocktype =level_1.astype(int)
    if i==2:      
        level_2=np.random.rand(total_block_x,total_block_y)*3
        array_of_blocktype =level_2.astype(int)
    if i==3:
        level_2=np.random.rand(total_block_x,total_block_y)*4
        array_of_blocktype =level_2.astype(int)
    if i==4:
        level_4=np.random.rand(total_block_x,total_block_y)*5
        array_of_blocktype =level_4.astype(int)

    return array_of_blocktype

#move the board by dragging
class DraggableRectangle:
    def __init__(self, rect):
        self.rect = rect
        self.press = None

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.rect.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.rect.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.rect.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        'on button press we will see if the mouse is over us and store some data'
        if event.inaxes != self.rect.axes: return
        contains, attrd = self.rect.contains(event)
        x0, y0 = self.rect.xy
        self.press = x0, y0, event.xdata, event.ydata

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        if self.press is None: return
        if event.inaxes != self.rect.axes: return
        x0, y0, xpress, ypress = self.press
        dx = event.xdata - xpress
        self.rect.set_x(x0+dx)
        self.rect.set_y(y0)
        self.rect.figure.canvas.draw()

    def on_release(self, event):
        'on release we reset the press data'
        self.press = None
        self.rect.figure.canvas.draw()

    def disconnect(self):
        'disconnect all the stored connection ids'
        self.rect.figure.canvas.mpl_disconnect(self.cidpress)
        self.rect.figure.canvas.mpl_disconnect(self.cidrelease)
        self.rect.figure.canvas.mpl_disconnect(self.cidmotion)

rects = ax.bar(0.7, 0.005, width=0.6, bottom=0.1,linewidth=0,color='#b880bd')

drs = []
for i in rects:
    dr = DraggableRectangle(i)
    dr.connect()
    drs.append(dr)
#############################

class Blocks:
    def __init__(self, x_init = 0.5, y_init = 1.2,type=1):
        self.x, self.y = x_init, y_init # center of mass position
        self.hp = 1 # hit points
        self.type = type # 0 - invisible, 1 - dies after one hit, 2 - dies after two hits, 3 - dies after three hits, 4 - invincble block
        self.block = None
        
    def blocktype(self,xcoord,ycoord):
        if self.type==0:#white block,background
            self.block=None
        elif self.type==1:#HP=1
            self.block=ax.add_patch(mpatches.Rectangle((xcoord-w/2, ycoord-h/2), w,h,facecolor='#03cad0',linewidth=0.5,edgecolor='#FFFFFF'))
        elif self.type==2:#HP=2
            self.block=ax.add_patch(mpatches.Rectangle((xcoord-w/2, ycoord-h/2), w,h,facecolor='#02999e',linewidth=0.5,edgecolor='#FFFFFF'))
        elif self.type==3:#HP=3
            self.block=ax.add_patch(mpatches.Rectangle((xcoord-w/2, ycoord-h/2), w,h,facecolor='#015052',linewidth=0.5,edgecolor='#FFFFFF'))
        elif self.type==4:#UNDYING
            self.block=ax.add_patch(mpatches.Rectangle((xcoord-w/2, ycoord-h/2), w,h,facecolor='#7a7a7a',linewidth=0.5,edgecolor='#FFFFFF'))

        return self.block
    
    def eval_collision(self, obj): # collision detection, only consider the center of obj hitting the square box from self center
        if self.type>=1:
            if abs(obj.x-self.x)<=w/2 and abs(obj.y-self.y)<=(h/2+ball_rad): ##collision with long side
                return 1           ##may be erroneous
            elif abs(obj.x-self.x)<=(w/2+ball_rad)and abs(obj.y-self.y)<=h/2:   ##collision with short side
                return 2
                
class Ball():
    global ball_rad    
    def __init__(self):
        self.x=1.0                    #x position
        self.y=0.05                   #y position
        self.speed=ref_speed          #ball speed
        self.angle=np.pi              #ball angle
        self.dx=0.0                  #expected x movement
        self.dy=0.0                #expected y mevement
        self.patch = None
    
    def plot(self,x,y):
        self.x = x
        self.y = y        
        self.patch = plt.Circle((x,y), radius=ball_rad, color='#d10263',linewidth=0.5,edgecolor='#00FFFF')
        return ax.add_patch(self.patch)
        
    def bounce(self):
        if self.x<=0.01 or self.x>=1.99:
            self.dx = -self.dx
            self.angle = np.arctan2(self.dy,self.dx)
            if self.x<=0.01:
                self.x=0.015
            else:
                self.x=1.985
        if self.y>=0.99:    
            self.dy = -self.dy
            self.angle = np.arctan2(self.dy,self.dx)
            self.y=0.985
        elif self.y<=0.1+ball_rad:
            X,Y=rects.patches[0].xy
            if self.x<(X+0.3) and self.x>X:
                if self.dy<0:
                    self.angle = np.pi/2+(X+0.3-self.x)*np.pi/(0.3*4)
            elif self.x<(X+0.6) and self.x>=(X+0.3):
                if self.dy<0:
                    self.angle = np.pi/2-(self.x-X-0.3)*np.pi/(0.3*4)
        self.dx = (self.speed)*np.cos(self.angle)
        self.dy = (self.speed)*np.sin(self.angle)
        
    def move(self):
        self.x += self.dx
        self.y += self.dy
        
ball=[]   ##container for balls
block=[]  ##container for blocks 
zero_count,undying_count = 0,0     #
center_message = ''
center_message_delay = 5  
ball_delay=0 
lv=1
score = 0

def init(lv):
    global zero_count,undying_count, block, score
    #initialize blocks
    for i in range(total_block_x):
        for j in range(total_block_y):
            bl = Blocks()
            bl.x = w*i+w/2
            bl.y = h*j+h/2+0.4
            bl.type=level(lv)[i][j]
            if undying_count>=10 and bl.type==4:
                bl.type=0
            bl.blocktype(bl.x,bl.y)
            block.append(bl)
            if bl.type==0:
                zero_count+=1
            elif bl.type==4:
                undying_count+=1

    plt_score.set(text='Score: '+str(score)) 
die_times=0
def animate(i):
    global center_message, center_message_delay,ball_delay
    global zero_count,undying_count,die_times,lv, score
    
    def draw_block(lv):
        global zero_count, undying_count, block
        for j in range(total_block_y):
            for i in range(total_block_x):
                bl = Blocks()
                bl.x = w*i+w/2
                bl.y = h*j+h/2+0.4
                bl.type=level(lv)[i][j]
                bl.blocktype(bl.x,bl.y)
                block.append(bl)
                if bl.type==0:
                    zero_count+=1
                elif bl.type==4:
                    undying_count+=1

        
    if len(ball)==0 and ball_delay==0 and center_message_delay==0:
        X,Y=rects.patches[0].xy        
        b = Ball()
        b.angle = np.pi/2+np.random.rand(1)[0]*2-1
        b.plot(X+0.32,Y)        
        ball.append(b)
        
    if i<=20: # display the initial message
        center_message = 'Break the blocks!'
        center_message_delay = 20
    elif i<40:
        center_message = 'Author: Pin-yi Lee & Wen-Hung Chou'
        center_message_delay = 20
    elif i==40:
        center_message = 'Go!'
        center_message_delay = 20
           
    
    for i in ball:
        for j in block:
            if j.eval_collision(i)==1:
                i.dy = -i.dy
                i.angle = np.arctan2(i.dy,i.dx)
                if j.type !=4:
                    j.type -= 1
                    j.block.remove()
                    j.blocktype(j.x,j.y)
                    if j.type==0:
                        zero_count+=1
                        score += 10
            elif j.eval_collision(i)==2:
                i.dx = -i.dx
                i.angle = np.arctan2(i.dy,i.dx)
                if j.type !=4:
                    j.type -= 1
                    j.block.remove()
                    j.blocktype(j.x,j.y)
                    if j.type==0:
                        zero_count+=1
        i.bounce()
        i.move()
        if i.y<0:
            die_times+=1
            i.patch.remove()
            ball.remove(i)
            ball_delay = 30
            center_message = 'QQAQQ, die '+str(die_times)+' times'
            center_message_delay = 15
            score-=20*die_times
        else:
            i.patch.center = (i.x, i.y)
        if zero_count==total_block_x*total_block_y-undying_count:
            ball.remove(i)
            i.patch.remove()
    if score<0:
        center_message = 'Loser! Ha! Ha! Ha!'
        center_message_delay = 999
    if zero_count==total_block_x*total_block_y-undying_count:
        if lv==4 or score > 2000:
            center_message = 'You are a genius <m(_ _)m> !!!'
            center_message_delay = 999
        else:
            center_message = 'Next level'
            center_message_delay = 30
            lv+=1
            zero_count,undying_count=0,0
            draw_block(lv)
            
    if center_message_delay>0:
        plt_tx_center.set(text=center_message)
        if center_message_delay!=999: center_message_delay -= 1
    else: plt_tx_center.set(text='')       
    
    if ball_delay>0:
        ball_delay -= 1
    
    plt_score.set(text='Score: '+str(score))

# main animation function call
anim = animation.FuncAnimation(fig, animate, init_func=init(lv), interval=20)

# plt.tight_layout()
plt.show()
