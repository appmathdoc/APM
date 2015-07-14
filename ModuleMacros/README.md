IPNmacros
=========

IPython Notebook Macros:  Python files to be used as macros in the IPython Notebook


Each file is a .py file that can be loaded as a macro in an Ipython notebook.  For example, the subeconomy problem generator is 

subeconomy.py

In the IPython notebook, executing 

%macro -q  MakeSubEconData  https://github.com/appmathdoc/IPNmacros/raw/master/subeconomy.py

generates a macro called MakeSubEconData, which upon execution creates simulated data and loads it as a pandas dataframe.

