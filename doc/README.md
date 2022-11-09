# CodeKey Alpha

# Description
CodeKey allows users to analyse code and extract metrics for the purpose of legal analysis.

The CodeKey GUI allows users unfamiliar with the scripting environment to analyse code using the graphical interface.

# Startup
Within the scripts folder, execute "./runSuite.sh" to operate the underlying functions
Within the scripts folder, execute "python -m guiScripts.codeKeyApp" to operate the GUI

# Pre-reqs
## Python Version
1. Python 3.4.4
2. PyQt 5
3. cx_Freeze 4.3.4

## External application dependencies
1. cloc 1.70
2. Understand SciTools *build (824)

## Pip
### Windows 8.1,10
1. [Install Pip](http://stackoverflow.com/questions/4750806/how-do-i-install-pip-on-windows)
2. Add pip to path, then run it with `python -m pip <rest of command>`
3. Install dependencies `python -m pip install -r requirements.txt`
