# -*- coding: utf-8 -*-


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


from compare import compare


if sys.version_info<(3,0,0):
        import Tkinter as tk
        import tkFileDialog
if sys.version_info > (3,0,0):
        import tkinter as tk
        from tkinter import filedialog
        
from compare import compare


class compare_layout(tk.Tk):
    
    def __init__(self,parent):
        tk.Tk.__init__(self,parent)
        self.parent = parent
        self.width = 1800
        self.height = 950
        self.geometry('{}x{}'.format(self.width, self.height))
        self.initialize()

    def initialize(self):
        self.grid()

        # create Frames
        file_frame = tk.Frame(self, width=self.width, height=self.height*0.05, pady=3, relief=tk.GROOVE, borderwidth = 1.5)
        file_frame.grid(row=0, columnspan=3, sticky="nsew")
        display_frame = tk.Frame(self, width=self.width, height=self.height*0.85, padx=3, pady=3)
        display_frame.grid(row=1, columnspan=3, sticky="nsew")
        action_frame = tk.Frame(self, width=self.width, height=self.height*0.1, pady=3)
        action_frame.grid(row=3, columnspan=3, sticky="nsew")

        draw1_frame = tk.Frame(center, width=self.width*0.35, height=self.height*0.85, relief=tk.GROOVE, borderwidth = 0.5)
        draw2_frame = tk.Frame(center, width=self.width*0.35, height=self.height*0.85, relief=tk.GROOVE, padx=3, pady=3, borderwidth = 0.5)
        display1_frame = tk.Frame(center, width=self.width*0.15, height=self.height*0.85, relief=tk.GROOVE, padx=3, pady=3, borderwidth = 0.5)
        display2_frame = tk.Frame(center, width=self.width*0.15, height=self.height*0.85, relief=tk.GROOVE, padx=3, pady=3, borderwidth = 0.5)
        draw1_frame.grid(row=0, column=1, sticky="nsew")
        draw1_frame.grid_propagate(0)
        draw2_frame.grid(row=0, column=2, sticky="nsew")
        draw2_frame.grid_propagate(0)
        display1_frame.grid(row=0, column=0, sticky="nsew")
        display1_frame.grid_propagate(0)
        display2_frame.grid(row=0, column=3, sticky="nsew")
        display2_frame.grid_propagate(0)

        action_frame = tk.Frame(btm_frame, width=self.width*0.6, height=self.height*0.1, relief=tk.GROOVE, borderwidth = 0.5)
        action_frame.grid_propagate(0)
        decision_frame = tk.Frame(btm_frame, width=self.width*0.4, height=self.height*0.1, relief=tk.GROOVE, pady=3, borderwidth = 0.5)
        decision_frame.grid_propagate(0)
        action_frame.grid(row=0, column=0, sticky="nsew")
        decision_frame.grid(row=0, column=2, sticky="nsew")

        option_frame = tk.Frame(display1_frame, width=self.width*0.15, height=self.height*0.85*0.35, relief=tk.GROOVE, borderwidth = 0.5)
        option_frame.grid_propagate(0)
        display_frame = tk.Frame(display1_frame, width=self.width*0.15, height=self.height*0.85*0.45, relief=tk.GROOVE, borderwidth = 0.5)
        display_frame.grid_propagate(0)
        display2_frame_frame = tk.Frame(display1_frame, width=self.width*0.15, height=self.height*0.85*0.2, relief=tk.GROOVE, borderwidth = 0.5)
        display2_frame_frame.grid_propagate(0)
        option_frame.grid(row=0, column=0, sticky="nsew")
        display_frame.grid(row=1, column=0, sticky="nsew")
        display2_frame_frame.grid(row=2, column=0, sticky="nsew")


        # create areas for drawing face
        fig_face = Figure()
        yaw = 90
        pitch = 90
        fig_face.get_axes()[0].view_init(yaw,pitch)
        self.axe_face = fig_face.add_axes((0,0,1,1), projection="3d") 
        self.axe_face.set_axis_off()
        self.canvas_face = FigureCanvasTkAgg(fig_face, master=draw1_frame)
        self.canvas_face.get_tk_widget().pack(fill=tk.BOTH, expand=1)

        # for slider frames
        self.w2 = tk.Scale(draw1_frame, from_=0, to=200, length=width*0.35,tickinterval=10, orient=tk.HORIZONTAL)
        w2.pack(anchor = tk.N)

        # label for display open file names
        self.facelift_filename = tk.StringVar().set("   FaceLift file: ")
        label_facelift = tk.Label(file_frame, textvariable=facelift_filename)
        label_facelift.grid(row=0, columnspan=3, sticky=tk.W)
        
        performer_filename = tk.StringVar()
        performer_filename.set("Performer file: ")
        lable_performer = tk.Label(file_frame, textvariable=performer_filename)
        lable_performer.grid(row=1, columnspan=3, sticky=tk.W)

        # create display global indice
        label_global_index_text = tk.Label(display2_frame_frame, text='Global Index: ', font=("Helvetica", 18))
        label_global_index_text.grid(row=0, column=0, columnspan=2)
        global_indice= tk.StringVar().set("")
        label_global_index_num = tk.Label(display2_frame_frame, textvariable=global_indice, padx=10, pady=10, font=("Helvetica", 24), fg="red")
        label_global_index_num.grid(row=3, column=1)
            
        # create display frame indice
        tk.Label(display_frame, text='Frame Info:', font=("Helvetica", 18)).grid(row=0, column=0, columnspan=2)

        label_avg_text = tk.Label(display_frame, text='Avg abs: ', anchor=tk.W, font=("Helvetica", 14), fg="blue")
        label_avg_text.grid(row=1, column=0, sticky=tk.E)
        self.avg_frame = tk.StringVar()
        label_avg_num = tk.Label(display_frame, textvariable=avg_frame, font=("Helvetica", 14), fg="blue")
        label_avg_num.grid(row=1, column=1, sticky=tk.W)

        tk.Label(display_frame, text='Avg rel(%): ', anchor=tk.W,  font=("Helvetica", 14), fg="blue").grid(row=2, column=0, sticky=tk.E)
        self.rel_frame = tk.StringVar()
        label_rel_tnum = tk.Label(display_frame, textvariable=rel_frame, font=("Helvetica", 14), fg="blue")
        label_rel_tnum.grid(row=2, column=1, sticky=tk.W)

        tk.Label(display_frame, text='Max abs: ', font=("Helvetica", 14), fg="blue").grid(row=3, column=0, sticky=tk.E)
        self.max_frame = tk.StringVar()
        label_max_num = tk.Label(display_frame, textvariable=max_frame, font=("Helvetica", 14), fg="blue")
        label_max_num.grid(row=3, column=1, sticky=tk.W)

        tk.Label(display_frame, text='Max rel(%): ', font=("Helvetica", 14), fg="blue").grid(row=4, column=0, sticky=tk.E)
        self.maxrel_frame = tk.StringVar()
        label_maxrel_text1 = tk.Label(display_frame, textvariable=maxrel_frame, font=("Helvetica", 14), fg="blue")
        label_maxrel_text1.grid(row=4, column=1, sticky=tk.W)

        tk.Label(display_frame, text='Min abs: ', font=("Helvetica", 14), fg="blue").grid(row=5, column=0, sticky=tk.E)
        self.min_frame = tk.StringVar()
        label_min_text1 = tk.Label(display_frame, textvariable=min_frame, font=("Helvetica", 14), fg="blue")
        label_min_text1.grid(row=5, column=1, sticky=tk.W)

        tk.Label(display_frame, text='Min rel(%): ', font=("Helvetica", 14), fg="blue").grid(row=6, column=0, sticky=tk.E)
        self.minrel_frame = tk.StringVar()
        label_minrel_text1 = tk.Label(display_frame, textvariable=minrel_frame, font=("Helvetica", 14), fg="blue")
        label_minrel_text1.grid(row=6, column=1, sticky=tk.W)

        tk.Label(display_frame, text='Avg index: ', anchor=tk.W, font=("Helvetica", 14), fg="green").grid(row=7, column=0, sticky=tk.E)
        self.logavg_frame = tk.StringVar()
        label_logavg_text1 = tk.Label(display_frame, textvariable=logavg_frame, font=("Helvetica", 14), fg="green")
        label_logavg_text1.grid(row=7, column=1, sticky=tk.W)

        tk.Label(display_frame, text='Max index: ',  font=("Helvetica", 14), fg="green").grid(row=8, column=0, sticky=tk.E)
        self.logmin_frame = tk.StringVar()
        label_logmin_text1 = tk.Label(display_frame, textvariable=label_logmin_frame, font=("Helvetica", 14), fg="green")
        label_logmin_text1.grid(row=8, column=1, sticky=tk.W)

        tk.Label(display_frame, text='Min index: ',  font=("Helvetica", 14), fg="green").grid(row=9, column=0, sticky=tk.E)
        self.logmin_frame = tk.StringVar()
        label_logmin_text1 = tk.Label(display_frame, textvariable=logmin_frame, font=("Helvetica", 14), fg="green")
        label_logmin_text1.grid(row=9, column=1, sticky=tk.W)

        
        # buttons
        btn_open = tk.Button(action_frame, width=20, height=3, text="Open", command=getFile)
        btn_open.grid(row=0, column=1, padx=10, pady=10)

        btn_FaceBuilder = tk.Button(action_frame, width=20, height=3, text="FaceBuilder")
        btn_FaceBuilder.grid(row=0, column=3, padx=10, pady=10)

        btn_Definition = tk.Button(action_frame, width=20, height=3, text="Definitions")
        btn_Definition.grid(row=0, column=2, padx=10, pady=10)

        btn_ture_plot = tk.Button(action_frame, width=20, height=3, text="Turn Scene", command=tureFig)
        btn_ture_plot.grid(row=0, column=2, padx=10, pady=10)

        
        label_decision = tk.Label(decision_frame, text='Decision: ', font=("Arial", 14))
        label_decision.grid(row=0, column=0, padx=20, pady=20)
        
        btn_success = tk.Button(decision_frame,  width=20, height=3, text="Sucess", bg='green')
        btn_success.grid(row=0, column=1, padx=10, pady=10), success.grid_propagate(0)
        
        btn_fail = tk.Button(decision_frame, width=20, height=3, text="Fail", bg='red', command=create_window)
        btn_fail.grid(row=0, column=2, padx=10, pady=10)
        
        btn_mesh_plot = tk.Button(action_frame, width=20, height=3, text="MeshFace", command=mesh_face)
        btn_mesh_plot.grid(row=0, column=3, padx=10, pady=10)

        btn_c3d_plot = tk.Button(action_frame, width=20, height=3, text="c3d Points", command=refresh_face2)
        btn_c3d_plot.grid(row=0, column=4, padx=10, pady=10)

        btn_facebuilder = tk.Button(action_frame, width=20, height=3, text="FaceBuilder")
        btn_facebuilder.grid(row=0, column=5, padx=10, pady=10)



        # create display options TODO
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
        
        
        # to do analyse, TODO
        self.threshold = tk.StringVar()
        self.bad_frame_num = tk.StringVar()
        
            
        tk.Label(display2_frame, text='Threshold: ').grid(row=0, column=0, padx=2, pady=2)
        tk.Entry(display2_frame, textvariable=threshold).grid(row=0, column=1, padx=2, pady=2)
        tk.Button(display2_frame, height=1, width=10, text="Process", command=retrieve_input).grid(row=2, column=0, padx=2, pady=2, columnspan=2)
        tk.Label(display2_frame, text='Number of bad frames: ').grid(row=3, column=0, padx=5, pady=5, columnspan=2)
        tk.Label(display2_frame, textvariable=bad_frame_num ).grid(row=4, column=0, padx=2, pady=2, columnspan=2)


    def set_label(fl, performer, frame):
        avg_frame.set(round(comp.avg_euclidean_dist_frame(fl, performer)[frame], 2))
        rel_frame.set(round(comp.relative_avg_euclidean_dist_frame(fl, performer)[frame], 2))
        logavg_frame.set(round(comp.log_avg_euclidean_dist_frame(fl, performer)[frame], 2))
        max_frame.set(round(comp.max_euclidean_dist_frame(fl, performer)[frame], 2))
        maxrel_frame.set(round(comp.relative_max_euclidean_dist_frame(fl, performer)[frame], 2))
        logmin_frame.set(round(comp.log_max_euclidean_dist_frame(fl, performer)[frame], 2))
        min_frame.set(round(comp.min_euclidean_dist_frame(fl, performer)[frame], 2))
        minrel_frame.set(round(comp.relative_min_euclidean_dist_frame(fl, performer)[frame], 2))
        label_logmin_frame.set(round(comp.log_min_euclidean_dist_frame(fl, performer)[frame], 2))


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
        
        facelift_filename.set("   FaceLift file: " + fl_c3d)
        performer_filename.set("Performer file: " + file_c3d)
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


        
        def tureFig():
            axe_face.set_axis_on()
            for x in range(0,100,20):
                yaw = np.degrees(np.sin(np.pi*2*x/100))
                #pitch = np.degrees(np.cos(np.pi*2*x/100))
                axe_face.view_init(yaw,pitch)
                canvas_face.draw()
                time.sleep(0.0
                   
                   
                   
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
              
                   
    # draw face c3d
    def plot_face(frame):
        
                #a = f.add_subplot(1, 1, 1, projection="3d")
                axe_face.clear()
                axe_face.set_axis_off()
                axe_face.scatter(performer[frame,:,0], performer[frame,:,1], performer[frame,:,2], c='r', marker = '^')
                axe_face.scatter(fl[frame,:,0], fl[frame,:,1], fl[frame,:,2],  c='b', marker = 'o')
                canvas_face.draw()
            
        
            def mesh_face():
        global mesh 
        mesh = 1
        frame = int(w2.get())
        axe_face.clear()
        yaw = 90
        pitch = 90
        axe_face.view_init(yaw,pitch)
        axe_face.set_axis_off()
        axe_face.plot_trisurf(fl[frame,:,0], fl[frame,:,1], fl[frame,:,2], facecolor='g')
        axe_face.plot_trisurf(performer[frame,:,0], performer[frame,:,1], performer[frame,:,2], facecolor='b')
        canvas_face.draw()
        


    def refresh_face1(event):
        frame = int(w2.get())
        axe_face.set_axis_off()
        if mesh:
            mesh_face()
        else:
            plot_face(frame)
        set_label(fl, performer, frame)
    

    def refresh_face2():
        frame = int(w2.get())
        axe_face.set_axis_off()
        axe_face.clear()
        yaw = 90
        pitch = 90
        axe_face.view_init(yaw,pitch)
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

        canvas_face1.draw()
        
    def retrieve_input():
        seuil = int(threshold.get())
        nb, frames = comp.get_frame_seuil(fl, performer, seuil)
        seuil_bad.set(str(nb) + " frames (" + str(round(nb/fl.shape[0]*100,2)) + "%)")


if __name__ == "__main__":
    app = compare_layout(None)
    app.title('Compare')
    app.mainloop()
    
    
    
    
    
