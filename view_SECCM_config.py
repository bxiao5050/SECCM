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
from view_SECCM_GUI import View_SECCM_GUI


class View_SECCM_config(View_SECCM_GUI):
    def __init__(self, master, seccm_mat, sel_seccm_filename = None, EDX_filepaths = None):
        super().__init__(master)
        self.plot_clicks = [] # save clicked plot
        self.clicks = []

        if sel_seccm_filename:
            self.sel_seccm_filename = sel_seccm_filename
            master.title(sel_seccm_filename)


        self.data = defaultdict(dict)
        self.shape = seccm_mat.shape

        self.export_voltage = []
        self.export_current = []
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self.data[i,j]['x'] = seccm_mat[j, i][0][0]
                self.data[i,j]['y'] = seccm_mat[j, i][0][1]

                self.export_voltage.append([j, i]+list(self.data[i,j]['x'].flatten()))
                self.export_current.append([j, i]+list(self.data[i,j]['y'].flatten()))



        v1, v2 = np.min(self.data[0, 0]['x']), np.max(self.data[0, 0]['x'])
        self.voltage_var.set((v2-v1)/5)
        # set voltage scale
        self.voltage_s.config(from_= v1, to=v2, resolution = (v2-v1)/100)
        #draw SECCM fig
        v = (v2-v1)/5
        self.matrix = np.zeros(self.shape)
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self.matrix[i, j] = self.get_y_from_x(v, self.data[i,j]['x'], self.data[i,j]['y'])
        self.cmap_cb_var.set('Blues')
        self.map_fig = self.ax_map.imshow(self.matrix, cmap = self.cmap_cb_var.get())
        self.map_cb = self.ax_map.figure.colorbar(self.map_fig)
        self.canvas_map.draw()

        #check if edx data is there
        if EDX_filepaths:
            self.EDX_filepaths = EDX_filepaths
        else:
            self.next_b.config(state = 'disabled')
        #toolbar
        self.ax_map.format_coord = self.format_coord

    def format_coord(self, x, y):
        try:
            x, y =int(x+0.5), int(y+0.5)
            return f'x:{x}, y:{y}'

        except:
            pass

    def get_seccm_fig_para(self):
        seccm_fig_para = {}
        seccm_fig_para['matrix'] = self.matrix
        seccm_fig_para['vmin_ratio'] =  float(self.min_var.get())
        seccm_fig_para['vmax_ratio'] =  float(self.max_var.get())
        seccm_fig_para['cmap'] = self.cmap_cb_var.get()
        return seccm_fig_para


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

    def on_clear_selection(self):

        [p.remove() for p in self.plot_clicks]
        self.plot_clicks = []
        self.clicks = []
        self.ax.clear()

        self.canvas_map.draw()
        self.canvas.draw()

    def onclick(self, event):
        i, j =int(event.xdata+0.5), int(event.ydata+0.5)
        x, y = self.data[j, i]['x'], self.data[j,i]['y']


        if (i, j) not in self.clicks:
            try:
                self.vline.remove()
            except:
                pass

            self.clicks.append((i, j))
            self.ax.plot(x, y, label = f'[{i}, {j}]')
            self.vline = self.ax.axvline(float(self.voltage_var.get()), color = 'red', linestyle = 'dashed')
            plot_click, = self.ax_map.plot(i, j, 'X',  color = 'red', markeredgecolor = 'white', markersize = 6)
            self.plot_clicks.append(plot_click)
            self.ax.legend()
            self.canvas.draw()
            self.canvas_map.draw()

    def on_next(self):
        w = Toplevel()
        w.title('Overlap between EDX and SCEEM figures    '+self.sel_seccm_filename)
        FigConfig_overlap(w, self.get_seccm_fig_para(), self.EDX_filepaths).pack(fill = 'both', expand = 1)

    def on_export(self):
        path = asksaveasfilename(defaultextension=".csv",filetypes=[("csv file", ".csv")])
        if len(path) !=0:

            col_v = ['x', 'y']+[f'voltage{n}' for n in range(len(self.export_voltage[0])-2)]
            col_c = ['x', 'y']+[f'current{n}' for n in range(len(self.export_voltage[0])-2)]

            pd.DataFrame(self.export_voltage, columns = col_v).to_csv(path.replace('.csv','')+'_voltage.csv', index = False)
            pd.DataFrame(self.export_current, columns = col_c).to_csv(path.replace('.csv','')+'_current.csv', index = False)
            messagebox.showinfo(message = 'file exported')





def main():
    root = Tk()
    m = loadmat('SECCM EDX Masking/SECCM/Sample24_L1N5_1_ORR_HER.mat')
    for v in m.values():
        if type(v) is np.ndarray:
            seccm_mat = v
            View_SECCM_config(root, seccm_mat)

    root.title('Visulization SECCM')
    root.mainloop()


if __name__=='__main__':
    main()


