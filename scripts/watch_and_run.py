import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ScriptReloader(FileSystemEventHandler):
    def __init__(self, script):
        self.script = script
        self.process = None
        self.restart_script()

    def restart_script(self):
        if self.process:
            self.process.terminate()
        print(f"Starting {self.script}...")
        self.process = subprocess.Popen(['python', self.script])

    def on_modified(self, event):
        if event.src_path.endswith(self.script):
            print(f"\nDetected change in {self.script}, reloading...")
            self.restart_script()

if __name__ == "__main__":
    script_to_run = "tkintergui.py"
    path = "."  # <- Watch current directory (where tkintergui.py is)

    event_handler = ScriptReloader(script=script_to_run)
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
