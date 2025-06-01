
# **Installing BCC (BPF Compiler Collection) on Ubuntu 24.04 with Python Virtual Environment** For JAMJAR

  

This guide provides steps to install [BCC](https://github.com/iovisor/bcc/blob/master/INSTALL.md) from source on **Ubuntu 24.04** using a **Python virtual environment** instead of system-wide installation.

---

## **🔧 Prerequisites**

You need Ubuntu version - 24.04

Before starting, make sure you have the following installed:

```
sudo apt update
sudo apt upgrade
sudo apt install -y unzip zip bison build-essential cmake flex git libedit-dev \
  libllvm18 llvm-18-dev libclang-18-dev python3 zlib1g-dev libelf-dev libfl-dev python3-setuptools \
  liblzma-dev libdebuginfod-dev arping netperf iperf libpolly-18-dev
```

These packages are internally used by bcc's dependencies and will be installed in ubuntu by default and will create issues when you are building bcc.

```
sudo apt install libcurl4--openssl-dev liblaujit-5.1-dev
```
---

## **📦 Installation Steps**
### **1. Clone JamJar from Github**

```
git clone https://www.github.com/hashedalgorithm/JamJar.git
```
### **2. Create a Python Virtual Environment**

```
python3 -m venv ~/JamJar/jamjar-venv
```

This ensures that Python bindings for BCC are installed in an isolated environment.

Activate the virtual environment (if not already):

```
source ~/JamJar/jamjar-venv/bin/activate
```


---

### **3. Clone the BCC Repository**

```
git clone https://github.com/iovisor/bcc.git
cd bcc
```

---

### **4. Change Folder Ownership (Recommended for Virtualized/Root-Owned Folders)**

If you’re using a virtual machine or ran git clone with sudo, you may need to change the folder’s ownership:

```
sudo chown -R $(whoami):$(whoami) .
```

---

### **5. Create and Enter the Build Directory**

```
mkdir build
cd build
```

---

### **6. Build and Install BCC Core**

```
cmake ..
make $(nproc)
make install
```

> ⚠️ If you are getting errors then the reason for it would be ownership issues with the folder.
---

### **7. Install Python Dependencies (for your venv)**
```
pip install six setuptools ipcalc build
```

### **8. Installing ptrace(0.9.9 stable) from source**

```
// Go to ~/JamJar
wget https://github.com/vstinner/python-ptrace/archive/refs/tags/0.9.9.zip
unzip python-ptrace0.9.9.zip
cd python-ptrace0.9.9/
```

```
python3 -m build
``` 
This creates a .whl file in the dist/ directory.

```
pip install dist/*.whl
```

### **9. Build and Install Python Bindings (for your venv)**

From within the build directory:

```
cmake -DPYTHON_CMD=python3 ..
pushd ../src/python
make $(nproc)
python3 setup.py install
popd
```

> ⚠️ **Do not use sudo make install here**, since you’re installing in a virtual environment.

---

## **✅ Verifying Installation**

Try running a sample Python program using BCC:

```
ubuntu@VM:~$ python3
Python 3.12.3 (main, Feb  4 2025, 14:48:35) [GCC 13.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from bcc import BPF
>>> import ptrace
>>> 

```

If this prints without errors, BCC is ready to use. If throws error in either of these you just to make, build and install again. 

> 🤩 Tip : Check the make logs and verify that everything is installed correctly
---

## **🧹 Cleanup (Optional)**

If you no longer need the source or build artifacts:

```
rm -rf ~/JamJar/bcc
rm -rf ~/JamJar/python-ptrace0.9.9
rm -r ~/JamJar/python-ptrace0.9.9.zip
```

---

## **🍯 Running JamJar**

JamJar needs su permissions to work hence it handles with kernal operations. even if you try to run it sudo it doesn't work. Hence we need root shell. To obtain root shell in ubuntu

### **👤 Change Password of Root User**

```
ubuntu@VM:~$ sudo passwd root
[sudo] password for ubuntu: 
New password: 
Retype new password: 
passwd: password updated successfully
```

### **🦾 Get Root Shell**

```
ubuntu@VM:~$ su
Password: 
root@VM:/home/ubuntu# 
```

Now navigate to JamJar and activate your venv and  run main.py
```
cd ~/JamJar
source jamjar-venv/bin/activate
python3 main.py
```

> ⚠️ If you came across any error like module not found try to install it using pip(except for bcc and ptrace).


---
