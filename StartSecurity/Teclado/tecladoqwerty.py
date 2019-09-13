import subprocess
import platform

class keyboard_mixin(object):
    def __init__(self):
        self.keyboard_process = None

    def show(self):
        if platform.system() == "Linux":
            try:
                cmd_path = "xvkbd"
                self.keyboard_process = subprocess.Popen([cmd_path])
                return
            except OSError:
                pass

        elif platform.system() == "Windows":
            try:
                cmd_path = "C:\\Program Files\\Common Files\\Microsoft Shared\\ink\\TabTip.exe"
                self.keyboard_process = subprocess.Popen([cmd_path], shell=True)
                return
            except OSError:
                pass

            try:
                cmd_path = "C:\\WINDOWS\\system32\\osk.exe"
                self.keyboard_process = subprocess.Popen([cmd_path], shell=True)
                return
            except OSError:
                pass

    def hide(self):
        # TODO: This does not close on windows platform
        if self.keyboard_process is not None:
            self.keyboard_process.terminate()
            self.keyboard_process = None

if __name__ == '__main__':
    osk = keyboard_mixin()
    osk.show()
