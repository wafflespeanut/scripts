#!/bin/bash
# Dependancies for Firefox OS
# Install Oracle Java7

sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java7-installer

update-java-alternatives -l
echo -e "You can run \"update-java-alternatives\" to update the alternatives of Java."

# Install adb and fast boot

sudo add-apt-repository ppa:nilarimogard/webupd8
sudo apt-get update
sudo apt-get install android-tools-adb android-tools-fastboot
echo -e "\e[1;31m\nBefore you proceed, 'sudo cp' the adb executables to /usr/bin/\e[0m"
echo "Press <Enter> to continue..."
read

# Rules for Android SDK on linux platform
# Edit this to include your device
sudo sh -c "echo 'SUBSYSTEM==\"usb\", ATTR{idVendor}==\"1782\", MODE=\"0666\", GROUP=\"plugdev\"
SUBSYSTEM==\"usb\", ATTR{idVendor}==\"1782\", ATTR{idProduct}==\"5d24\", \
SYMLINK+=\"spice-fireone\"\n' >> /etc/udev/rules.d/android.rules"
echo -e "\e[1;31mModify the rules to include your vendor & product ID obtained from 'lsusb'\e[0m"
sudo gedit /etc/udev/rules.d/android.rules
sudo chmod a+r /etc/udev/rules.d/android.rules
sudo service udev restart
adb kill-server
adb start-server
echo
adb devices

echo -e "\e[1;31mPlease run \"GAIA_DEVICE_TYPE=phone PRODUCTION=1 make reset-gaia\" \
from your gaia repository.\e[0m\n"
