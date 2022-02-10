import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.io import loadmat
from collections import defaultdict
from matplotlib.backends.backend_tkagg import (
                                    FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import *
import os
from tkinter.filedialog import asksaveasfilename
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from figConfig_overlap import FigConfig_overlap


class View_SECCM_GUI():
    def __init__(self, master):

        f_l = Frame(master)
        f_r = Frame(master)
        f_l.pack(fill = 'both', expand = True, side = 'left')
        f_r.pack(side = 'right')

        #leftside
        para_f = Frame(f_l)
        self.voltage_var = DoubleVar()
        # v1, v2 = np.min(self.data[0, 0]['x']), np.max(self.data[0, 0]['x'])
        # self.voltage_var.set((v2-v1)/5)

        scale_f = LabelFrame(para_f, text = 'change potential')
        self.voltage_s = Scale(scale_f,orient='horizontal', length = 500, variable = self.voltage_var, command = self.on_change_map)
        # self.voltage_s = Scale(scale_f, from_= v1, to=v2, orient='horizontal', length = 500, variable = self.voltage_var, command = self.on_change_map, resolution = (v2-v1)/100)
        self.voltage_s.pack()

        #volatage range
        v_f = LabelFrame(para_f)
        min_l = Label(v_f, text = 'vmin:')
        self.min_var = DoubleVar()
        self.min_var.set(0)
        min_sb = Scale(v_f, variable = self.min_var,length = 180, from_=0, to=0.5, orient = 'horizontal', resolution = 0.01, command = self.on_change_map)
        max_l = Label(v_f, text = 'vmax:')
        self.max_var = DoubleVar()
        self.max_var.set(1)
        max_sb = Scale(v_f, variable = self.max_var,length = 180, from_=0.5, to=1, orient = 'horizontal', resolution = 0.01, command = self.on_change_map)

        min_l.grid(row = 0, column =0, sticky = 'nw', padx = (5,0), pady = (5,0))
        min_sb.grid(row = 0, column =1, sticky = 'nw', padx = (0,5), pady = (0,5))
        max_l.grid(row = 0, column =2, sticky = 'nw', padx = (48,0), pady = (5,0))
        max_sb.grid(row = 0, column =3, sticky = 'nw', padx = (0,5), pady = (0,5))

        #buttons
        f_bb = Frame(para_f)
        #select cmap
        self.cmap_cb_var = StringVar()
        cmap_f = LabelFrame(f_bb, text = 'select colormaps')
        cmap_cb = ttk.Combobox(cmap_f, textvariable = self.cmap_cb_var, values  = ['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 'winter_r'])
        cmap_cb.pack()
        cmap_cb.current(0)
        cmap_cb.bind("<<ComboboxSelected>>", self.on_change_map)
        export_b = Button(f_bb, text = 'export .csv', fg= 'blue', command = self.on_export)
        self.next_b = Button(f_bb, text = 'next: overlap with EDX data', command = self.on_next, fg = 'red')


        cmap_f.grid(row = 0, column = 0, padx = (5,5), pady =(5,5), sticky = 'nw')
        export_b.grid(row = 0, column = 1,padx = (5,5), pady =(15,5), sticky = 'nw')
        self.next_b.grid(row = 0, column = 2,padx = (5,5), pady =(15,5), sticky = 'nw')

        scale_f.pack()
        v_f.pack()
        f_bb.pack()
        Button(para_f, text = 'clear selection', width = '20', fg= 'green', command = self.on_clear_selection).pack()

        fig_map = Figure(figsize = (6,6))
        self.ax_map = fig_map.add_subplot(111)
        fig_map.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)

        self.canvas_map = FigureCanvasTkAgg(fig_map, master=para_f)  # A tk.DrawingArea.
        toolbar = NavigationToolbar2Tk(self.canvas_map, para_f)
        toolbar.update()

        para_f.pack(fill = 'both', expand = 1)
        self.canvas_map.get_tk_widget().pack(fill='both', expand=1)


        self.cid = self.canvas_map.mpl_connect('button_press_event', self.onclick)

        #right side
        fig = Figure(figsize = (6,6))
        self.ax = fig.add_subplot(111)
        # fig.subplots_adjust(left=0.2, right=0.8, top=0.8, bottom=0.2)

        self.canvas = FigureCanvasTkAgg(fig, master=f_r)  # A tk.DrawingArea.
        toolbar = NavigationToolbar2Tk(self.canvas, f_r)
        toolbar.update()
        self.canvas.get_tk_widget().pack(fill='both', expand=1)

    def on_clear_selection(self):
        pass

    def on_change_map(self, e):
        pass
    def onclick(self, event):
        pass
    def on_next(self):
        pass
    def on_export(self):
        pass










def main():
    root = Tk()

    View_SECCM_GUI(root)

    root.title('Visulization SECCM')
    root.mainloop()


if __name__=='__main__':
    main()


