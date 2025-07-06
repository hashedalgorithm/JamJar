
# **JamJar Installation Guide (Ubuntu 24.04 + Python Virtual Environment)**

This guide covers installing the [BPF Compiler Collection (BCC)](https://github.com/iovisor/bcc/blob/master/INSTALL.md) from source on **Ubuntu 24.04** inside a **Python virtual environment**, including troubleshooting common installation issues.
  

---

## **🔧 Prerequisites**

Make sure your system is Ubuntu 24.04 or similar.

Update and install system packages:

```
sudo apt update && sudo apt upgrade -y
sudo apt install -y unzip zip bison build-essential cmake flex git libedit-dev \
libllvm18 llvm-18-dev libclang-18-dev python3 zlib1g-dev libelf-dev libfl-dev python3-setuptools \
liblzma-dev libdebuginfod-dev arping netperf iperf libpolly-18-dev libcurl4-openssl-dev libluajit-5.1-dev

```

These packages are needed for building BCC and its dependencies.

```

---

## **🧹 Cleanup (Start fresh)**

If you've attempted installation before and want to start clean, remove these folders and files:

rm -rf ~/JamJar/bcc
rm -rf ~/JamJar/python-ptrace-0.9.9
rm -rf ~/JamJar/0.9.9.zip
rm -rf ~/JamJar/jamjar-venv

---

## **📦 Installation Steps**
### **1. Clone JamJar Repository from Github

```
git clone https://github.com/hashedalgorithm/JamJar.git
cd JamJar
```
---

### **2. Create and activate Python virtual environment**

```
python3 -m venv jamjar-venv
source jamjar-venv/bin/activate
```

This ensures that Python bindings for BCC are installed in an isolated environment.

---

### **3. Clone the BCC Repository**

```
git clone https://github.com/iovisor/bcc.git
cd bcc
```

---

### **4. Fix folder ownership (if cloned with sudo or running in VM)**

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

### **6. Install Python Dependencies (inside venv)**

```
pip install six setuptools ipcalc build
```

> ⚠️ If permission or dependency errors arise, check folder ownership and your virtual environment activation.

---

### **7. Build and Install BCC Core**

```
cmake ..
make -j$(nproc)
sudo make install
```

> **Note:** sudo is needed here because installing to /usr/lib requires root permissions.

---

### **8. Build and Install Python Bindings (for your venv)**

From within the build directory:

```
cd ../bcc
cmake -DPYTHON_CMD=python3 .
cd src/python
make -j$(nproc)
python3 setup.py install
```

> ⚠️ **Important:** Do NOT run sudo make install here; the Python bindings must install in the virtual environment.

---

## **✅ Verifying Installation**

Activate your virtual environment and run:

```
python3 -c "from bcc import BPF; print('✅ BCC Python bindings installed!')"

```

If this prints without errors, BCC is ready to use.

> 🤩 Tip : Check the make logs and verify that everything is installed correctly

---

## **🚩 Common Issues and Solutions**
### **1. ModuleNotFoundError: No module named 'bcc.version'**

Cause: version.py file missing in bcc/ directory.

Fix: Create a version.py in bcc/ with the following content:

```
__version__ = "0.35.0"
```

Confirm your current directory is the root of BCC Python source (bcc/src/python/) when running Python commands.

---

### **2. Permission Denied on make install for BCC core libraries**

Cause: You need root permission to install shared libraries into /usr/lib.

Fix: Use sudo make install during core BCC installation.

---

### **3. Errors during pip install or building Python bindings**

Cause: Folder ownership issues or missing dependencies.

Fix: Ensure the entire BCC repo directory is owned by your user:

```
sudo chown -R $(whoami):$(whoami) ~/JamJar/bcc
```

Make sure your Python virtual environment is activated before installing.

---

### **4. Bash error: bash: !': event not found when running python -c with exclamation marks**

Cause: Bash interprets ! as history expansion.

Fix: Use single quotes instead of double quotes or escape !:

```
python3 -c 'from bcc import BPF; print("✅ BCC installed!")'
```

Make sure your Python virtual environment is activated before installing.

---

## **🍯 Running JamJar**

JamJar requires root privileges due to kernel operations.

1. Set root password:
```
sudo passwd root

```

> ⚠️ If you came across any error like module not found try to install it using pip(except for bcc and ptrace).

2. Switch to root shell: 
```
su
```

3. Navigate to JamJar, activate venv and run: 
```
cd ~/JamJar
source jamjar-venv/bin/activate
python3 main.py
```

> ⚠️ If you came across any error like module not found try to install it using pip(except for bcc and ptrace).

---

## **🧹 Cleanup (Optional)**

If you no longer need the source or build artifacts:

```
sudo rm -rf ~/JamJar/bcc
```