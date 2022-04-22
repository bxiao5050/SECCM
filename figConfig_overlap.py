import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from numpy import genfromtxt
from scipy.ndimage import zoom
from scipy.ndimage import rotate
import glob
from matplotlib.backends.backend_tkagg import (
                                    FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import *
from matplotlib.figure import Figure
import os
import numpy as np
from tkinter.filedialog import asksaveasfilename
from tkinter import ttk, messagebox
from scipy import ndimage
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition
import pandas as pd
from figGUI_overlap import FigGUI_overlap, Export_GUI
from scipy.io import loadmat

class FigConfig_overlap(FigGUI_overlap):
    def __init__(self, master, seccm_fig_para, EDX_filepaths=None):
        super().__init__(master, EDX_filepaths)
        self.EDX_filepaths = EDX_filepaths
        self.initialize_SECCM_GUI(seccm_fig_para)

        #EDX data

        self.EDX_file =os.path.join(self.root_path,self.EDX_l_var.get())
        self.EDX_manipulated = genfromtxt(self.EDX_file, delimiter=',')

        self.EDX_manipulated[np.where(np.isnan(self.EDX_manipulated))]= 0
        # self.EDX_manipulated = self.normalization(self.EDX_manipulated)

        self.EDX_original= self.EDX_manipulated

        self.EDX = gaussian_filter(self.EDX_manipulated,float(self.gau_var.get()), mode='nearest')

        self.EDX[np.where(self.EDX < np.quantile(self.EDX, 0.5))]= np.nan #mask

        #draw EDX
        self.x0, self.y0 = 0, 0
        self.ax_xmax, self.ax_ymax = max(self.ax.get_xlim())-min(self.ax.get_xlim()), max(self.ax.get_ylim())-min(self.ax.get_ylim())

        self.width, self.height = 1.05, 1.05
        self.axin2 = self.ax.inset_axes([self.x0, self.y0, self.width*self.ax_xmax, self.height*self.ax_ymax], transform=self.ax.transData)

        self.limt = min(self.EDX.shape)
        self.EDX_fig = self.axin2.imshow(self.EDX[:, :], extent = (0 ,self.limt, self.limt, 0), cmap = 'jet')# EDX
        self.xcolor(self.axin2)
        self.ax.format_coord = self.format_coord
        #zoom
        self.zoom = []


        # fig.canvas.mpl_connect('button_press_event', on_click)

    def get_edxCoord_from_seccm(self, x,y):

        axin_xmax, axin_ymax = max(self.axin2.get_xlim())-min(self.axin2.get_xlim()),max(self.axin2.get_ylim())-min(self.axin2.get_ylim())
        xx= (x-self.x0)/self.width*axin_xmax/self.ax_xmax
        yy = (y-self.y0)/self.height*axin_ymax/self.ax_ymax
        return xx, yy

    def format_coord(self, x, y):

        if 1:
            xx, yy = self.get_edxCoord_from_seccm(int(x)+0.5, int(y)+0.5)
            t1 = f'SECCM: (x: {int(x)}, y: {int(y)}, v: {round(self.matrix[int(y)][int(x)], 2)})'

                # t1 = f'SECCM: (x: {int(x)}, y: {int(y)})'
            if xx>=0 and xx<=max(self.axin2.get_xlim()) and yy>=0 and yy<=max(self.axin2.get_ylim()):
                t2 = f'EDX (gaussian/threshold): (x: {int(xx)}, y: {int(yy)}, v: {round(self.EDX[int(yy)][int(xx)], 2)})'
                # t3 = f'EDX (original): (x: {int(xx)}, y: {int(yy)}, v: {round(self.EDX_manipulated[int(yy)][int(xx)], 2)})'
            else:
                t2 = f'EDX (gaussian/threshold): (x: {int(xx)}, y: {int(yy)})'
                # t3 = f'EDX (original): (x: {int(xx)}, y: {int(yy)})'
            return t1+ '                  '+t2


    def on_export(self):
        w = Toplevel(self)
        w.title('select element')
        self.edx_export = Export_GUI(w, self.EDX_filepaths)
        self.edx_export.pack()
        Button(w, text = 'export', command = lambda w = w: self.on_export_EDX(w)).pack(pady = (15,5))



    def on_export_EDX(self, w):
        path = asksaveasfilename(defaultextension=".csv",filetypes=[("csv file", ".csv")])

        if len(path) !=0:
            res = []
            edx_clicked = self.edx_export.get_clicked()
            EDXdatas = [self.get_EDXdata(f) for f in edx_clicked]
            for x in range(self.matrix_idx_min):
                for y in range(self.matrix_idx_min):
                    coord = [x, y]
                    v_seccm = round(self.matrix[int(y)][int(x)], 3)

                    xx, yy = self.get_edxCoord_from_seccm(int(x)+0.5, int(y)+0.5)

                    v_edx_original = [] #one row EDX data
                    for EDXdata in EDXdatas:
                        if xx>=0 and xx<=max(self.axin2.get_xlim()) and yy>=0 and yy<=max(self.axin2.get_ylim()):
                            v_edx_original.append(round(EDXdata[int(yy)][int(xx)], 2))
                        else:
                            v_edx_original.append(0)
                    if self.edx_export.is_nor():
                        res.append(coord+[v_seccm]+self.normalization(v_edx_original))
                    else:
                        res.append(coord+[v_seccm]+v_edx_original)
            # print(res)
            columns = ['x', 'y', 'v_seccm'] + [os.path.basename(f).replace('.csv', '') for f in edx_clicked]
            pd.DataFrame(res, columns = columns).to_csv(path.replace('.csv', '')+'.csv', index = False)
            w.destroy()
            messagebox.showinfo(message = 'file exported')

    def get_EDXdata(self, EDX_filename):
        EDX_manipulated = genfromtxt(EDX_filename, delimiter=',')
        EDX_manipulated[np.where(np.isnan(EDX_manipulated))]= 0
        #rotate
        theta = float(self.rotate_b_var.get())
        EDX_manipulated = ndimage.rotate(EDX_manipulated, theta, reshape = False)
        #gaussian_filter
        filter_size = float(self.gau_var.get())
        EDXdata = gaussian_filter(EDX_manipulated,filter_size, mode='nearest')
        #mask
        EDXdata[np.where(EDXdata < np.quantile(EDXdata, float(self.mask_var.get())))]= 0
        return EDXdata

    def normalization(self, d):
        s = sum(d)
        return [round(x/s,2) for x in d]

    def initialize_SECCM_GUI(self, seccm_fig_para):
        self.matrix = seccm_fig_para['matrix']
        vmin_ratio = seccm_fig_para['vmin_ratio']
        vmax_ratio = seccm_fig_para['vmax_ratio']
        vmin = np.quantile(self.matrix, vmin_ratio)
        vmax = np.quantile(self.matrix, vmax_ratio)
        cmap = seccm_fig_para['cmap']

        #draw SECCM
        self.matrix_idx_min = min(self.matrix.shape)
        #make the inset a rectangle
        self.SECCM_fig = self.ax.imshow(self.matrix, vmin =vmin, vmax = vmax, extent = (0, self.matrix_idx_min, self.matrix_idx_min, 0), cmap = cmap)
        #set scalebar
        self.min_var.set(vmin_ratio)
        self.max_var.set(vmax_ratio)
        self.SECCM_cb_v.set(cmap)

    def on_SECCM_fig(self, e=''):
        vmin = np.quantile(self.matrix, float(self.min_var.get()))
        vmax = np.quantile(self.matrix, float(self.max_var.get()))
        cmap = self.SECCM_cb_v.get()

        #draw SECCM
        # self.matrix_idx_min = min(self.matrix.shape)
        #make the inset a rectangle
        self.SECCM_fig = self.ax.imshow(self.matrix, vmin =vmin, vmax = vmax, extent = (0, self.matrix_idx_min, self.matrix_idx_min, 0), cmap = cmap)
        self.canvas.draw()

    #select a SECCM file from list
    def on_SECCM_l(self, event):
        self.SECCM_fig.remove()
        self.on_SECCM_fig()
        self.canvas.draw()

    #select a EDX.csv from list
    def on_EDX_l(self, event):
        self.EDX_file = os.path.join(self.root_path,self.EDX_l_var.get())

        self.EDX_manipulated = genfromtxt(self.EDX_file, delimiter=',')
        self.EDX_manipulated[np.where(np.isnan(self.EDX_manipulated))]= 0
        # self.EDX_manipulated = self.normalization(self.EDX_manipulated)
        self.EDX_original= self.EDX_manipulated
        self.on_rotate(event) #draw EDX
        self.on_scale()

    #override gaussian and mask
    def on_gau_mask(self, e):
        #EDX data
        filter_size = float(self.gau_var.get())
        self.EDX = gaussian_filter(self.EDX_manipulated,filter_size, mode='nearest')

        #mask
        self.EDX[np.where(self.EDX < np.quantile(self.EDX, float(self.mask_var.get())))]= np.nan
        #re-draw EDX
        self.EDX_fig.remove()

        self.limt = min(self.EDX.shape)
        self.EDX_fig = self.axin2.imshow(self.EDX[:, :], extent = (0 ,self.limt, self.limt, 0), cmap = 'jet')# EDX

        self.xcolor(self.axin2)
        self.canvas.draw()

    def on_scale(self):
        pass
        # self.zoom.append((self.scaleX_var.get(), self.scaleY_var.get()))
        # if len(self.zoom) >1:
        #     self.EDX_manipulated = ndimage.zoom(self.EDX_manipulated, zoom=[self.zoom[-1][0]/self.zoom[-2][0], self.zoom[-1][1]/self.zoom[-2][1]])
        # else:
        #     self.EDX_manipulated=ndimage.zoom(self.EDX_manipulated, zoom = self.zoom[-1])
        # self.on_gau_mask('')


    #rotate EDX
    def on_rotate(self, e):
        theta = float(self.rotate_b_var.get())
        # theta = np.radians(float(self.rotate_b_var.get()))
        self.EDX_manipulated = ndimage.rotate(self.EDX_original, theta, reshape = False)

        self.on_gau_mask(e)

    def on_gau_transparent(self, e):
        self.EDX_fig.set_alpha(self.transparent_var.get())
        self.canvas.draw()

    #override button presson
    def on_move(self, e):
        self.axin2.remove()
        if e == 'up':
            self.y0 -= 1
        elif e == 'down':
            self.y0 +=1
        elif e == 'left':
            self.x0 -= 1
        elif e == 'right':
            self.x0 +=1
        elif e == 'zoomin':
            self.width = self.width*1.02
            self.height = self.height*1.02
        elif e == 'zoomout':
            self.width = self.width/1.02
            self.height = self.height/1.02

        self.axin2 = self.ax.inset_axes([self.x0, self.y0, self.width*self.ax_xmax, self.height*self.ax_ymax], transform=self.ax.transData)
        # self.axin2.set_axes_locator(ip)
        self.EDX_fig= self.axin2.imshow(self.EDX[:, :], extent = (0 ,self.limt, self.limt, 0), cmap = 'jet')# EDX

        self.xcolor(self.axin2)
        self.canvas.draw()


    def xcolor(self, ax):
        [t.set_color('red') for t in ax.xaxis.get_ticklabels()]
        [t.set_color('red') for t in ax.yaxis.get_ticklabels()]
        ax.tick_params(axis='x', colors='red')
        ax.tick_params(axis='y', colors='red')
        ax.spines['bottom'].set_color('red')
        ax.spines['top'].set_color('red')
        ax.spines['right'].set_color('red')
        ax.spines['left'].set_color('red')

        self.axin2.patch.set_alpha(0)
        self.EDX_fig.set_alpha(self.transparent_var.get())


def main():
    root = Tk()

    # SECCM data

    ec_file = 'SECCM EDX Masking/SECCM/Sample24_L1N5_1_OER.csv'
    scan = genfromtxt(ec_file, delimiter=',')

    FigConfig_overlap(root, scan).pack(fill = 'both', expand = True)
    root.mainloop()


if __name__=='__main__':
    main()
