import objc
import subprocess
from Cocoa import NSApplication, NSStatusBar, NSVariableStatusItemLength, NSMenu, NSMenuItem
from Foundation import NSObject, NSTimer
import psutil

class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        # Create the status bar item
        self.status_item = NSStatusBar.systemStatusBar().statusItemWithLength_(NSVariableStatusItemLength)
        self.status_item.setTitle_("Loading...")

        # Create a quit option in the menu
        self.menu = NSMenu.alloc().init()
        quit_menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Quit", "terminate:", "")
        self.menu.addItem_(quit_menu_item)
        self.status_item.setMenu_(self.menu)

        # Start a timer to update the status
        self.timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            1.0, self, "updateStatus:", None, True
        )

    def updateStatus_(self, timer):
        # Get CPU and RAM usage
        cpu_usage = psutil.cpu_percent(interval=0.1)
        memory_info = psutil.virtual_memory()
        memory_usage = memory_info.percent
        command = "sudo powermetrics --samplers smc | grep -i 'CPU die temperature'"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Command was successful, and the output is in result.stdout
        temp = result.stdout
        
        # Update the status bar title
        self.status_item.setTitle_(f"CPU: {cpu_usage:.1f}% | RAM: {memory_usage:.1f}% | Temp: {temp}")

if __name__ == "__main__":
    app = NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    app.setDelegate_(delegate)
    app.run()

