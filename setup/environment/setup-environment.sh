#!/usr/bin/env bash

envname="calorie-estimation"
pythonversion=3.8

echo "Start creating python environment"
bash create-environment.sh $envname $pythonversion
echo "Environment created"

echo "Activate environment"
source /anaconda/etc/profile.d/conda.sh
conda activate $envname
pip install --upgrade pip
pip install ipykernel
echo "Environment activated"

echo "Start creating Notebook Kernel"
ipython kernel install --user --name $envname --display-name "Python 3.8 (calorie-estimation)"
echo "Kernel created"

echo "Install dependencies"
pip install -r requirements.txt
echo "Dependencies installed"

