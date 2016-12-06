# py-scripts
Simple Python Scripts

This repository is for python3 scripts. 

Short description of scripts is below:
* `apache-log-ip-parser.py`

  It's a script for parsing apache server logs and finding ip addresses, 
  count it and write to the `result.csv` file with header: `Ip`, `Frequency` and delimiter `,`.
  
  Name of log file passing by first command line argument of script, if there is no arguments script try
  to find `log.txt` by default.
  
  Example of using:
  ```python
  apache-log-ip-parser.py apache.log
  ```
  
