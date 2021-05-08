
<h3>RatInstaller</h3>

<div>

[![deepcode](https://www.deepcode.ai/api/gh/badge?key=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF0Zm9ybTEiOiJnaCIsIm93bmVyMSI6InJldGFydDEzMzciLCJyZXBvMSI6IlJhdEluc3RhbGxlciIsImluY2x1ZGVMaW50IjpmYWxzZSwiYXV0aG9ySWQiOjE3MTM5LCJpYXQiOjE2MDI2NzgyODh9.-C-yDHV8eJ5FOOXsoSOWC2YrQClgHXz7WnJYMcK-RnI)](https://www.deepcode.ai/app/gh/retart1337/RatInstaller/_/dashboard?utm_content=gh%2Fretart1337%2FRatInstaller)
[![Release](https://img.shields.io/github/v/release/retart1337/RatInstaller.svg)](https://github.com/retart1337/RatInstaller/releases/)
![LOC](https://tokei.rs/b1/github/SPRAVEDLIVO/RatInstaller?category=code)

</div>

---

<p> Installer for RatPoison
    <br> 
</p>

## 📝 Table of Contents

- [How to compile](#compilation)
- [Usage](#usage)
- [Authors](#authors)
- [Settings](#settings)

## 🏁 Compilation <a name = "compilation"></a>

First of all, clone this repository and install [python](https://www.python.org/downloads/release/python-385/).
Then execute 
```
pip3 install -r requirements.txt
```
and 
```
pyinstaller --onefile installer.py --icon=data/1.ico
```
If build was successfully, you will find ``installer.exe`` file in ``dist/`` folder

## 🎈 Usage <a name="usage"></a>

Place compiled build to ``RatPoison`` folder

## Settings <a name="settings">

Settings are located in ``installerSettings.json`` file

**Description**

``force_install_jdk`` - When true, installer will download jdk even when it is already installed or already downloaded

``force_cheat_update`` - When true, installer will download and install update without asking for your input when update is needed

``force_cheat_compile`` - When true, installer will compile cheat even when it is already compiled

``download_missing_files`` - When true, installer will diff your files with commit/branch, find missing and download

``update_type`` - When ``call_installer``, installer will call downloaded installer, otherwise will make everything itself (debugging usage)

``build_folder`` - Name of build folder

``jdk_zip_name`` - Installer will save downloaded JDK under this name

``github_repo`` - Repository where to check and download updates

``settings_directory`` - Name of settings folder

``bypass_download`` - When true, installer wont download new update folder and search for downloaded one

``jdk_link`` - Link to download JDK from

## ✍️ Authors <a name = "authors"></a>

- [@SPRAVEDLIVO](https://github.com/SPRAVEDLIVO) - Main author
