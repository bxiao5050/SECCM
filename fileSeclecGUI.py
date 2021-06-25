from tkinter import *
from tkinter.filedialog import askopenfilenames
from tkinter import messagebox
import os
import numpy as np
from scipy.io import loadmat

from view_SECCM_GUI import View_SECCM_GUI
from figConfig import FigConfig

class FileSeclecGUI(Frame):
    def __init__(self, master):
        super().__init__(master)

        edx_b = Button(self, text = 'import EDX.mat', command = self.on_edx_import)
        seccm_b = Button(self, text = 'import SECCM.mat', command = self.on_seccm_import)
        self.edx_l = Listbox(self, width = 30)

        self.seccm_l_var = StringVar()
        self.seccm_b =Listbox(self, width = 80, listvariable = self.seccm_l_var)
        self.seccm_b.bind('<Double-Button>', self.on_next)
        next_b = Button(self, text = 'overlap SECCM with EDX', command = self.overlap_edx_seccm, fg = 'red')

        edx_b.grid(row = 0, column =0, sticky = 'nw', padx =(5,5), pady = (5,5))
        seccm_b.grid(row = 0, column =1, sticky = 'nw', padx =(5,5), pady = (5,5))
        self.edx_l.grid(row = 1, column =0, sticky = 'nw', padx =(5,5), pady = (5,5))
        self.seccm_b.grid(row =1, column =1, sticky = 'nw', padx =(5,5), pady = (5,5))

        next_b.grid(row = 2, column = 1,padx = (5,5), pady =(15,5), sticky = 'ne')




    def on_edx_import(self):
        self.files = askopenfilenames(title = 'choose .csv data', filetypes=[('csv', '.csv')])
        [self.edx_l.insert(i+1, os.path.basename(f)) for i,f in enumerate(self.tk.splitlist(self.files))]
        self.EDX_filepaths = self.tk.splitlist(self.files)


    def on_seccm_import(self):
        self.SECCM_files = askopenfilenames(title = 'choose .mat data', filetypes=[('mat', '.mat')])

        self.seccm_data = {} #store all SECCM data
        for i,f in enumerate(self.tk.splitlist(self.SECCM_files)):
            for k, v in loadmat(f).items():
                if type(v) is np.ndarray:
                    name = os.path.basename(f)+'  :-->  ' + k + '  :-->  '+f'{v.shape}'
                    self.seccm_b.insert(i+1, name)
                    self.seccm_data[name]=loadmat(f)[k]


    def on_next(self, e=''):
        try:
            idx = self.seccm_b.curselection()[0]
        except:
            messagebox.showinfo(message = 'select a SECCM.mat data')
            return

        seccm_mat = self.seccm_data[self.seccm_b.get(idx)]
        View_SECCM_GUI(Toplevel(), seccm_mat, sel_seccm_filename= self.seccm_b.get(idx), EDX_filepaths = self.EDX_filepaths)


    def overlap_edx_seccm(self):
        w = Toplevel()
        w.title('Overlap between EDX and SCEEM figures')
        FigConfig(w, self.seccm_data, self.EDX_filepaths).pack(fill = 'both', expand = 1)


def main():
    root = Tk()
    root.title('import files')

    FileSeclecGUI(root).pack()

    root.mainloop()

if __name__=='__main__':
    main()
