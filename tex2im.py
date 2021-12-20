#!/usr/bin/env python3

import os, sys
from pathlib import Path
import subprocess

from PIL import Image,ImageChops,ImageOps
from PIL.PngImagePlugin import PngImageFile, PngInfo

import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk


#version = '0.0.1'

class inputWindow(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.cancel      = True
        self.regenerated = False
        self.home = str(Path.home())

        self.display_window()

    def display_window(self):
        ### configuring root window
        self.title('Latex to Image')
        self.resizable(height=False,width=False)
        
        ### prompt for regenerating image
        self.file_frame = tk.Frame(self)
        self.file_frame.grid()
        
        self.regenerate_prompt = tk.Entry(self.file_frame,width=50)
        self.regenerate_prompt.grid(row=0,column=0,columnspan=4)

        self.file_explorer = ttk.Button(self.file_frame,text='Open a File')
        self.file_explorer['command'] = self.select_file
        self.file_explorer.grid(row=1,column=1)

        self.regenerate_button = ttk.Button(self.file_frame,text='Reload')
        self.regenerate_button['command'] = self.load_image_info
        self.regenerate_button.grid(row=1,column=2)
        
        for child in self.file_frame.winfo_children():
            child.grid(padx=1,pady=5)

        ### main box with latex script
        if not os.path.isfile(self.home+'/.tex2im_template'):
            tex_template = '\n'.join(['\\documentclass{article}',
                '\\usepackage{amsmath}',
                '\\pagestyle{empty}',
                '\\begin{document}',
                2*'\n',
                '\\end{document}'])

            with open(self.home+'/.tex2im_template','w') as file:
                file.writelines(tex_template)

        else:
            with open(self.home+'/.tex2im_template','r') as file:
                tex_template = ''.join(file.readlines())

        self.script_frame = tk.Frame(self)
        self.script_frame.grid()
        
        self.script_box = tk.Text(self.script_frame,width=50,height=15)
        self.script_box.insert('1.0',tex_template)
        self.script_box.grid(row=2,column=0,columnspan=3)

        for child in self.script_frame.winfo_children():
            child.grid(padx=5,pady=5)
       
        ### other text boxes
        self.font_frame = tk.Frame(self)
        self.font_frame.grid()
        
        self.font_label = tk.Label(self.font_frame,text='font size')
        self.font_label.grid(row=3,column=0)
        #self.font_size = tk.StringVar(value=20)
        self.font_box = tk.Entry(self.font_frame,width=3)
        self.font_box.insert(0,'20')
        #self.font_box['textvariable'] = self.font_size
        self.font_box.grid(row=3,column=1)

        for child in self.font_frame.winfo_children():
            child.grid(padx=5,pady=5)
        
        ### buttons
        self.button_frame = tk.Frame(self)
        self.button_frame.grid()
        
        self.generate_button = ttk.Button(self.button_frame,text='Generate')
        self.generate_button['command'] = self.get_image_info
        self.generate_button.grid(row=4,column=2)
        
        self.cancel_button = ttk.Button(self.button_frame,text='Cancel')
        self.cancel_button['command'] = self.destroy
        self.cancel_button.grid(row=4,column=1)
        
        self.update_template_button = ttk.Button(self.button_frame,text='Update template')
        self.update_template_button['command'] = self.update_template
        self.update_template_button.grid(row=4,column=0)

        for child in self.button_frame.winfo_children():
            child.grid(padx=5,pady=5)
        ### opens window with information about program
        #self.message_button = ttk.Button(self,text='Information')
        #self.message_button['command'] = self.display_message
        #self.message_button.grid()

    
    
    def load_image_info(self):
        self.regenerated = True
    
        file_path = self.regenerate_prompt.get() 
        image     = PngImageFile(file_path)
        metadata = image.text
        
        self.script_box.delete('1.0','end')
        self.script_box.insert('1.0',metadata['Script'])

        self.font_box.delete(0,'end')
        self.font_box.insert(0,metadata['Font Size'])
        
        global base
        base = ''.join(os.path.splitext(file_path)[:-1])

    def select_file(self):
        self.file_types = [("PNG", "*.png")]
        self.file_path = filedialog.askopenfilenames(parent=self,filetypes=self.file_types)

        self.regenerate_prompt.delete(0,'end')
        self.regenerate_prompt.insert(0,self.file_path[0])

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
    file_types = ['.aux','.log']
    if clean_dvi:
        file_types.append('.dvi')
    if clean_tex:
        file_types.append('.tex')

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
        
        if not os.path.isdir('tex2im_output'):
            os.mkdir(os.path.join(os.getcwd(),'tex2im_output'))
        
        os.chdir(os.path.join(os.getcwd(),'tex2im_output'))

        if not root.regenerated:
            base = get_unique_name('output.png')
            base = base[:base.index('.')]
       
        with open(base+'.tex','w') as file:
            file.writelines(latex_script)
        
        latex_cmd = 'latex %s'%(base+'.tex')
        res = subprocess.run(latex_cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        
        dpi = get_dpi(fontsize)
        convert_dvi_cmd = 'dvipng %s -o %s -T "tight" -D %d'%(base+'.dvi',base+'.png',dpi)
        res = subprocess.run(convert_dvi_cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        
        clean_files(base,clean_dvi=True,clean_tex=True)
        write_script_to_metadata(base+'.png',latex_script,int(fontsize))
