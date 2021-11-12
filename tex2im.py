#!/usr/bin/env python3

import os, sys
from pathlib import Path
import subprocess

from PIL import Image,ImageChops,ImageOps
from PIL.PngImagePlugin import PngImageFile, PngInfo

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


#version = '0.0.1'

class inputWindow(tk.Tk):
    
    def __init__(self):
        super().__init__()
        
        ### set cancel default to True
        self.cancel = True

        ### configuring root window
        self.title('Latex to Image')
        self.resizable(height=False,width=False)

        ### main box with latex script
        home = str(Path.home())
        if not os.path.isfile(home+'/.tex2im_template'):
            tex_template = '\n'.join(['\\documentclass{article}',
                '\\usepackage{amsmath}',
                '\\pagestyle{empty}',
                '\\begin{document}',
                2*'\n',
                '\\end{document}'])

            with open(home+'/.tex2im_template','w') as file:
                file.writelines(tex_template)

        else:
            with open(home+'/.tex2im_template','r') as file:
                tex_template = ''.join(file.readlines())

        self.script_box = tk.Text(self,width=50,height=15)
        self.script_box.insert('1.0',tex_template)
        self.script_box.grid()
       
        ### other text boxes
        self.font_label = tk.Label(self,text='font size')
        self.font_label.grid()
        self.font_size = tk.StringVar(value=20)
        self.font_box = tk.Entry(self,width=3)
        self.font_box['textvariable'] = self.font_size
        self.font_box.grid()

        ### buttons
        self.generate_button = ttk.Button(self,text='Generate')
        self.generate_button['command'] = self.get_image_info
        self.generate_button.grid()
        
        self.cancel_button = ttk.Button(self,text='Cancel')
        self.cancel_button['command'] = self.destroy
        self.cancel_button.grid()
        
        self.update_template_button = ttk.Button(self,text='Update template')
        self.update_template_button['command'] = self.update_template
        self.update_template_button.grid()
        
        ### opens window with information about program
        self.message_button = ttk.Button(self,text='Information')
        self.message_button['command'] = self.display_message
        self.message_button.grid()

        for child in self.winfo_children():
            child.grid(padx=5,pady=5)
    
    def display_message(self):
        message = 'This is a program that converts short latex scripts to an image.'
        messagebox.showinfo('Information',message)

    def update_template(self):
        new_template = self.script_box.get('1.0','end-1c')

        with open(str(Path.home())+'/.tex2im_template','w') as file:
            file.writelines(new_template)
    
    def get_image_info(self):
        self.cancel = False
        global latex_script, fontsize
        latex_script = self.script_box.get('1.0','end-1c')
        fontsize = float(self.font_box.get())
        
        self.destroy()

def get_unique_name(file_name):
    if os.path.isfile(file_name):
        suffix = 1
        dot_index = file_name.index('.')
        while True:
            temp = file_name[:dot_index] + str(suffix) + file_name[dot_index:]
            if os.path.isfile(temp):
                suffix += 1
            else:
                file_name = temp
                break

    return file_name

def clean_files(base,clean_dvi=True,clean_tex=False):
    file_types = ['aux','log']
    if clean_dvi:
        file_types.append('dvi')
    if clean_tex:
        file_types.append('tex')

    for file_type in file_types:
        try:
            os.remove(base+file_type)
        except:
            continue

def get_dpi(fontsize):
    return fontsize*96/72*72.27/10

def write_script_to_metadata(file_name,latex_script,fontsize):
    image = PngImageFile(file_name)
    metadata = PngInfo()
    metadata.add_text('Script',latex_script)
    metadata.add_text('Font Size',str(fontsize))
    image.save(file_name,pnginfo=metadata)

if __name__ == '__main__':
    
    root = inputWindow()    
    root.mainloop()
    
    if not root.cancel:
    
        file_name = get_unique_name('output.tex')
        
        with open(file_name,'w') as file:
            file.writelines(latex_script)
        
        latex_cmd = 'latex %s'%file_name
        res = subprocess.run(latex_cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        
        base = file_name[:file_name.index('.')+1]
        dpi = get_dpi(fontsize)
        convert_dvi_cmd = 'dvipng %s -o %s -T "tight" -D %d'%(base+'dvi',base+'png',dpi)
        res = subprocess.run(convert_dvi_cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        
        clean_files(base,clean_dvi=True,clean_tex=False)
        write_script_to_metadata(base+'png',latex_script,int(fontsize))
        


