# programme scrolling fichier texte (TRON)
# version 19

import curses
import time
import sys

window_larger=43 # taille de la newwin -2 
window_height=24
map_size_larger=100 # nb de colonne de la carto, on pourrait le calculer auto
map_size_height=50  # nb de ligne de la carto, on pourrait le calculer auto

# lecture de la map
# il faudrait verifier dans la carto que chaque ligne possede le meme nb de chr
f = open('map1.txt','r')
map = f.readlines()
f.close()

curses.initscr()
win = curses.newwin(25,46,0,0) # line, row, coord X,Y
curses.curs_set(0) # delete the cursor
curses.start_color()
win.border(0)
win.keypad(1) # you can use special keys like KEY_UP...
win.nodelay(1) 
curses.init_pair(1,curses.COLOR_WHITE,curses.COLOR_GREEN)

def ShowMap(line, row) : # affiche la map aux coord (line,row)
	for i in range(1,window_height) :
		mystring=map[i-2+line][row-1:row+window_larger]
		win.addstr(i,1,mystring)
		if "1" in mystring :
			# la chaine contient un O
			j=0
			for chr in mystring :
				j=j+1
				if chr in "1" :
					win.addstr(i, j, " ", curses.color_pair(1))

def CreateCursor(line, row) : # enregistre la moto dans la map (line,row)
	map_line = map[line-1]
	current_chr = map_line[row-1]
	map_line=map_line[0:row-1]+"1"+map_line[row:map_size_larger]
	map[line-1]=map_line
	return current_chr

# init des valeurs pour positionner la moto
y=20  # line (moto)
x=20 # row (moto)

direction=1
# variable direction
# 1=UP 2=RIGHT 3=DOWN 4=LEFT

while 1: # main loop	
	
	sleeptime=0.100 # init de la vitesse (100ms)
	key = win.getch() # quelle touche on appuie ?
	if key == 27: break # if ESC key => quit
	if key == curses.KEY_UP : direction=1
	if key == curses.KEY_RIGHT : direction=2
	if key == curses.KEY_LEFT : direction=4
	if key == curses.KEY_DOWN : direction=3
	if key == ord('w') : sleeptime=0.030 # touche W => accelerateur
	
	# gestion des depassement de la carte
	if y < 1 : y=map_size_height
	if y > map_size_height : y=1
	if x < 1 : x=map_size_larger
	if x > map_size_larger : x=1
	
	current = CreateCursor(y,x)
	if current != " " :
		print "GAME OVER" # collision !!
		break 
	
	map_y=y-11
	if map_y<1 : map_y=1
	if map_y>map_size_height-window_height+2 : map_y=map_size_height-window_height+2
	map_x=x-20
	if map_x<1 : map_x=1
	if map_x>map_size_larger-window_larger : map_x=map_size_larger-window_larger
	
	ShowMap(map_y,map_x)
	win.addstr(0, 30, "Y="+str(y)) # affichage de Y
	win.addstr(0, 36, "X="+str(x)) # affichage de X
	win.refresh() # on affiche tout
	time.sleep(sleeptime)
	
	if direction == 1 :
		y=y-1
	if direction == 2 :
		x=x+1
	if direction == 3 :
		y=y+1
	if direction == 4 :
		x=x-1
	
