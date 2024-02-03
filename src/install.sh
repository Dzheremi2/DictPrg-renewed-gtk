#!/bin/bash

echo If you are using zsh, to init this script switch to bash
echo ""

echo Checking for PyInstaller
echo ""
pip install pyinstaller

echo Installing Dependencies
echo ""

pip install pygobject
pip install toolz

echo "Compiling via PyInstaller with --onefile argument"
echo ""

pyinstaller --onefile main.py

echo "Done, maybe"