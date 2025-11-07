<h1>Tephra Glass Trace Element Database</h1>
<p>This project was developed for research regarding storing the Alaskan Grubstake Tephra. The main aim for the project was creating a better way to store Tephra Glass Element Traces so that it is,</p>
<p>1. More Organized</p>
<p>2. Easily Accessible</p>
<p>3. Faster Searching and Loading of larger databases</p>
<p>4. Shift away from outdated and slow method of storing large datasets. (Excel Spreadsheets)</p>
<p>5. Reliable Interface to manipulate and convert old forms of data</p>
<h1>Languages Used: Python & SQL</h1>
<p>I decided to go with Python as a frontend and SQL for the backend. Python allowed me to easily create a gui using tkinterbootstrap, that still looks presentable to a degree compared to competiting programs. As well as aiding with my prior knowledge of using tkinter for other projects, which made it easier to get this project into an Alpha phase. SQL allowed me to store data efficiently and which can load quickly or be parsed into segments for large scale storage. I tested the validity of using SQL with large datasets and it managed to work well in an unoptimized state with up to 1.6 million entries each containing around 30 columns of data. With SQL being </p>
<h1>Standard Template</h1>
<p>The Template consists of 3 main points,</p>
<p>1. It needs to have a starting column of IntStdWv. E.X. 33.2 (float) or 33 (int)</p>
<p>2. It must have a format of {sample} - {iterate #}. E.X. NIST612 - 15, UA12 - 8</p>
<p>3. The Data must be outputted into a .csv instead of directly using .xlsx files (Excel has a csv output mode)</p>
<p>Any Columns after these two can be literally anything as it will use them in generating specific tables for each set of samples that have the same Trace Elements</p>
<p>Future versions of the program will eventually not have these requirements be as strict, but as I am on a 4 month timelimit for my research I have not developed as such.</p>
<h2>Full Example Template</h2>
<p>Headers (can be anything as the names arent directly used):</p> 
<p>IntStdWv, Sample, ... </p>
<p>33.7,NIST612 - 1, ...</p>
<p>33.7,NIST612 - 2, ...</p>
<p>32.6,NIST610 - 1, ...</p>
<h1>Installation</h1>
<h2>Releases</h2>
<a href="">here</a>
<h2>Self Building</h2>
<p>I have added an rudimentary makefile that automatically installs the required libraries for the project and then converts the python code into an executable.</p>
<h2>Prerequisutes</h2>
<p>Python 3.12 (as this is what I build the app on)</p>
<p>Make 4.3 (optional)</p>
<h2>Make Route Steps</h2>
<p>1. make install</p>
<p>2. make build</p>
<h3>OR</h3>
<p>1. make</p>
<h2>Manual Steps</h2>
<p>1. pip install requirements.txt</p>
<p>2. pyinstaller --onefile "Tephra Glass Trace Database GUI.pyw"</p>
