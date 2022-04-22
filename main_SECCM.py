from tkinter import *
from tkinter.filedialog import askopenfilenames
from tkinter import messagebox
import os
import numpy as np
from scipy.io import loadmat
from datetime import *
from view_SECCM_config import View_SECCM_config

class Main_SECCM(Frame):
    def __init__(self, master):
        super().__init__(master)

        edx_b = Button(self, text = 'import EDX.csv', command = self.on_edx_import)
        seccm_b = Button(self, text = 'import SECCM.mat', command = self.on_seccm_import)
        self.edx_l = Listbox(self, width = 30)

        self.seccm_l_var = StringVar()
        self.seccm_b =Listbox(self, width = 80, listvariable = self.seccm_l_var)
        self.seccm_b.bind('<Double-Button>', self.on_next)

        next_b = Button(self, text = 'select a SECCM data and next', command = self.on_next)

        edx_b.grid(row = 0, column =0, sticky = 'nw', padx =(5,5), pady = (5,5))
        seccm_b.grid(row = 0, column =1, sticky = 'nw', padx =(5,5), pady = (5,5))
        self.edx_l.grid(row = 1, column =0, sticky = 'nw', padx =(5,5), pady = (5,5))
        self.seccm_b.grid(row =1, column =1, sticky = 'nw', padx =(5,5), pady = (5,5))
        next_b.grid(row =2, column = 1, sticky = 'ne', padx =(5,5), pady = (5,5))
        # self.on_edx_import()
        # self.on_seccm_import()



    def on_edx_import(self):
        self.files = askopenfilenames(title = 'choose .csv data', filetypes=[('csv', '.csv')])

        # self.files = ('C:/Users/AI-PC2/Dropbox/PythonProgram/SECCM/SECCM EDX Masking/EDX/edx_summation.csv', 'C:/Users/AI-PC2/Dropbox/PythonProgram/SECCM/SECCM EDX Masking/EDX/Ir At%.csv', 'C:/Users/AI-PC2/Dropbox/PythonProgram/SECCM/SECCM EDX Masking/EDX/Pd At%.csv', 'C:/Users/AI-PC2/Dropbox/PythonProgram/SECCM/SECCM EDX Masking/EDX/Pt At%.csv', 'C:/Users/AI-PC2/Dropbox/PythonProgram/SECCM/SECCM EDX Masking/EDX/Rh At%.csv', 'C:/Users/AI-PC2/Dropbox/PythonProgram/SECCM/SECCM EDX Masking/EDX/Ru At%.csv', 'C:/Users/AI-PC2/Dropbox/PythonProgram/SECCM/SECCM EDX Masking/EDX/Si At%.csv', 'C:/Users/AI-PC2/Dropbox/PythonProgram/SECCM/SECCM EDX Masking/EDX/Ta At%.csv')



        [self.edx_l.insert(i+1, os.path.basename(f)) for i,f in enumerate(self.tk.splitlist(self.files))]
        self.EDX_filepaths = self.tk.splitlist(self.files)


    def on_seccm_import(self):
        self.SECCM_files = askopenfilenames(title = 'choose .mat data', filetypes=[('mat', '.mat')])
        # self.SECCM_files = ('C:/Users/AI-PC2/Dropbox/PythonProgram/SECCM/SECCM EDX Masking/SECCM/HEAZOOM_51nm_Scan1_ORR_21by21.mat', 'C:/Users/AI-PC2/Dropbox/PythonProgram/SECCM/SECCM EDX Masking/SECCM/Sample24_L1N5_1_OER.mat', 'C:/Users/AI-PC2/Dropbox/PythonProgram/SECCM/SECCM EDX Masking/SECCM/Sample24_L1N5_1_ORR_HER.mat')

        self.seccm_data = [] #store all SECCM data
        for i,f in enumerate(self.tk.splitlist(self.SECCM_files)):
            for k, v in loadmat(f).items():
                if type(v) is np.ndarray:
                    name = os.path.basename(f)+'  :-->  ' + k + '  :-->  '+f'{v.shape}'
                    self.seccm_b.insert(i+1, name)
                    self.seccm_data.append(loadmat(f)[k])


    def on_next(self, e=''):
        try:
            idx = self.seccm_b.curselection()[0]
        except:
            messagebox.showinfo(message = 'select a SECCM.mat data')
            return

        seccm_mat = self.seccm_data[idx]
        View_SECCM_config(Toplevel(), seccm_mat, sel_seccm_filename= self.seccm_b.get(idx), EDX_filepaths = self.EDX_filepaths)




def main():

    if datetime.today()> datetime(2025, 1, 2):
        return
    root = Tk()
    root.title('import files')

    Main_SECCM(root).pack()

    root.mainloop()

if __name__=='__main__':
    main()
