#fakegovdocs-filegen

Govdocs select is one of the few datasets we have available that's 

*Public
*Provides a large enough volume to test digital workflows

I am using Govdocs at present time of writing [2016-08-08] to look at the
performance of DROID's file format identification algorithms, against tools 
for creating checksum values. There is also an opportunity to compare the
performance of Siegfried. 

##This program

This program creates a simulant version of Govdocs. That is, a set of 
randomly generated files occupying the same volume and size of Govdocs,
that is, once compiled it will:

*Create a folder called *fake_govdocs* in the working folder
*Output 259 folders, each containing 1000 files
*The files are created from a disk usage listing of the govdocs corpus the 
file: 'filsizes'
*The files are written with random values from 0x00 to 0xFF
*The output is timed, and can take in upwards of 23 minutes to complete
*The complete corpus size is 31.4GB

##Example use

The primary use of this tool is to give both Siegfried and DROID example
files where no-identification results are expected, that is, to prove that 
the tools will not expend any more time processing the files than necessary.
These results will be used in comparison to sets where DROID and Siegfried
are expected to process the collection.

##Licence

Copyright (c) 2016 Ross Spencer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to 
deal in the Software without restriction, including without limitation the 
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in 
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM
, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
THE SOFTWARE.