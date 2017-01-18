#pnc-cli
A python CLI around the PNC REST API

Installation:
 * python setup.py install --user
 
Usage:
 * Configure the REST endpoint for PNC in USER_HOME/.config/pnc-cli/pnc-cli.conf
 * pnc -h for a list of valid operations.

Currently outputs the raw JSON. More refined output is definitely in the works :) 

#Tests

Requirements:
 * py.test (pip install pytest)
 * mock (pip install mock)
 * GitPython (pip install GitPython)

Run any of the testing scripts to see results. The tested instance is configured by the local file ~/.config/pnc-cli/pnc-cli.conf 
