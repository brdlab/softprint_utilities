# TO-DO: Add circle gcode generator with radius and centre coordinates as inputs

from datetime import datetime
import os
import time
import shutil
import math

def gcode_length(fname):
	count = 0
	with open(fname, 'r') as f1:
		for line in f1:
			count += 1
	f1.close()
	return count

def gcode_folder(fname):
	dt_string = datetime.today().strftime("%Y%m%d")
	dir_path = ".\\Generated Gcodes\\"+dt_string+"\\"
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
	if not fname=="":
		if not os.path.isfile(dir_path+fname):
			shutil.copy(fname, dir_path)
	os.chdir(dir_path)
	cur_dir = os.getcwd()
	print("Saving Gcodes to:\n", cur_dir)

def gcode_line_parse(line):
	# Line format : G1 X43.909 Y78.008 E2.11939 ; infill
	splits = line.split(' ')
	x = float(splits[1][1:])
	y = float(splits[2][1:])
	return [x,y]

def gcode_headers(fname):
	f2 = open(fname, 'w+')
	now = datetime.now()
	dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
	f2.write("; GCode generated by python script on "+dt_string+"\n")
	f2.write("\n")
	f2.write("G21 ; set units to millimeters\n")
	f2.write("G90 ; use absolute coordinates\n")
	f2.write("M82 ; use absolute distances for extrusion\n")
	f2.write("G92 E0 ; reset extrusion distance\n\n")
	f2.close()

def gcode_footers(fname, row, col, row_sep, col_sep, shape):
	f2 = open(fname, 'a+')
	f2.write("M9\n")
	f2.write("G1 Z10 F480.00\n")
	f2.write("G92 E0 ; reset extrusion distance\n")
	f2.write("G91   ;\n")
	f2.write("G90            ; absolute\n")
	f2.write("G28 X0 Y0  ; home X axis\n")
	f2.write("G92 X0 Y0 ; confirm we are at zero\n")
	f2.write("M84            ; disable motors\n")
	f2.write("M30           ; End ofprogram\n")
	f2.write("M104 S0 ; turn off temperature\n")
	f2.write("G28 X0  ; home X axis\n")
	f2.write("M84     ; disable motors\n")
	f2.write("; parameters")
	f2.write("; number of rows = "+str(row)+"\n")
	f2.write("; number of columns = "+str(col)+"\n")
	f2.write("; separation between rows = "+str(row_sep)+"\n")
	f2.write("; separation between columns = "+str(col_sep)+"\n")
	f2.write("; patterned shape = "+shape+"\n")
	f2.close()

def gcode_calc_offset(fname, x0, y0):
	f1 = open(fname, 'r+')
	key = "G1 X"
	for line in f1:
		if key in line:
			p1 = gcode_line_parse(line)
			break
		else:
			continue
	return [x0-p1[0], y0-p1[1]]
	f1.close()

def gcode_rectangle(x,y,l,w,ext_width,fname):
	n_infill = int(round(w/ext_width))
	f2 = open(fname, 'a+')
	f2.write("G1 Z10 F250.00\n")
	line = "G1 X"+str(x)+" Y"+str(y)+" F180; moving to first point\n"
	f2.write(line)
	f2.write("G1 Z0.5 F250.00\n")
	f2.write("M0; pause\n")
	f2.write("M7; start extruding\n")
	for i in range(n_infill):
		y1 = y+ext_width
		if i%2==0:
			x1 = x+l
		else:
			x1 = x-l
		line_x = "G1 X"+str(x1)+" Y"+str(y)+ " F180; infill\n"
		f2.write(line_x)
		if i<(n_infill-1):
			line_y = "G1 X"+str(x1)+" Y"+str(y1)+ " F180; infill\n"
			f2.write(line_y)
		else:
			f2.write("M9\n")
			f2.write("G1 Z10 F250.00\n")
		x = x1
		y = y1
	f2.close()

def gcode_triangle(x,y,b,h,ext_width,fname):
	n_infill = int(round(h/ext_width))
	f2 = open(fname, 'a+')
	f2.write("G1 Z10 F250.00\n")
	line = "G1 X"+str(x)+" Y"+str(y)+" F180; moving to first point\n"
	f2.write(line)
	f2.write("G1 Z0.5 F250.00\n")
	f2.write("M0; pause\n")
	f2.write("M7; start extruding\n")
	dx = (ext_width*b)/(2*h)
	for i in range(n_infill):
		y1 = y+ext_width
		if ((i+1)%2)==1:
			x1 = x+dx
			x2 = x1-(2*(i+1)*dx)
		else:
			x1 = x-dx
			x2 = x1+(2*(i+1)*dx)
		line_y = "G1 X"+str(x1)+" Y"+str(y1)+ " F180; infill\n"
		f2.write(line_y)
		line_x = "G1 X"+str(x2)+" Y"+str(y1)+ " F180; infill\n"
		f2.write(line_x)
		y = y1
		x = x2
	f2.write("M9\n")
	f2.write("G1 Z10 F250.00\n")
	f2.close()

def gcode_horseshoe(x,y,l,s,ext_width,fname):
	f2 = open(fname, 'a+')
	f2.write("G1 Z10 F250.00\n")
	line = "G1 X"+str(x)+" Y"+str(y)+" F180; moving to first point\n"
	f2.write(line)
	f2.write("G1 Z0.5 F250.00\n")
	f2.write("M0; pause\n")
	f2.write("M7; start extruding\n")
	# 3x4mm pad -> line -> perpendicular line -> line -> 3x4mm line thick pad
	for i in range(3):
		x1 = x+ext_width
		if i%2==0:
			y1 = y-2
		else:
			y1 = y+2
		line_y = "G1 X"+str(x)+" Y"+str(y1)+" F180; infill\n"
		f2.write(line_y)
		line_x = "G1 X"+str(x1)+" Y"+str(y1)+" F180; infill\n"
		f2.write(line_x)
		x = x1
		y = y1
	line_y = "G1 X"+str(x)+" Y"+str(y+4+l)+" F180; infill\n"
	f2.write(line_y)
	line_x = "G1 X"+str(x+s)+" Y"+str(y+4+l)+" F180; infill\n"
	f2.write(line_x)
	line_y = "G1 X"+str(x+s)+" Y"+str(y)+" F180; infill\n"
	f2.write(line_y)
	x = x+s
	for i in range(3):
		x1 = x+ext_width
		if i%2==0:
			y1 = y+2
		else:
			y1 = y-2
		line_x = "G1 X"+str(x1)+" Y"+str(y)+" F180; infill\n"
		f2.write(line_x)
		line_y = "G1 X"+str(x1)+" Y"+str(y1)+" F180; infill\n"
		f2.write(line_y)
		x = x1
		y = y1
	f2.close()

def gcode_offset(fname1, fname2, x, y):
	f1 = open(fname1, 'r+')
	f2 = open(fname2, 'a+')
	f2.write("G1 Z10 F250; moving to first infill point\n")
	start_key = "; start gcode"
	parse_key = "G1 X"
	stop_key = "; stop gcode"
	for line in f1:
		if parse_key in line:
			p1 = gcode_line_parse(line)
			x1 = p1[0] + x
			y1 = p1[1] + y
			new_line = "G1 X"+str(x1)+" Y"+str(y1)+" F180; infill\n"
			f2.write(new_line)
			if start_key in line:
				f2.write("G1 Z0.5 F250.00\n")
				f2.write("M0; pause\n")
				f2.write("M7; start extruding\n")
				continue
			if stop_key in line:
				f2.write("M9\n")
				f2.write("G1 Z10 F250.00\n")
				break
	f2.close()
	f1.close()

# Initial print parameters
ext_width = 0.5 # mm
n_layers = 2
x0 = 100
y0 = 100

print("Enter number of array rows:")
r = int(input())
print("Enter number of array columns:")
c = int(input())
print("Enter horizontal separation (mm):")
r_sep = float(input())
print("Enter vertical separation (mm):")
c_sep = float(input())

print("Select one standard shape to repeat or press C for your own gcode template:\n")
print("(R)ectangle \t (T)riangle \t (U)-shape \t custom (G)-code ")
choice = input().capitalize()

if choice == "R":
	print("Enter length (mm):")
	l_r = float(input())
	print("Enter width (mm):")
	w_r = float(input())
	shape = "Rectangle"
	fname_output = shape+"_"+str(r)+"x"+str(c)+"_output.gcode"
	gcode_headers(fname_output)
	for i in range(r):
		y = y0 + (i*r_sep)
		for j in range(c):
			x = x0 + (j*c_sep)
			gcode_rectangle(x,y,l_r,w_r,ext_width,fname_output)
	gcode_footers(fname_output,r,c,r_sep,c_sep,shape)

if choice == "T":
	print("Enter height (mm):")
	h_t = float(input())
	print("Enter base (mm):")
	b_t = float(input())
	shape = "Triangle"
	fname_output = shape+"_"+str(r)+"x"+str(c)+"_output.gcode"
	gcode_headers(fname_output)
	for i in range(r):
		y = y0 + (i*r_sep)
		for j in range(c):
			x = x0 + (j*c_sep)
			gcode_triangle(x,y,b_t,h_t,ext_width,fname_output)
	gcode_footers(fname_output,r,c,r_sep,c_sep,shape)

if choice == "U":
	print("Enter length (mm):")
	l_u = float(input())
	print("Enter separation (mm):")
	s_u = float(input())
	shape = "U"
	fname_output = shape+"_"+str(r)+"x"+str(c)+"_output.gcode"
	gcode_headers(fname_output)
	for i in range(r):
		y = y0 + (i*r_sep)
		for j in range(c):
			x = x0 + (j*c_sep)
			gcode_horseshoe(x,y,l_u,s_u,ext_width,fname_output)
	gcode_footers(fname_output,r,c,r_sep,c_sep,shape)

if choice == "G":
	print("Ensure the gcode file has only 1 Z-layer")
	print("Enter name of file (without .gcode extension):")
	f_template = input()
	fname_template = f_template+".gcode"
	shape = fname_template
	gcode_folder(fname_template)
	offsets = gcode_calc_offset(fname_template, x0, y0)
	fname_output = f_template+"_"+str(r)+"x"+str(c)+"_output.gcode"
	gcode_headers(fname_output)
	for i in range(r):
		y = (i*r_sep) + offsets[1]
		for j in range(c):
			x = (j*c_sep) + offsets[0]
			gcode_offset(fname_template, fname_output, x, y)
	gcode_footers(fname_output,r,c,r_sep,c_sep,shape)