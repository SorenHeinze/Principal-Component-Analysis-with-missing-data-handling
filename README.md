# Principal-Component-Analysis-with-missing-data-handling
A program for a very basic PCA that handles missing data correctly.

## Description
This software was written in connection with a PhD course about "Multivariate data- and meta-modelling". 
I wanted to understand the math and principles behind the Principal Component Analysis (PCA) taught there and thought: what better way then to write the software myself.

I will not go into the details what PCA is. The wikipedia article is a good starting point.
However, in very short: PCA allows to discover underlying patterns (the components) in data that may explain the distribution of the given data in a better way then just the measured variables.
What all the fancy words mean (e.g. scores, loadings, residuals etc.) you have to look up for yourself.

Many PCA modules exist for python but I couldn't find one that handles missing values the correct way without imputing them. 
In addition I wanted to have the possibility to visualize the results in 3D. 
Hence, I programmed one algorithm to get the components (NIPALs) and some common plotting possibilites for visualization.

The program was written in Python 2.7 ... because, reasons.

## How the data has to look like
- The data needs to be in one file.
- The first line of the data needs to contain the names/descriptors of the measured variables.
- The first column must contain the names/descriptors of each experiment/observation.
- The separator between the data must be a comma < , >.
- Missing data should look like this: < ,, > (so no entry between commas).
- However, all values that can NOT be converted to float will be treated as missing data.
- Everything needs to be a number! E.g. if a colour is encoded in the data don't use "blue". ... 
- ... However, variables like "colour" should not be encoded e.g. 1 for blue, 2 for green, 3 for orange. This could lead to wrong results, because why should orange have a higher value then blue. In these cases each e.g. colour needs to be it's own variable and if e.g. sample is blue it will get a 1 for the "blue"-variable and a 0 for the other colour-variables. 
This is basic PCA-stuff, but since it is so important I include this information here.    

An example:  
Sample-name,Temperature,height,green,blue  
Sample_5,123.1,456,0,1        <= A blue sample  
Sample_23,123.3,,0,1          <= Missing value here!  
Sample_42,120,15,1,0          <= A green sample    

The file random_data.txt contains lots of (more or less) random data.

ATTENTION: In physics the data is very often "the other way around" -- the samples/observations as the columns, instead of the rows. The program can handle that.  

## Usage
Copy all the python-files into one folder and simply run PCA.py (don't forget, it's written in python 2.7).
Follow the instructions on the screen. 
The program should run with the provided random_data.txt-file. 

Some remarks:
- The programmed NIPALS-algorithm is really slow, because I do all the matrix multiplications and other stuff "by hand". I needed to do that to be able to handle missing data correctly, one of the reasons why this program actually exists.
- Start with a small number of components (e.g. three). This value can not be greater then the number of variables.
- See under "How the data has to look like" (In the ATTENTION-part) what is meant with "Physics data".
- Pre-processing: This program can mean center or normalize the data. At least mean centering is usually very important.
- Enhancing: If the meaning/influence of one (two, three, etc.) variables is known, these can be enhanced to put (almost) all of it's influence into the very first (second, third, etc.) component. So the remaining components are "cleaner".
Enhancing sounds fancy, but means just multiplying the data by a (large) factor.
- The points in the data can be colour coded, if such information was provided in the colourcode.py-file.
- Probably most interesting are the explained variance, the score vs. score and loading vs. loading plots. Because these are the reasons why I did all the shebang.
- A plot needs to be closed to be able to plot the next thing. However, running the program twice, thrice, etc. allows to have two, three, etc. plots at the same time.
- 3D-plotting shows just the scores and loadings (but in 3D ... WHOA!), while in 2D-plotting more stuff (e.g. correlation loadings) can be plotted. 
- In 3D both graphs can be rotated by clicking on the left graph (and holding) and then dragging the graph around.

Some words of advice: Try to be a friendly user ;)  
I wrote this for personal use. Hence, I do not check at all places if the user-input is correct. So e.g. if characters are used when integers are required the program will stop working and you have to start again.

Have fun :)
