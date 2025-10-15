#!/bin/bash

if command -v python3 &> /dev/null; then
    echo "Python3 is installed."
else
    echo "Python3 is not installed."
    exit 1
fi

if [[ -n $(dpkg -l | grep python3-venv) ]]; then
    echo "Python3 venv is installed."
else
    echo "Python3 venv is not installed."
fi

if [ -d ./venv ]; then
    echo "Venv is present."
    . ./venv/bin/activate
else
    echo "No venv detected. Creating..."
    python3 -m venv ./venv
    . ./venv/bin/activate
fi

pip3 install --upgrade pip
pip3 install -r ./requirements.txt

echo "--------------------------------------------------------------------------------"

python3 ./src/main.py
