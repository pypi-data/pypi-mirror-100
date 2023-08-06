# anonfiles.py
Simple AnonFiles.com API Wrapper written on Python3

BayFiles is also added and supported.

## Install

    $ pip3 install anonfiles-py

## Usage
```python3
from anonfiles import AnonFiles 

# BayFiles is also available and can be used similarly.
# `from anonfiles import BayFiles`

a = AnonFiles()

up = a.upload("example.py")

print(up.status)
```


##
### &copy; 2021 TheBoringDude