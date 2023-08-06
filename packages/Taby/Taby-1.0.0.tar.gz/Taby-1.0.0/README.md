# Taby

A python package that highlights tabs in a file. 

### Features
- Easy to use
- Fast
- Efficient

### Author
This pip package was created and maintained by Landon Hutchins and Travis Mackey

### Installation
The following are the steps on how to use the Taby package.

```sh
pip install taby
```

```
#------Example Usage------#
#import package

from Taby import *

#Create a highlighter object by specifying the color of the highlight and then the 'TAB' keyword to replace all tab instances in the file.

highlighter_object = higlighter('yellow', 'TAB')

#Specify a file to be read from, a file to output, and the highlighter object
#Any file type can be read in, except for byte-like files such as PDF or JPEG

reader('inputfile.py', 'outfile.txt', highlighter_object)

#Once the output file has been written to, specify the same outfile and pass in the highlighter object so that the changes can be printed to the console. 

console('outfile.txt', highlighter_object)


#Current highlights available:
 - yellow
 - red
 - green
 - blue

```
### Contributions
This project is currently closed to contributions

### License
MIT


