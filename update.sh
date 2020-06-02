#!/bin/bash

cd ~/.config/blender/2.83/scripts/addons/bigasterisk
git pull https://github.com/drewp/blender-addons.git
ln -sf bigasterisk/write_animation.py ../
