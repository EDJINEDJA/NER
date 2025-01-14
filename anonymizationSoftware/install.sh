#!/bin/bash
#upgrade and update linux system
echo "update and upgrade the system..."
sudo apt-get update
sudo apt-get upgrade
sleep(2)

echo "install pip..."
sudo apt install pip -y
sleep(2)

#Installing the necessary packages
echo "Installing the necessary packages..."
pip install -r LogicielAnonymization/requirements.txt

touch cronlog.log

echo "Installation finished..."
