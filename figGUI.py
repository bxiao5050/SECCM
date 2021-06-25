import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from numpy import genfromtxt
from scipy.ndimage import zoom
from scipy.ndimage import rotate
import glob
from matplotlib.backends.backend_tkagg import (
                                    FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import *
import os
from tkinter import ttk
from matplotlib.figure import Figure

class FigGUI(Frame):
    def __init__(self, master, seccm_data = None, EDX_filepaths= None):
        super().__init__(master)
        f_l = Frame(self)
        f_r = Frame(self)
        f_l.pack(fill = 'both', expand = True, side = 'left')
        f_r.pack(side = 'right')

        #left side
        self.SECCM_l_var = StringVar() # SECCM
        self.SECCM_l = ttk.Combobox(f_l,  width = 40, textvariable = self.SECCM_l_var)

        if EDX_filepaths:
            EDX_files = EDX_filepaths
            self.SECCM_l.config(values = [k for k in seccm_data])
        else:
            EDX_files = glob.glob('SECCM EDX Masking/EDX/*.csv')
            scan_files = glob.glob('SECCM EDX Masking/SECCM/*.csv')
            self.SECCM_l.config(values = [os.path.basename(e) for e in scan_files])

        self.SECCM_l.current(0)

        self.EDX_l_var = StringVar() # EDX
        edx_f = LabelFrame(f_l, text = 'select EDX data')
        self.EDX_l = ttk.Combobox(edx_f, width = 40,  textvariable = self.EDX_l_var, values = [os.path.basename(e) for e in EDX_files])
        self.SECCM_l.pack()

        self.EDX_l.current(0)
        edx_f.pack()
        self.EDX_l.pack()

        fig = Figure(figsize = (7, 7))
        self.ax = fig.add_subplot(111)
        fig.subplots_adjust(left=0.2, right=0.8, top=0.8, bottom=0.2)

        self.canvas = FigureCanvasTkAgg(fig, master=f_l)  # A tk.DrawingArea.
        toolbar = NavigationToolbar(self.canvas, f_l)
        toolbar.update()
        self.canvas.get_tk_widget().pack(fill='both', expand=1)

        #right side
        #EDX figure
        # gaussian filter
        fig_f = LabelFrame(f_r, text = 'EDX fig sharpness')
        gau_t = Label(fig_f, text = 'gaussian'+ '\n'+'filter:')
        self.gau_var = DoubleVar()
        self.gau_var.set(3)
        gau_sc = Scale(fig_f, variable = self.gau_var, from_=0, to=30, resolution =0.2, length = 700,  command = self.on_gau_mask)
        #mask
        mask_t = Label(fig_f, text = 'mask'+'\n'+'threshold')
        self.mask_var = DoubleVar()
        self.mask_var.set(0.5)
        mask_sc = Scale(fig_f, variable = self.mask_var, from_ =0, to =1, resolution = 0.05, length = 700,  command = self.on_gau_mask)
        #transparent
        transparent_t = Label(fig_f, text = 'transparent')
        self.transparent_var = DoubleVar()
        self.transparent_var.set(1)
        transparent_sc = Scale(fig_f, variable = self.transparent_var, from_ =1, to =0, resolution = 0.05, length = 700,  command = self.on_gau_transparent)

        gau_t.grid(row = 0, column = 0, sticky = 'nw', padx = (5,5), pady = (5,5))
        gau_sc.grid(row = 1, column = 0, sticky = 'nw', padx = (5,5), pady = (5,5))
        mask_t.grid(row = 0, column = 1, sticky = 'nw', padx = (5,5), pady = (5,5))
        mask_sc.grid(row = 1, column = 1, sticky = 'nw', padx = (5,5), pady = (5,5))
        transparent_t.grid(row = 0, column = 2, sticky = 'nw', padx = (5,5), pady = (5,5))
        transparent_sc.grid(row = 1, column = 2, sticky = 'nw', padx = (5,5), pady = (5,5))

        SECCM_f = LabelFrame(f_r, text = 'SECCM fig')
        self.SECCM_cb_v = StringVar()
        SECCM_cb = ttk.Combobox(SECCM_f, textvariable = self.SECCM_cb_v, values = ['binary', 'Greys', 'ocean', 'YlOrRd', 'jet', 'Set1'])
        SECCM_cb.current(0)
        SECCM_cb.pack()

        #figure movement
        move_f = LabelFrame(f_r, text = 'EDX fig movement')
        self.up_b = Button(move_f, text = 'up', width = '4',command = lambda e = 'up':self.on_move(e))
        self.down_b = Button(move_f, text = 'down', width = '4',command = lambda e = 'down':self.on_move(e))
        self.left_b = Button(move_f, text = 'left', width = '4',command = lambda e = 'left':self.on_move(e))
        self.right_b = Button(move_f, text = 'right', width = '4',command = lambda e = 'right':self.on_move(e))
        self.zoom_in_b = Button(move_f, text = '+', width = 2,command = lambda e = 'zoomin':self.on_move(e))
        self.zoom_out_b = Button(move_f, text = '-',width = 2,command = lambda e = 'zoomout':self.on_move(e))
        self.rotate_b_var = DoubleVar()
        self.rotate_b = Scale(move_f, variable = self.rotate_b_var, from_=-10, to=10, resolution = 0.05, length = 180, orient = 'horizontal', command = self.on_rotate)

        self.up_b.grid(row = 0, column = 1, sticky = 'nw')
        self.down_b.grid(row = 2, column = 1, sticky = 'nw')
        self.left_b.grid(row = 1, column = 0, sticky = 'nw')
        self.right_b.grid(row = 1, column = 2, sticky = 'nw')

        self.zoom_in_b.grid(row = 0, column = 3, sticky = 'nw', padx = (15,5))
        self.zoom_out_b.grid(row = 2, column = 3, sticky = 'nw', padx = (15,5))
        self.rotate_b.grid(row = 3, column = 0, sticky = 'nw', columnspan = 4,pady = (5,5))


        fig_f.pack()
        SECCM_f.pack()
        move_f.pack()


        SECCM_cb.bind("<<ComboboxSelected>>", self.on_SECCM_fig)
        self.EDX_l.bind("<<ComboboxSelected>>", self.on_EDX_l)
        self.SECCM_l.bind("<<ComboboxSelected>>", self.on_SECCM_l)



    def on_move(self):
        pass

    def on_gau_mask(self, e):
        pass

    def on_gau_transparent(self, e):
        pass

    def on_SECCM_l(self, event):
        pass

    def on_EDX_l(self, event):
        pass

    def on_SECCM_fig(self, e):
        pass

    def on_rotate(self, e):
        pass


class NavigationToolbar(NavigationToolbar2Tk):
    # only display the buttons we need
    toolitems = []

def main():
    root = Tk()
    FigGUI(root).pack(fill = 'both', expand = True)
    root.mainloop()


if __name__=='__main__':
    main()
