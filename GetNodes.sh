#! /bin/bash

###
# @Author: Francis Fu
# @Date: 2023-02-20 19:56:07
# @LastEditTime: 2023-02-28 13:23:11
# @LastEditors: Francis Fu
###

# Pre-Requisite: python3, pip. Tested: Ubuntu 20.04LTS x64.

# subconverter_linux64: https://github.com/tindy2013/subconverter  v0.7.2
# lite-linux-amd64: https://github.com/xxf098/LiteSpeedTest v0.14.1


date

python3 ./utils/output.py

sleep 5

python3 ./utils/generator.py

