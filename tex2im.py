#!/usr/bin/env python3

from pylatex import Document, Package, Command, NoEscape

import sys, os
import io

from PIL import Image,ImageChops,ImageEnhance
from pdf2image import convert_from_path

import tkinter as tk
from tkinter import ttk

def generate_image():

    fontsize = int(font_box.get())
    dpi      = int(dpi_box.get())

    latex_input = latex_box.get('1.0','end-1c')
    latex_input = latex_input.split('\n')
    doc_class   = latex_input[0][latex_input[0].index(r'{')+1:-1]
    begin_index = latex_input.index(r'\begin{document}')
    end_index   = latex_input.index(r'\end{document}')
    
    preamble = '\n'.join(latex_input[1:begin_index])
    body     = '\n'.join(latex_input[begin_index+1:end_index])
    
    doc = Document(documentclass=doc_class,
            font_size='Huge',
            lmodern=False,
            textcomp=False)

    doc.preamble.append(NoEscape(r'%s'%preamble))
    doc.append(NoEscape(r'%s'%body))
    doc.generate_pdf('output',clean=True,clean_tex=True)
    
    im = convert_from_path('output.pdf',fmt='png')[0]
    
    try:
        os.remove('output.pdf')
    except:
        pass

    white = (255,255,255,255)
    bg = Image.new(im.mode,im.size,white)
    diff = ImageChops.difference(im,bg)
    diff = ImageChops.add(diff,diff,1.0)
    bbox = diff.getbbox()
    im = im.crop(bbox)
    
    width, height = im.size
    aspect_ratio = width/height
    print(im.size,im.size[0]/im.size[1])
    scale = fontsize/30
    width  = int(width*scale)
    height = int(width/aspect_ratio)
    im = im.convert('RGB').resize((width,height),resample=Image.LANCZOS)
    print(im.size,im.size[0]/im.size[1])
    
    im.save('output.png',quality=95,optimize=True)
    
    root.destroy()

root = tk.Tk()
root.title('Latex to Image')
root.resizable(height=False,width=False)

### Generates frame to hold equation textbox and information
eq_frame = ttk.Frame(root)
eq_frame.grid()

eq_default_prompt_list = ['\\documentclass{article}',
        '\\usepackage{amsmath}',
        '\\pagestyle{empty}',
        '\\begin{document}',
        2*'\n',
        '\\end{document}']
latex_box = tk.Text(eq_frame,width=50,height=15)
latex_box.insert('1.0','\n'.join(eq_default_prompt_list))
latex_box.grid()

for child in eq_frame.winfo_children():
    child.grid_configure(padx=5,pady=5)

### Generates frame to hold option information
options_frame = ttk.Frame(root)
options_frame.grid()

ttk.Label(options_frame,text='font size').grid()
fontsize = tk.StringVar(value=20)
font_box = ttk.Entry(options_frame,width=3,textvariable=fontsize)
font_box.grid()

ttk.Label(options_frame,text='dpi').grid()
dpi = tk.StringVar(value=1200)
dpi_box = ttk.Entry(options_frame,width=4,textvariable=dpi)
dpi_box.grid()

for child in options_frame.winfo_children():
    child.grid_configure(padx=5,pady=3)

### Generates frame to hold button information

button_frame = ttk.Frame(root)
button_frame.grid()

generate_button = ttk.Button(button_frame,text='Generate',command=generate_image)
generate_button.grid()

cancel_button = ttk.Button(button_frame,text='Cancel',command=root.destroy)
cancel_button.grid()

for child in button_frame.winfo_children():
    child.grid_configure(padx=3,pady=3)

root.mainloop()
