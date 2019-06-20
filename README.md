# Diffusion Simulator GUI

## Installation

In order to use the Diffusion Simulator, you will need to do a few things:

- Install Python 
- Install Python packages
- Compile the GoLang library (You probably don't need to do it!!)

The first two steps are very easy, and the last one will probably will not be necessary. I am writing the complete instructions here in case you are the poor soul that needs to debug something.

### Part 1 - Installing Python

Download the Python Installer from here (DONT install python using self-service):

https://www.python.org/ftp/python/3.7.3/python-3.7.3-amd64.exe

In the installtion, choose custome installation and NOT for all users. In the 'Advance Options' menu, make sure to check both "Add Python to environmetn variables" and "Associate files with Python (requires the py launcher)".

(If you want to install a different python version, make sure you download something that is 3.5+ and 64bit. If you will try to install python using self-service, you won't have premissions to install additional packages, so avoid this if possible.)

### Part 2 - Installing Python Packages

Download the Diffusion-Simulator-GUI files as a zip from the top-right corner of this webpage (clone or download -> download zip). Extract the files from the zip file somewhere on your computer. Notice you can see a file named "install.bat". (By *this* webpage, I mean : https://github.com/tomirendo/diffusion-simulator-gui)

Double click on the file named "install.bat" and wait until the installation is over. This might take 2-3 minutes.

### Part 3 - Compiling the GoLang Library

If you just want to run the GUI, you can skip this step. I'm leaving it here for future reference. Skip to Part 4 - Running the GUI.

Download the golang compiler for windows:

https://golang.org/

We will need to compile the file 'Animation/animation.go' as a 'dll' that can be used by the python code. The way to compile this as a shared library is to run:

	go build -o animation.go.dll -buildmode=c-shared animation.go

The resulting dll should be kept in the 'Animation' directory.

### Part 4 - Running the GUI

Double click on the file "gui.py", which you can find in the same directory as all the files downloaded earlier (e.g. "install.bat"). The GUI should appear.