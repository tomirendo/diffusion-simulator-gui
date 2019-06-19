# Diffusion Simulator GUI

## Installation

In order to use the Diffusion Simulator, you will need to do a few things:

- Install Python 
- Install Python packages
- Compile the GoLang library (You probably don't need to do it!!)

The first two steps are very easy, and the last one will probably will not be necessary. I am writing the complete instructions here in case you are the poor soul that need to debug something.

### Part 1 - Installing Python

Install Python3 from the Python.org website. Make sure you download a 'x86-64' (and NOT simply 'x86'). You can simply donwload an installer from here:

https://www.python.org/ftp/python/3.7.3/python-3.7.3-amd64.exe

In the installtion, in the 'Advance Options' menu, make sure to check both "Add Python to environmetn variables" and "Associate files with Python (requires the py launcher)".

### Part 2 - Installing Python Packages

Download the Diffusion-Simulator-GUI files. You can download them from this link (On the top right corner, you can download a zip file with everything. Extract the files from the zip file somewhere on your computer. Notice you can see a file named "install.bat"):

https://github.com/tomirendo/diffusion-simulator-gui

Open a Command Line Window by opening the Start key, and typing "cmd.exe". Once you find it, press Enter. A black window with White text should appear.

 Drag the file "install.bat" into the Command Line Window (after you drop it in the window, the path of 'install.bat' should appear there). Press Enter and wait until everything is done. It might take a while.

### Part 3 - Compiling the GoLang Library

If you just want to run the GUI, you can skip this step. I'm leaving it here for future reference. Skip to Part 4 - Running the GUI.

Download the golang compiler for windows:

https://golang.org/

We will need to compile the file 'Animation/animation.go' as a 'dll' that can be used by the python code. The way to compile this as a shared library is to run:

	go build -o animation.go.dll -buildmode=c-shared animation.go

The resulting dll should be kept in the 'Animation' directory.

### Part 4 - Running the GUI

Double click on the file "gui.py", which you can find in the same directory as all the files downloaded earlier (e.g. "install.bat"). A GUI should appear.


