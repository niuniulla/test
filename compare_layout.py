import sys, os
import numpy as np
import matplotlib
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import time

matplotlib.use('TkAgg')
from mpl_toolkits.mplot3d import Axes3D

if sys.version_info<(3,0,0):
        import Tkinter as tk
        import tkFileDialog
if sys.version_info > (3,0,0):
        import tkinter as tk
        from tkinter import filedialog
        
from compare import compare

comp = compare()
mesh = 0

# root
root = tk.Tk()
root.title('Model Definition')
width = 1800
height = 950
root.geometry('{}x{}'.format(width, height))
#root.resizable(width=tk.FALSE, height=tk.FALSE)


# create Frames
top_frame = tk.Frame(root, width=width, height=height*0.05, pady=3, relief=tk.GROOVE, borderwidth = 1.5)
center = tk.Frame(root, width=width, height=height*0.85, padx=3, pady=3)
btm_frame = tk.Frame(root, width=width, height=height*0.1, pady=3)

top_frame.grid(row=0, columnspan=3, sticky="nsew")
center.grid(row=1, columnspan=3, sticky="nsew")
btm_frame.grid(row=3, columnspan=3, sticky="nsew")

ctr_left = tk.Frame(center, width=width*0.35, height=height*0.85, relief=tk.GROOVE, borderwidth = 0.5)
ctr_mid = tk.Frame(center, width=width*0.35, height=height*0.85, relief=tk.GROOVE, padx=3, pady=3, borderwidth = 0.5)
ctr_right = tk.Frame(center, width=width*0.15, height=height*0.85, relief=tk.GROOVE, padx=3, pady=3, borderwidth = 0.5)
ctr_right2 = tk.Frame(center, width=width*0.15, height=height*0.85, relief=tk.GROOVE, padx=3, pady=3, borderwidth = 0.5)
ctr_left.grid(row=0, column=1, sticky="nsew")
ctr_left.grid_propagate(0)
ctr_mid.grid(row=0, column=2, sticky="nsew")
ctr_mid.grid_propagate(0)
ctr_right.grid(row=0, column=0, sticky="nsew")
ctr_right.grid_propagate(0)
ctr_right2.grid(row=0, column=3, sticky="nsew")
ctr_right2.grid_propagate(0)

btm_left = tk.Frame(btm_frame, width=width*0.6, height=height*0.1, relief=tk.GROOVE, borderwidth = 0.5)
btm_left.grid_propagate(0)
btm_right = tk.Frame(btm_frame, width=width*0.4, height=height*0.1, relief=tk.GROOVE, pady=3, borderwidth = 0.5)
btm_right.grid_propagate(0)
btm_left.grid(row=0, column=0, sticky="nsew")
btm_right.grid(row=0, column=2, sticky="nsew")


option_frame = tk.Frame(ctr_right, width=width*0.15, height=height*0.85*0.35, relief=tk.GROOVE, borderwidth = 0.5)
option_frame.grid_propagate(0)
display_frame = tk.Frame(ctr_right, width=width*0.15, height=height*0.85*0.45, relief=tk.GROOVE, borderwidth = 0.5)
display_frame.grid_propagate(0)
display2_frame = tk.Frame(ctr_right, width=width*0.15, height=height*0.85*0.2, relief=tk.GROOVE, borderwidth = 0.5)
display2_frame.grid_propagate(0)
option_frame.grid(row=0, column=0, sticky="nsew")
display_frame.grid(row=1, column=0, sticky="nsew")
display2_frame.grid(row=2, column=0, sticky="nsew")

# create areas for drawing
fig_face = Figure()
a_face = fig_face.add_axes((0,0,1,1), projection="3d")
yaw = 90
pitch = 90
fig_face.get_axes()[0].view_init(yaw,pitch)
a_face.set_axis_off()
canvas = FigureCanvasTkAgg(fig_face, master=ctr_left)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

# for slider frames
w2 = tk.Scale(ctr_left, from_=0, to=200, length=width*0.35,tickinterval=10, orient=tk.HORIZONTAL)
w2.pack(anchor = tk.N)

f1_comp = Figure()
a1_comp = f1_comp.add_subplot(211)
a2_comp = a1_comp.twinx()
a3_comp = f1_comp.add_subplot(212)
canvas1 = FigureCanvasTkAgg(f1_comp, master=ctr_mid)
canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=1)


# label for display open file names
text_fl = tk.StringVar()
text_fl.set("   FaceLift file: ")
text_performer = tk.StringVar()
text_performer.set("Performer file: ")
fl_label = tk.Label(top_frame, textvariable=text_fl)
performer_label = tk.Label(top_frame, textvariable=text_performer)
fl_label.grid(row=0, columnspan=3, sticky=tk.W)
performer_label.grid(row=1, columnspan=3, sticky=tk.W)


# create display global indice
number_label = tk.Label(display2_frame, text='Global Index: ', font=("Helvetica", 18))
number_label.grid(row=0, column=0, columnspan=2)
global_indice= tk.StringVar()
global_indice.set("")
global_label = tk.Label(display2_frame, textvariable=global_indice, padx=10, pady=10, font=("Helvetica", 24), fg="red")
global_label.grid(row=3, column=1)


# create display frame indice
frame_label = tk.Label(display_frame, text='Frame Info:', font=("Helvetica", 18))
frame_label.grid(row=0, column=0, columnspan=2)

avg_label = tk.Label(display_frame, text='Avg abs: ', anchor=tk.W, font=("Helvetica", 14), fg="blue")
avg_label.grid(row=1, column=0, sticky=tk.E)
avg_indice = tk.StringVar()
avg_label1 = tk.Label(display_frame, textvariable=avg_indice, font=("Helvetica", 14), fg="blue")
avg_label1.grid(row=1, column=1, sticky=tk.W)

rel_label = tk.Label(display_frame, text='Avg rel(%): ', anchor=tk.W,  font=("Helvetica", 14), fg="blue")
rel_label.grid(row=2, column=0, sticky=tk.E)
rel_indice = tk.StringVar()
rel_label1 = tk.Label(display_frame, textvariable=rel_indice, font=("Helvetica", 14), fg="blue")
rel_label1.grid(row=2, column=1, sticky=tk.W)

max_label = tk.Label(display_frame, text='Max abs: ', font=("Helvetica", 14), fg="blue")
max_label.grid(row=3, column=0, sticky=tk.E)
max_indice = tk.StringVar()
max_label1 = tk.Label(display_frame, textvariable=max_indice, font=("Helvetica", 14), fg="blue")
max_label1.grid(row=3, column=1, sticky=tk.W)

maxrel_label = tk.Label(display_frame, text='Max rel(%): ', font=("Helvetica", 14), fg="blue")
maxrel_label.grid(row=4, column=0, sticky=tk.E)
maxrel_indice = tk.StringVar()
maxrel_label1 = tk.Label(display_frame, textvariable=maxrel_indice, font=("Helvetica", 14), fg="blue")
maxrel_label1.grid(row=4, column=1, sticky=tk.W)

min_label = tk.Label(display_frame, text='Min abs: ', font=("Helvetica", 14), fg="blue")
min_label.grid(row=5, column=0, sticky=tk.E)
min_indice = tk.StringVar()
min_label1 = tk.Label(display_frame, textvariable=min_indice, font=("Helvetica", 14), fg="blue")
min_label1.grid(row=5, column=1, sticky=tk.W)

minrel_label = tk.Label(display_frame, text='Min rel(%): ', font=("Helvetica", 14), fg="blue")
minrel_label.grid(row=6, column=0, sticky=tk.E)
minrel_indice = tk.StringVar()
minrel_label1 = tk.Label(display_frame, textvariable=minrel_indice, font=("Helvetica", 14), fg="blue")
minrel_label1.grid(row=6, column=1, sticky=tk.W)

log_label = tk.Label(display_frame, text='Avg index: ', anchor=tk.W, font=("Helvetica", 14), fg="green")
log_label.grid(row=7, column=0, sticky=tk.E)
log_indice = tk.StringVar()
log_label1 = tk.Label(display_frame, textvariable=log_indice, font=("Helvetica", 14), fg="green")
log_label1.grid(row=7, column=1, sticky=tk.W)

minlog_label = tk.Label(display_frame, text='Max index: ',  font=("Helvetica", 14), fg="green")
minlog_label.grid(row=8, column=0, sticky=tk.E)
minlog_indice = tk.StringVar()
minlog_label1 = tk.Label(display_frame, textvariable=minlog_indice, font=("Helvetica", 14), fg="green")
minlog_label1.grid(row=8, column=1, sticky=tk.W)

maxlog_label = tk.Label(display_frame, text='Min index: ',  font=("Helvetica", 14), fg="green")
maxlog_label.grid(row=9, column=0, sticky=tk.E)
maxlog_indice = tk.StringVar()
maxlog_label1 = tk.Label(display_frame, textvariable=maxlog_indice, font=("Helvetica", 14), fg="green")
maxlog_label1.grid(row=9, column=1, sticky=tk.W)


def set_label(fl, performer, frame):
    avg_indice.set(round(comp.avg_euclidean_dist_frame(fl, performer)[frame], 2))
    rel_indice.set(round(comp.relative_avg_euclidean_dist_frame(fl, performer)[frame], 2))
    log_indice.set(round(comp.log_avg_euclidean_dist_frame(fl, performer)[frame], 2))
    max_indice.set(round(comp.max_euclidean_dist_frame(fl, performer)[frame], 2))
    maxrel_indice.set(round(comp.relative_max_euclidean_dist_frame(fl, performer)[frame], 2))
    maxlog_indice.set(round(comp.log_max_euclidean_dist_frame(fl, performer)[frame], 2))
    min_indice.set(round(comp.min_euclidean_dist_frame(fl, performer)[frame], 2))
    minrel_indice.set(round(comp.relative_min_euclidean_dist_frame(fl, performer)[frame], 2))
    minlog_indice.set(round(comp.log_min_euclidean_dist_frame(fl, performer)[frame], 2))


# open file button
def getFile():
    global fl
    global performer
    filename = filedialog.askopenfilename()
    if "_FaceLift" in filename:
            fl_c3d = filename
            file_c3d = filename.replace("_FaceLift", "")
            print("if fl: ", fl_c3d, "perfomer:" , file_c3d)
    else:
            file_c3d = filename
            fl_c3d = filename.split(".")[0] + "_FaceLift" + ".c3d"
            print("else fl: ", fl_c3d, "perfomer:" , file_c3d)
    
    text_fl.set("   FaceLift file: " + fl_c3d)
    text_performer.set("Performer file: " + file_c3d)
    if os.path.isfile(fl_c3d) and os.path.isfile(file_c3d):
        w2.set(0)
        fl, performer = comp.prepare_datasets(fl_c3d, file_c3d)
        plot_face(0)
        plot_comp()
        w2.bind("<B1-Motion>", refresh_face1)
        w2.configure(to=fl.shape[0], tickinterval=fl.shape[0]/10)
        log_global = comp.log_average_euclidean_dist(fl, performer)
        global_indice.set(round(log_global, 2))
        set_label(fl, performer, 0)
    else:
        print("no file exists")

openb = tk.Button(btm_left, width=20, height=3, text="Open", command=getFile)
openb.grid(row=0, column=1, padx=10, pady=10)

FaceBuilder = tk.Button(btm_left, width=20, height=3, text="FaceBuilder")
FaceBuilder.grid(row=0, column=3, padx=10, pady=10)

Definition = tk.Button(btm_left, width=20, height=3, text="Definitions")
Definition.grid(row=0, column=2, padx=10, pady=10)

def tureFig():
    a_face.set_axis_on()
    for x in range(0,100,20):
        yaw = np.degrees(np.sin(np.pi*2*x/100))
        #pitch = np.degrees(np.cos(np.pi*2*x/100))
        a_face.view_init(yaw,pitch)
        canvas.draw()
        time.sleep(0.01)

ture_plot = tk.Button(btm_left, width=20, height=3, text="Turn Scene", command=tureFig)
ture_plot.grid(row=0, column=2, padx=10, pady=10)


# create button success/fail
def create_window():
    window = tk.Toplevel(root)

    window.title("Review")
    frame1 = tk.Frame(window)
    frame1.pack(fill=tk.X)
    
    lbl1 = tk.Label(frame1, text="Title", width=6)
    lbl1.pack(side=tk.LEFT, padx=5, pady=5)           
    
    entry1 = tk.Entry(frame1)
    entry1.pack(fill=tk.X, padx=5, expand=True)
    
    frame2 = tk.Frame(window)
    frame2.pack(fill=tk.X)
    
    lbl2 = tk.Label(frame2, text="Author", width=6)
    lbl2.pack(side=tk.LEFT, padx=5, pady=5)        

    entry2 = tk.Entry(frame2)
    entry2.pack(fill=tk.X, padx=5, expand=True)
    
    frame3 = tk.Frame(window)
    frame3.pack(fill=tk.BOTH, expand=True)
    
    lbl3 = tk.Label(frame3, text="Review", width=6)
    lbl3.pack(side=tk.LEFT, anchor=tk.N, padx=5, pady=5)        

    txt = tk.Text(frame3)
    txt.pack(fill=tk.BOTH, pady=5, padx=5, expand=True)  
    
    def comment():
        window.destroy()
    
    
    e_performer = tk.Checkbutton(frame3, text = "Performer", variable = Check3, onvalue = 1, offvalue = 0, height=1, width = 20)
    e_performer.pack(side=tk.LEFT)
    e_fl = tk.Checkbutton(frame3, text = "FaceLift", variable = Check3, onvalue = 0, offvalue = 0, height=1, width = 20)
    e_fl.pack(side=tk.LEFT)
    
    e_button = tk.Button(frame3, width=10, height=3, text="send", command=comment)
    e_button.pack(side=tk.BOTTOM)
    
    
#photo=tk.PhotoImage(file="c.png")
width_label = tk.Label(btm_right, text='Decision: ', font=("Arial", 14))
success = tk.Button(btm_right,  width=20, height=3, text="Sucess", bg='green')
fail = tk.Button(btm_right, width=20, height=3, text="Fail", bg='red', command=create_window)
width_label.grid(row=0, column=0, padx=20, pady=20)
success.grid(row=0, column=1, padx=10, pady=10), success.grid_propagate(0)
fail.grid(row=0, column=2, padx=10, pady=10)


# draw face c3d
def plot_face(frame):
    
    #a = f.add_subplot(1, 1, 1, projection="3d")
    a_face.clear()
    a_face.set_axis_off()
    a_face.scatter(performer[frame,:,0], performer[frame,:,1], performer[frame,:,2], c='r', marker = '^')
    a_face.scatter(fl[frame,:,0], fl[frame,:,1], fl[frame,:,2],  c='b', marker = 'o')
    canvas.draw()

    
def mesh_face():
    global mesh 
    mesh = 1
    frame = int(w2.get())
    a_face.clear()
    yaw = 90
    pitch = 90
    a_face.view_init(yaw,pitch)
    a_face.set_axis_off()
    a_face.plot_trisurf(fl[frame,:,0], fl[frame,:,1], fl[frame,:,2], facecolor='g')
    a_face.plot_trisurf(performer[frame,:,0], performer[frame,:,1], performer[frame,:,2], facecolor='b')
    canvas.draw()
    


def refresh_face1(event):
    frame = int(w2.get())
    a_face.set_axis_off()
    if mesh:
        mesh_face()
    else:
        plot_face(frame)
    set_label(fl, performer, frame)
   

def refresh_face2():
    frame = int(w2.get())
    a_face.set_axis_off()
    a_face.clear()
    yaw = 90
    pitch = 90
    a_face.view_init(yaw,pitch)
    plot_face(frame)
    set_label(fl, performer, frame)
    global mesh 
    mesh = 0

# draw comparison
def plot_comp():
    a1_comp.clear()
    a2_comp.clear()
    a3_comp.clear()
    t = range(fl.shape[0])
    avg = comp.avg_euclidean_dist_frame(fl, performer)
    mean = comp.relative_average_euclidean_dist(fl, performer)
    mean = np.full(len(t), mean)
    
    s2 = comp.relative_avg_euclidean_dist_frame(fl, performer)
    a1_comp.plot(t, s2, 'b', linewidth=0.3)
    a1_comp.set_ylabel('Percentage (%)', color='b')
    a1_comp.plot(t, mean, linewidth=1.0, color='r')
    a2_comp.plot(t, avg, linewidth=0.3, color='y')
    a2_comp.set_ylabel('Absolute value', color='y')
    
    logall = comp.log_average_euclidean_dist(fl, performer)
    logall = np.full(len(t), logall)
    log = comp.log_avg_euclidean_dist_frame(fl, performer)
    a3_comp.plot(t, log, linewidth=0.3, color='g')
    a3_comp.set_ylabel('Index', color='b')
    a3_comp.plot(t, logall, linewidth=1.0, color='m')

    canvas1.draw()



# create display options
display_label = tk.Label(option_frame, text='Display options:', font=("Helvetica", 18))
Check1 = tk.IntVar()
Check2 = tk.IntVar()
Check3 = tk.IntVar()
Check4 = tk.IntVar()
C1 = tk.Checkbutton(option_frame, text = "mean per frame", variable = Check4, onvalue = 0, offvalue = 1, height=1, width = 20)
C2 = tk.Checkbutton(option_frame, text = "max per frame", variable = Check1, onvalue = 1, offvalue = 0, height=1, width = 20)
C3 = tk.Checkbutton(option_frame, text = "min per frame", variable = Check2, onvalue = 1, offvalue = 0, height=1, width = 20)
C4 = tk.Checkbutton(option_frame, text = "overall mean", variable = Check3, onvalue = 1, offvalue = 0, height=1, width = 20)

display_label.grid(row=0, column=0)
C1.grid(row=1, column=0, padx=2, pady=2, sticky=tk.W)
C2.grid(row=2, column=0, padx=2, pady=2, sticky=tk.W)
C3.grid(row=3, column=0, padx=2, pady=2, sticky=tk.W)
C4.grid(row=4, column=0, padx=2, pady=2, sticky=tk.W)



"""
seuil_box = Text(ctr_right2, height=2, width=10)
textBox.pack(fill=tk.BOTH, expand=1)
Process = Button(ctr_right2, height=1, width=10, text="Process", command=lambda: retrieve_input())
buttonCommit.pack()

"""
variable1 = tk.StringVar()
seuil_bad = tk.StringVar()
def retrieve_input():
    seuil = int(variable1.get())
    nb, frames = comp.get_frame_seuil(fl, performer, seuil)
    seuil_bad.set(str(nb) + " frames (" + str(round(nb/fl.shape[0]*100,2)) + "%)")
    
    #print("The bad frames: ", frames)
    
tk.Label(ctr_right2, text='Threshold: ').grid(row=0, column=0, padx=2, pady=2)
tk.Entry(ctr_right2, textvariable=variable1).grid(row=0, column=1, padx=2, pady=2)
tk.Button(ctr_right2, height=1, width=10, text="Process", command=retrieve_input).grid(row=2, column=0, padx=2, pady=2, columnspan=2)
tk.Label(ctr_right2, text='Number of bad frames: ').grid(row=3, column=0, padx=5, pady=5, columnspan=2)
tk.Label(ctr_right2, textvariable=seuil_bad).grid(row=4, column=0, padx=2, pady=2, columnspan=2)



mesh_plot = tk.Button(btm_left, width=20, height=3, text="MeshFace", command=mesh_face)
mesh_plot.grid(row=0, column=3, padx=10, pady=10)

c3d_plot = tk.Button(btm_left, width=20, height=3, text="c3d Points", command=refresh_face2)
c3d_plot.grid(row=0, column=4, padx=10, pady=10)

Fb = tk.Button(btm_left, width=20, height=3, text="FaceBuilder")
Fb.grid(row=0, column=5, padx=10, pady=10)

root.mainloop()