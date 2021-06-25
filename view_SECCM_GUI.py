import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from collections import defaultdict
from matplotlib.backends.backend_tkagg import (
                                    FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import *
import os
from tkinter import ttk
from matplotlib.figure import Figure



class View_SECCM_GUI():
    def __init__(self, master, seccm_mat, sel_seccm_filename = None, EDX_filepaths = None):
        if sel_seccm_filename:
            self.sel_seccm_filename = sel_seccm_filename
            master.title(sel_seccm_filename)
            self.EDX_filepaths = EDX_filepaths


        self.data = defaultdict(dict)
        self.shape = seccm_mat.shape

        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self.data[i,j]['x'] = seccm_mat[j, i][0][0]
                self.data[i,j]['y'] = seccm_mat[j, i][0][1]


        f_l = Frame(master)
        f_r = Frame(master)
        f_l.pack(fill = 'both', expand = True, side = 'left')
        f_r.pack(side = 'right')

        #leftside
        para_f = Frame(f_l)
        self.voltage_var = DoubleVar()
        v1, v2 = np.min(self.data[0, 0]['x']), np.max(self.data[0, 0]['x'])
        self.voltage_var.set((v2-v1)/5)

        scale_f = LabelFrame(para_f, text = 'change potential')
        voltage_s = Scale(scale_f, from_= v1, to=v2, orient='horizontal', length = 500, variable = self.voltage_var, command = self.on_change_map, resolution = (v2-v1)/100)
        voltage_s.pack()

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
        cmap_cb = ttk.Combobox(cmap_f, textvariable = self.cmap_cb_var, values = ['binary', 'Greys', 'ocean', 'YlOrRd', 'jet', 'Set1'])
        cmap_cb.pack()
        cmap_cb.current(0)
        cmap_cb.bind("<<ComboboxSelected>>", self.on_change_map)
        export_b = Button(f_bb, text = 'export .csv', command = self.on_export)


        cmap_f.grid(row = 0, column = 0, padx = (5,5), pady =(5,5), sticky = 'nw')
        export_b.grid(row = 0, column = 1,padx = (5,5), pady =(15,5), sticky = 'nw')


        scale_f.pack()
        v_f.pack()
        f_bb.pack()

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

        v = (v2-v1)/5
        self.matrix = np.zeros(self.shape)
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self.matrix[i, j] = self.get_y_from_x(v, self.data[i,j]['x'], self.data[i,j]['y'])
        self.map_fig = self.ax_map.imshow(self.matrix, cmap = 'binary')
        self.map_cb = self.ax_map.figure.colorbar(self.map_fig)
        self.canvas_map.draw()

    def on_export(self):
        pass


    def get_y_from_x(self, x, array_x, array_y):
        idx = np.abs(array_x - x).argmin()
        return array_y[idx]

    def on_change_map(self, e):
        try:
            self.map_cb.remove()
            self.map_fig.remove()
            self.vline.remove()

        except:
            pass
        # self.ax_map.clear()

        v = float(self.voltage_var.get())
        self.matrix = np.zeros(self.shape)
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self.matrix[i, j] = self.get_y_from_x(v, self.data[i,j]['x'], self.data[i,j]['y'])
        vmin = np.quantile(self.matrix, float(self.min_var.get()))
        vmax = np.quantile(self.matrix, float(self.max_var.get()))
        cmap = self.cmap_cb_var.get()
        self.map_fig = self.ax_map.imshow(self.matrix, vmin=vmin, vmax = vmax, cmap = cmap)
        self.map_cb = self.ax_map.figure.colorbar(self.map_fig)
        self.canvas_map.draw()

        self.vline = self.ax.axvline(float(self.voltage_var.get()), color = 'red', linestyle = 'dashed')
        self.canvas.draw()

    def onclick(self, event):
        self.ax.clear()
        try:
            self.plot_click.remove()
        except:
            pass

        j, i =int(event.xdata+0.5), int(event.ydata+0.5)
        x, y = self.data[i, j]['x'], self.data[i,j]['y']
        self.ax.plot(x, y, label = f'[{i}, {j}]')
        self.vline = self.ax.axvline(float(self.voltage_var.get()), color = 'red', linestyle = 'dashed')
        self.plot_click, = self.ax_map.plot(j, i, 'X',  color = 'red', markeredgecolor = 'white', markersize = 8)
        self.ax.legend()
        self.canvas.draw()
        self.canvas_map.draw()






def main():
    root = Tk()
    m = loadmat('SECCM EDX Masking/SECCM/Sample24_L1N5_1_ORR_HER.mat')
    for v in m.values():
        if type(v) is np.ndarray:
            seccm_mat = v
            View_SECCM_GUI(root, seccm_mat)

    root.title('Visulization SECCM')
    root.mainloop()


if __name__=='__main__':
    main()


