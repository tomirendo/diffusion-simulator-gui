# Diffusion Simulator GUI

## Installation

In order to use the Diffusion Simulator, you will need to do a few things:

- Install Python 
- Install Python packages
- Compile the GoLang library (You probably don't need to do it!!)

The first two steps are very easy, and the last one will probably will not be necessary. I am writing the complete instructions here in case you are the poor soul that need to debug something.

### Part 1 - Installing Python

For various reasons, you don't want to install python directly on Windows. The easiest way to install Python is to install some kind of python distribution, like Anaconda (Python 3.7 or above):

https://www.anaconda.com/distribution/#download-section

### Part 2 - Installing Python Packages

Download the Diffusion-Simulator-GUI files. You can download them from here:

https://github.com/tomirendo/diffusion-simulator-gui

On the top right corner, you can download a zip file with everything. Extract the files from the zip file somewhere on your box. Notice you can see a file named "install.bat".

Open the Anaconda Prompt (Press Start, and start typing Anaconda until it shows up). Drag the file "install.bat" into the Anaconda Prompt windows (after you drop it in the window, the path of 'install.bat' should appear there). Press Enter and wait. It might take a while.

### Part 3 - Compiling the GoLang Library

You probably can skip this step. I'm leaving it here for future reference. Skip to Part 4 - Running the GUi

Download the golang compiler for windows:

https://golang.org/

We will need to compile the file 'Animation/animation.go' as a 'dll' that can be used by the python code. The way to compile this as a shared library is to run:

	go build -o animation.go.dll -buildmode=c-shared animation.go

### Part 4 - Running the Gui


