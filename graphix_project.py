from graphix import Circle,Window,Point,Line,Rectangle,Text,Polygon
import time
import math
patch_size = 100
box_size=20
box_half=10
radius=5


def draw_circle(win, centre, radius, colour):
    circle = Circle(centre, radius)
    circle.fill_colour = colour
    circle.outline_colour=colour
    circle.draw(win)
    return circle
    
    
def draw_plain_patch(win,tp_x,tp_y,colour,shapes):
    for y in range(tp_y,tp_y+patch_size,box_size):
        for x in range(tp_x,tp_x+patch_size,box_size):
            rec=Rectangle(Point(x,y),Point(x+box_size,y+box_size))
            rec.fill_colour=colour
            rec.outline_colour=colour
            rec.draw(win)
            shapes[(x,y)]=[rec]
            
            
def draw_patch_0(win,tp_x,tp_y,colour,shapes):
    text="hi!"
    size=8
    for y in range(tp_y,tp_y+patch_size,box_size):
        for x in range(tp_x,tp_x+patch_size,box_size):
            top_left=Point(x,y)
            bot_right=Point(x+box_size,y+box_size)
            square=Rectangle(top_left,bot_right)
            msg=Text(Point(x+box_half,y+box_half),text)
            msg.size=size
            square.outline_colour=colour
            msg.outline_colour=colour
            square.draw(win)
            msg.draw(win)
            shapes[(x,y)]=[square,msg]
            
            
def draw_patch_3(win,tp_x,tp_y,colour,shapes):
    even_row=False
    for y in range(tp_y,tp_y+patch_size,box_size):
        even_row=not even_row
        even_col=False
        for x in range(tp_x,tp_x+patch_size,box_size):
            centre=Point(x+box_half,y+box_half)
            if even_row:
                rec=Rectangle(Point(x,y),Point(x+box_size,y+box_size))
                rec.fill_colour=colour
                rec.outline_colour=colour
                rec.draw(win)
                circle=draw_circle(win, centre, radius,"white")
                shapes[(x,y)]=[rec,circle]
            else:
                even_col=not even_col
                centre=Point(x+box_half,y+box_half)
                if even_col:
                    points=[Point(x,y+box_half),Point(x+box_half,y),Point(x+box_size,y+box_half),Point(x+box_half,y+box_size)]
                    pol=Polygon(points)
                    pol.fill_colour=colour
                    pol.outline_colour=colour
                    pol.draw(win)
                    circle=draw_circle(win, centre, radius,"white")
                    shapes[(x,y)]=[pol,circle]
                else:
                    circle=draw_circle(win, centre, radius,colour)
                    shapes[(x,y)]=[circle]
                
                    
def get_inputs():
    in_colours=["","",""]
    sizes=["5","7","9"]
    colours=["red","green", "blue", "magenta","orange","purple"]
    for i in range(len(in_colours)):
        colour=input(f"Enter colour {i+1} for design: ")
        while (colour not in colours) or (colour in in_colours):
            if colour not in colours:
                colour=input("You have inputed an invalid colour.Please select from colours red, green, blue, magenta,orange or purple: ")
            elif colour in in_colours:
                colour=input("You have already picked this colour.Please select another one: ")
        in_colours[i]=colour
    win_size=input("Enter size for window(5,7,9): ")
    while win_size not in sizes:
        win_size=input("Select ONLY from sizes 5,7,9: ")
    return in_colours,int(win_size)

def get_colour(in_colours,window_size,x,y):
    if x==0 or y==0 or x==window_size-patch_size or y==window_size-patch_size:
        return in_colours[0]
    elif x+y<window_size:
        return in_colours[1]
    elif x+y>=window_size:
        return in_colours[2]
    
def get_patch(window_size,x,y):
    if y%200==0:
        even_row=True
    else:
        even_row=False
    if (y==0 or y==window_size-patch_size) or \
    ((x==0 or x==window_size-patch_size) and even_row==True):
        patch_type="f"
    elif even_row==True and x+y<window_size:
        patch_type="p"
    elif even_row==True and x+y>=window_size:
        patch_type="f"
    else:
        patch_type="plain"
    return patch_type
    

def patchwork(win,in_colours,window_size,empty_spots,shapes):#/get_colour/get_patch
    for y in range(0,window_size,patch_size):#just keep the row and do %200 instead of 2 later on
        for x in range(0,window_size,patch_size):
            colour=get_colour(in_colours,window_size,x,y)
            patch=get_patch(window_size,x,y)
            if patch=="f":
                draw_patch_0(win,x,y,colour,shapes)
            elif patch=="p":
                draw_patch_3(win,x,y,colour,shapes)
            else:
                draw_plain_patch(win,x,y,colour,shapes)
            empty_spots[(x,y)]=False   


def draw_line(win,p1,p2):
    line=Line(p1,p2)
    line.outline_width=8
    line.draw(win)
    return line


def undraw_border(win,lines):
    for line in lines:
        line.undraw()
    lines.clear()


def create_border(win,top_left,top_right,bot_left,bot_right,lines):
    line_1=draw_line(win,top_left,top_right)
    line_2=draw_line(win,top_left,bot_left)
    line_3=draw_line(win,bot_left,bot_right)
    line_4=draw_line(win,top_right,bot_right)
    lines.append(line_1)
    lines.append(line_2)
    lines.append(line_3)
    lines.append(line_4)


def undraw_patch(win,tp_x,tp_y,empty_spots,shapes):
        for y in range(tp_y,tp_y+patch_size,box_size):
            for x in range(tp_x,tp_x+patch_size,box_size):
                for shape in shapes[(x,y)]:
                    shape.undraw()
                shapes[(x,y)].clear()
                
   


def move_patch(win,tp_x,tp_y,empty_spots,shapes,dir_x,dir_y):
    move_patch=[]
    for y in range(tp_y,tp_y+patch_size,box_size):
        for x in range(tp_x,tp_x+patch_size,box_size):
            for shape in shapes[(x,y)]:
                shapes[(x+dir_x,y+dir_y)].append(shape)
                move_patch.append(shape)
            shapes[(x,y)].clear()
            
    for i in range(5):
        time.sleep(0.08)
        for obj in move_patch:
            obj.move(dir_x//5,dir_y//5)
    move_patch.clear()         
            
            
def edit(win,window_size,lines,empty_spots,in_colours,shapes):
    select=False
    while True:
        if select==False:
            click=win.get_mouse()
            for y in range(0,window_size,patch_size):
                for x in range(0,window_size,patch_size):
                    top_left=Point(x,y)
                    top_right=Point(x+patch_size,y)
                    bot_right=Point(x+patch_size,y+patch_size)
                    bot_left=Point(x,y+patch_size)
                    if (x<=click.x<=x+100) and (y<=click.y<=y+100) and select==False:
                        patch_tl=top_left
                        patch_tr=top_right
                        patch_bl=bot_left
                        patch_br=bot_right
                        create_border(win,patch_tl,patch_tr,patch_bl,patch_br,lines)
                        select=True
        while select==True:
            key=win.get_key()
            if key=="Escape":
                undraw_border(win,lines)
                select=False
                
            if key=="x" and empty_spots[(patch_tl.x,patch_tl.y)]==False:
                undraw_patch(win,patch_tl.x,patch_tl.y,empty_spots,shapes)
                empty_spots[(patch_tl.x,patch_tl.y)]=True
                
            if (key=="1" or key=="2" or key=="3") \
            and empty_spots[(patch_tl.x,patch_tl.y)]==True:
                colour=int(key)-1
                undraw_border(win,lines)
                draw_patch_3(win,patch_tl.x,patch_tl.y,in_colours[colour],shapes)
                create_border(win,patch_tl,patch_tr,patch_bl,patch_br,lines)
                empty_spots[(patch_tl.x,patch_tl.y)]=False
                        
            elif (key=="4" or key=="5" or key=="6") \
            and empty_spots[(patch_tl.x,patch_tl.y)]==True:
                colour=int(key)-4
                undraw_border(win,lines)
                draw_patch_0(win,patch_tl.x,patch_tl.y,in_colours[colour],shapes)
                create_border(win,patch_tl,patch_tr,patch_bl,patch_br,lines)
                empty_spots[(patch_tl.x,patch_tl.y)]=False
            
            elif (key=="7" or key=="8" or key=="9") \
            and empty_spots[(patch_tl.x,patch_tl.y)]==True:
                colour=int(key)-7
                undraw_border(win,lines)
                draw_plain_patch(win,patch_tl.x,patch_tl.y,in_colours[colour],shapes)
                create_border(win,patch_tl,patch_tr,patch_bl,patch_br,lines)
                empty_spots[(patch_tl.x,patch_tl.y)]=False
                
            if empty_spots[(patch_tl.x,patch_tl.y)]==False:     
                if key=="Up" and patch_tl.y-patch_size>=0 and empty_spots[(patch_tl.x,patch_tl.y-patch_size)]==True:
                    move_patch(win,patch_tl.x,patch_tl.y,empty_spots,shapes,0,-patch_size)
                    empty_spots[(patch_tl.x,patch_tl.y)]=True
                    empty_spots[(patch_tl.x,patch_tl.y-patch_size)]=False
                
                elif key=="Down" and patch_tl.y+patch_size<=window_size-patch_size and empty_spots[(patch_tl.x,patch_tl.y+100)]==True:
                    move_patch(win,patch_tl.x,patch_tl.y,empty_spots,shapes,0,patch_size)
                    empty_spots[(patch_tl.x,patch_tl.y)]=True
                    empty_spots[(patch_tl.x,patch_tl.y+patch_size)]=False
                
                elif key=="Left" and patch_tl.x-patch_size>=0 and empty_spots[(patch_tl.x-patch_size,patch_tl.y)]==True:
                    move_patch(win,patch_tl.x,patch_tl.y,empty_spots,shapes,-patch_size,0)
                    empty_spots[(patch_tl.x,patch_tl.y)]=True
                    empty_spots[(patch_tl.x-patch_size,patch_tl.y)]=False
                
                elif key=="Right" and patch_tl.x+patch_size<=window_size-patch_size and empty_spots[(patch_tl.x+patch_size,patch_tl.y)]==True:
                    move_patch(win,patch_tl.x,patch_tl.y,empty_spots,shapes,patch_size,0)
                    empty_spots[(patch_tl.x,patch_tl.y)]=True
                    empty_spots[(patch_tl.x+patch_size,patch_tl.y)]=False
                
                
def main():
    lines=[]
    empty_spots={}
    shapes={}
    in_colours,win_size=get_inputs()
    win_size=win_size*patch_size
    win=Window("",win_size,win_size)
    patchwork(win,in_colours,win_size,empty_spots,shapes)
    edit(win,win_size,lines,empty_spots,in_colours,shapes)
    

main()

