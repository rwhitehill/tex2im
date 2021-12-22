# tex2im

### Program Requirements

To run the program the following must be installed:
1. For Python
    * os
    * sys
    * subprocess
    * Pillow
    * tkinter
2. For the command line
    * latex
    * dvipng
    * imagemagick

### Program Operation

When this program is run, a window opens where a latex script can be written. The script is converted into a latex document, and the DVI file is converted to a PNG, which is cropped and made transparent with a size corresponding to the font size. Note that all files are placed in a subdirectory titled "tex2im\_output".

A capability of the program is to regenerate images. In the program window, the absolute or relative path to the image can be typed in (or the file can be found from "Open a file" in the file explorer). Once the script and font size is reloaded, the input can be changed, and a new image replaces the old one.  

### System setup

For my systems, I placed the script into a bin file and added the bin directory to PATH, which allows the file to be run from anywhere.

Note that the file permissions must be changed so that the file is executable with something like `chmod +x tex2im.py`.

There are certain settings in the code that may be changed without changing the operation of the program. For example, the program cleans files produced converting the latex script to a DVI file. You may wish to change whether the TEX/DVI file are deleted by changing the truth value for the optional arguments in `clean_files(base,clean_dvi=True,clean_tex=True)`.

### Future changes

* Error processing
    * The program quits during certain operations when it is not ideal: for example, when the file explorer is exited during reloading.
* Image naming: it may be desirable to have the option to name the image file.
