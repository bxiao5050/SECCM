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
from scipy import ndimage
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition
from figGUI import FigGUI
from scipy.io import loadmat

class FigConfig(FigGUI):
    def __init__(self, master, seccm_data, EDX_filepaths=None):
        super().__init__(master, seccm_data, EDX_filepaths)
        self.seccm_data = seccm_data
        self.matrix = seccm_data[self.SECCM_l_var.get()] #get the first seccm data
        self.draw_SECCM(self.matrix)

        #EDX data
        filter_size = 3
        self.EDX_file = os.path.join('SECCM EDX Masking/EDX/',self.EDX_l_var.get())
        self.EDX_withRotation = genfromtxt(self.EDX_file, delimiter=',')

        self.EDX_withRotation[np.where(np.isnan(self.EDX_withRotation))]= 0
        # self.EDX_withRotation = self.normalization(self.EDX_withRotation)

        self.EDX_noRotation= self.EDX_withRotation

        self.EDX = gaussian_filter(self.EDX_withRotation,filter_size, mode='nearest')

        self.EDX[np.where(self.EDX < np.quantile(self.EDX, 0.5))]= np.nan #mask

        #draw EDX
        self.x0, self.y0 = 0, 0
        self.ax_xmax, self.ax_ymax = max(self.ax.get_xlim())-min(self.ax.get_xlim()), max(self.ax.get_ylim())-min(self.ax.get_ylim())

        self.width, self.height = 1.05, 1.05
        self.axin2 = self.ax.inset_axes([self.x0, self.y0, self.width*self.ax_xmax, self.height*self.ax_ymax], transform=self.ax.transData)

        self.limt = min(self.EDX.shape)
        self.EDX_fig = self.axin2.imshow(self.EDX[:, :], extent = (0 ,self.limt, self.limt, 0), cmap = 'jet')# EDX
        self.xcolor(self.axin2)


        # fig.canvas.mpl_connect('button_press_event', on_click)
        def format_coord(x, y):
            try:
                Bx, By = x, y

                axin_xmax, axin_ymax = max(self.axin2.get_xlim())-min(self.axin2.get_xlim()),max(self.axin2.get_ylim())-min(self.axin2.get_ylim())

                xx= (Bx-self.x0)/self.width*axin_xmax/self.ax_xmax
                yy = (By-self.y0)/self.height*axin_ymax/self.ax_ymax

                t1 = f'SECCM: (x: {int(Bx)}, y: {int(By)}, v: {round(self.matrix[int(By)][int(Bx)], 2)})'
                t2 = f'EDX (gaussian): (x: {int(xx)}, y: {int(yy)}, v: {round(self.EDX[int(yy)][int(xx)], 2)})'
                t3 = f'EDX (original): (x: {int(xx)}, y: {int(yy)}, v: {round(self.EDX_withRotation[int(yy)][int(xx)], 2)})'
                return t1+ '                  '+t2+ '                  '+t3
            except:
                pass

        self.ax.format_coord = format_coord

    def draw_SECCM(self, matrix):

        #draw SECCM
        self.limt0 = min(self.matrix.shape)
        #make the inset a rectangle
        self.SECCM_fig = self.ax.imshow(self.matrix, extent = (0, self.limt0, self.limt0, 0), cmap = 'gray')


    def on_SECCM_fig(self, e):
        self.SECCM_fig.set_cmap(self.SECCM_cb_v.get())
        self.canvas.draw()

    #select a SECCM file from list
    def on_SECCM_l(self, event):
        self.SECCM_fig.remove()
        self.matrix = self.seccm_data[self.SECCM_l_var.get()]
        self.draw_SECCM(self.matrix)
        self.canvas.draw()

    #select a EDX.csv from list
    def on_EDX_l(self, event):
        try:
            self.EDX_file = os.path.join('SECCM EDX Masking/EDX/',self.EDX_l_var.get())
        except:
            self.EDX_file = self.EDX_l_var.get()

        self.EDX_withRotation = genfromtxt(self.EDX_file, delimiter=',')
        self.EDX_withRotation[np.where(np.isnan(self.EDX_withRotation))]= 0
        # self.EDX_withRotation = self.normalization(self.EDX_withRotation)
        self.EDX_noRotation= self.EDX_withRotation
        self.on_rotate(event) #draw EDX

    #override gaussian and mask
    def on_gau_mask(self, e):
        #EDX data
        filter_size = float(self.gau_var.get())
        self.EDX = gaussian_filter(self.EDX_withRotation,filter_size, mode='nearest')

        #mask
        self.EDX[np.where(self.EDX < np.quantile(self.EDX, float(self.mask_var.get())))]= np.nan
        #re-draw EDX
        self.EDX_fig.remove()

        self.limt = min(self.EDX.shape)
        self.EDX_fig = self.axin2.imshow(self.EDX[:, :], extent = (0 ,self.limt, self.limt, 0), cmap = 'jet')# EDX

        self.xcolor(self.axin2)
        self.canvas.draw()

    #rotate EDX
    def on_rotate(self, e):
        theta = float(self.rotate_b_var.get())
        # theta = np.radians(float(self.rotate_b_var.get()))
        self.EDX_withRotation = ndimage.rotate(self.EDX_noRotation, theta, reshape = False)

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

    FigConfig(root, scan).pack(fill = 'both', expand = True)
    root.mainloop()


if __name__=='__main__':
    main()
