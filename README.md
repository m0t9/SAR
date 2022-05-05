# SAR (System App Remover) - this is an application which can help with uninstalling system programs on Your Android-device.

## <ins>Installation</ins>

### Debug version
You should download and unzip this repository to desired folder, open it.

#### *For Windows users*
* You need to install the adb drivers via `DriverInstaller.msi`. Just launch it.

#### *For Linux users*
* You should install adb on your PC using `sudo apt install adb` command in terminal.

### Release version

#### *For Windows users*
* You need to install the archive with executable application from https://disk.yandex.ru/d/y8AMJWp6nV0VxA

## <ins>Preparing your phone</ins>

The next step is to enable **developer mode** on your phone. Through it, you must enable **USB-debugging**.
Connect your device to your computer using USB cable.

## <ins>Running the program</ins>

* Install the required modules using the `pip3 install -r requirements.txt` command in terminal in folder with program.
* Run the program using the `python3 main.py` command in terminal in folder with *SystemAppRemover*.
* Choose your phone model in corresponding menu, apps, which you want remove (a second click on the application will remove it from the list) and press "Remove" button. After completing the removal process, the results will be displayed in the log.

**All actions You perform at Your own peril and risk.**
