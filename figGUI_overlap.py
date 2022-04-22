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

class FigGUI_overlap(Frame):
    def __init__(self, master, EDX_filepaths= None):
        super().__init__(master)
        f_l = Frame(self)
        f_r = Frame(self)
        f_l.pack(fill = 'both', expand = True, side = 'left')
        f_r.pack(side = 'right')

        #left side
        if EDX_filepaths:
            EDX_files = EDX_filepaths
        else:
            EDX_files = glob.glob('SECCM EDX Masking/EDX/*.csv')
            scan_files = glob.glob('SECCM EDX Masking/SECCM/*.csv')

            self.SECCM_l_var = StringVar() # SECCM
            self.SECCM_l = ttk.Combobox(f_l,  width = 40, textvariable = self.SECCM_l_var, values = [os.path.basename(e) for e in scan_files])
            self.SECCM_l.current(0)
            self.SECCM_l.bind("<<ComboboxSelected>>", self.on_SECCM_l)

        self.EDX_l_var = StringVar() # EDX
        edx_f = LabelFrame(f_l, text = 'select EDX data')
        self.root_path = os.path.dirname(EDX_files[0])
        self.EDX_l = ttk.Combobox(edx_f, width = 40,  textvariable = self.EDX_l_var, values = [os.path.basename(e) for e in EDX_files])
        self.EDX_l.current(0)
        # self.SECCM_l.pack()

        self.EDX_l.current(0)
        edx_f.pack()
        self.EDX_l.pack()

        fig = Figure(figsize = (7.5, 7.5))
        self.ax = fig.add_subplot(111)
        fig.subplots_adjust(left=0.2, right=0.8, top=0.8, bottom=0.2)

        self.canvas = FigureCanvasTkAgg(fig, master=f_l)  # A tk.DrawingArea.
        toolbar = NavigationToolbar(self.canvas, f_l)
        toolbar.update()
        self.canvas.get_tk_widget().pack(fill='both', expand=1)

        #right side
        #EDX figure
        # gaussian filter
        fig_f = LabelFrame(f_r, text = 'EDX figure setup')
        gau_t = Label(fig_f, text = 'gaussian'+ '\n'+'filter:')
        self.gau_var = DoubleVar()
        self.gau_var.set(3)
        gau_sc = Scale(fig_f, variable = self.gau_var, from_=0, to=30, resolution =0.2, length = 400,  command = self.on_gau_mask)
        #mask
        mask_t = Label(fig_f, text = 'mask'+'\n'+'threshold')
        self.mask_var = DoubleVar()
        self.mask_var.set(0.5)
        mask_sc = Scale(fig_f, variable = self.mask_var, from_ =0, to =1, resolution = 0.05, length = 400,  command = self.on_gau_mask)
        #transparent
        transparent_t = Label(fig_f, text = 'transparency')
        self.transparent_var = DoubleVar()
        self.transparent_var.set(1)
        transparent_sc = Scale(fig_f, variable = self.transparent_var, from_ =1, to =0, resolution = 0.05, length = 400,  command = self.on_gau_transparent)

        gau_t.grid(row = 0, column = 0, sticky = 'nw', padx = (5,5), pady = (5,5))
        gau_sc.grid(row = 1, column = 0, sticky = 'nw', padx = (5,5), pady = (5,5))
        mask_t.grid(row = 0, column = 1, sticky = 'nw', padx = (5,5), pady = (5,5))
        mask_sc.grid(row = 1, column = 1, sticky = 'nw', padx = (5,5), pady = (5,5))
        transparent_t.grid(row = 0, column = 2, sticky = 'nw', padx = (5,5), pady = (5,5))
        transparent_sc.grid(row = 1, column = 2, sticky = 'nw', padx = (5,5), pady = (5,5))

        SECCM_f = LabelFrame(f_r, text = 'SECCM figure setup')
        SECCM_cb_l = Label(SECCM_f, text = 'colormaps')
        self.SECCM_cb_v = StringVar()
        SECCM_cb = ttk.Combobox(SECCM_f, textvariable = self.SECCM_cb_v, values = ['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 'winter_r'], width = 18)
        #volatage range
        min_l = Label(SECCM_f, text = 'vmin:')
        self.min_var = DoubleVar()
        # self.min_var.set(0)
        min_sb = Scale(SECCM_f, variable = self.min_var,length = 120, from_=0, to=0.5, orient = 'horizontal', resolution = 0.01, command = self.on_SECCM_fig)
        max_l = Label(SECCM_f, text = 'vmax:')
        self.max_var = DoubleVar()
        # self.max_var.set(1)
        max_sb = Scale(SECCM_f, variable = self.max_var,length = 120, from_=0.5, to=1, orient = 'horizontal', resolution = 0.01, command = self.on_SECCM_fig)
        SECCM_cb_l.grid(row = 0, column =0, sticky = 'nw', padx = (5,0), pady = (5,0))
        SECCM_cb.grid(row = 0, column =1, sticky = 'nw', padx = (0,5), pady = (5,0))
        min_l.grid(row = 1, column =0, sticky = 'nw', padx = (5,0), pady = (5,0))
        min_sb.grid(row = 1, column =1, sticky = 'nw', padx = (0,5), pady = (0,5))
        max_l.grid(row = 2, column =0, sticky = 'nw', padx = (5,0), pady = (5,0))
        max_sb.grid(row = 2, column =1, sticky = 'nw', padx = (0,5), pady = (0,5))


        #figure movement
        move_f = LabelFrame(f_r, text = 'EDX figure movement')
        self.up_b = Button(move_f, text = 'up', width = '4',command = lambda e = 'up':self.on_move(e))
        self.down_b = Button(move_f, text = 'down', width = '4',command = lambda e = 'down':self.on_move(e))
        self.left_b = Button(move_f, text = 'left', width = '4',command = lambda e = 'left':self.on_move(e))
        self.right_b = Button(move_f, text = 'right', width = '4',command = lambda e = 'right':self.on_move(e))
        self.zoom_in_b = Button(move_f, text = '+', width = 2,command = lambda e = 'zoomin':self.on_move(e))
        self.zoom_out_b = Button(move_f, text = '-',width = 2,command = lambda e = 'zoomout':self.on_move(e))
        rotate_f = LabelFrame(move_f, text = 'rotate')
        self.rotate_b_var = DoubleVar()
        self.rotate_b = Scale(rotate_f, variable = self.rotate_b_var, from_=-10, to=10, resolution = 0.05, length = 190, orient = 'horizontal', command = self.on_rotate)
        self.rotate_b.pack()

        self.up_b.grid(row = 0, column = 1, sticky = 'nw')
        self.down_b.grid(row = 2, column = 1, sticky = 'nw')
        self.left_b.grid(row = 1, column = 0, sticky = 'nw')
        self.right_b.grid(row = 1, column = 2, sticky = 'nw')

        self.zoom_in_b.grid(row = 0, column = 3, sticky = 'nw', padx = (15,5))
        self.zoom_out_b.grid(row = 2, column = 3, sticky = 'nw', padx = (15,5))
        rotate_f.grid(row = 3, column = 0, sticky = 'nw', columnspan = 4,pady = (5,5))
        # figure scale
        scale_f = LabelFrame(f_r, text = 'EDX figure scale')
        self.scaleX_var = DoubleVar()
        self.scaleY_var = DoubleVar()
        self.scaleX_var.set(1.0)
        self.scaleY_var.set(1.0)
        Label(scale_f, text = 'scale x:').grid(row =0, column =0,sticky = 'nw',padx = (40,0))
        Entry(scale_f, textvariable = self.scaleX_var, width = 4).grid(row =0, column=1, sticky = 'nw')
        Label(scale_f, text = 'scale y:').grid(row =1, column =0,sticky = 'nw',padx = (40,0))
        Entry(scale_f, textvariable = self.scaleY_var, width = 4).grid(row =1, column=1, sticky = 'nw')
        Button(scale_f, text = 'set', fg = 'green', width = 6,command = self.on_scale).grid(row =2, column=0, columnspan = 2, padx =(75,75), pady = (2, 6),sticky = 'nw')

        #export button
        export_b = Button(f_r, text = 'export data',fg = 'blue', command = self.on_export)


        fig_f.pack()
        SECCM_f.pack()
        move_f.pack()
        scale_f.pack()
        export_b.pack(pady = (5,5))


        SECCM_cb.bind("<<ComboboxSelected>>", self.on_SECCM_fig)
        self.EDX_l.bind("<<ComboboxSelected>>", self.on_EDX_l)

    def on_scale(self):
        pass

    def on_export(self):
        pass

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

class Export_GUI(Frame):
    def __init__(self, master, EDX_filepaths):
        super().__init__(master)
        self.EDX_cbs = {}
        f = LabelFrame(self, text = 'select elements to export:')
        for name in EDX_filepaths:
            text = os.path.basename(name).replace('.csv', '')
            cb_var = IntVar()
            cb_var.set(1)
            self.EDX_cbs[name] = cb_var
            cb = Checkbutton(f, text = text, variable = cb_var)
            cb.pack(side = 'left', padx = (2,2), pady=(5,5))


        self.nor_var = IntVar(value = 1)
        nor_cb = Checkbutton(self, text = 'normalization', variable = self.nor_var)

        f.pack()
        nor_cb.pack()

    def is_nor(self):
        return self.nor_var.get()



    def get_clicked(self):
        EDX_clicked = []
        for text, cb_var in self.EDX_cbs.items():
            if cb_var.get() ==1:
                EDX_clicked.append(text)
        return EDX_clicked


class NavigationToolbar(NavigationToolbar2Tk):
    # only display the buttons we need
    toolitems = []

def main():
    root = Tk()
    FigGUI_overlap(root).pack(fill = 'both', expand = True)
    root.mainloop()


if __name__=='__main__':
    main()
