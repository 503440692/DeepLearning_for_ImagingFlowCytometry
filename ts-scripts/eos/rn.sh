#!/bin/bash
cd /home/maximl/workdir/basic_nn

source venv/bin/activate
python main.py cv configs/eos/cv-3-resnet18.json ~/runs/simple_nn/eos/resnet18/s23 ~/IFC/data/
