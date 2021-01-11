import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.utils.dirsnapshot import DirectorySnapshot
from shutil import copy2
import os

autoRunBat = "./folderWatcher/autoRunEndGameReplayHere.bat"


class Watcher:

    def __init__(self, watchDir, targetDir, copyAutoRunBat=True, fileExt=".Civ6Save", recursive=False):
        self.observer = Observer()
        self.event_handler = Handler(watchDir, targetDir, copyAutoRunBat, fileExt, recursive)
        self.observer.schedule(self.event_handler, watchDir, recursive=recursive)

    def run(self):
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()

        self.observer.join()


class Handler(FileSystemEventHandler):

    def __init__(self, watchDir, targetDir, copyAutoRunBat, fileExt, recursive):
        self.watchDir = watchDir
        self.targetDir = targetDir
        self.recursive = recursive
        self.fileExt = fileExt
        self.snapshot = DirectorySnapshot(self.watchDir, self.recursive)
        if not os.path.exists(targetDir):
            os.makedirs(targetDir)
        for path in self.snapshot.paths:
            if fileExt == os.path.splitext(path)[1]:
                copy2(path, os.path.join(self.targetDir, os.path.basename(path)))
        if copyAutoRunBat:
            copy2(autoRunBat, os.path.join(self.targetDir, os.path.basename(autoRunBat)))
            print(f"\nAfter the game, you can run the endGameReplay.py by double clicking\n"
                  f"autoRunEndGameReplayHere.bat from the target folder:\n'{targetDir}'\n")

    def on_any_event(self, event):
        self.snapshot = DirectorySnapshot(self.watchDir, self.recursive)
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print("Received created event - %s." % event.src_path)
            copy2(event.src_path, self.targetDir)

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print("Received modified event - %s." % event.src_path)
            copy2(event.src_path, self.targetDir)