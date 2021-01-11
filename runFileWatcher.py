from folderWatcher.fileCopier import Watcher
import os
from datetime import datetime
####################################################################################################
# EDIT THIS PATH TO CORRECT LOCATION (Either Single/auto/ or Multi/auto/) - REMEMBER TO END WITH "/"
watchDir = os.path.expanduser("~/Documents/My Games/Sid Meier's Civilization VI/Saves/Single/auto/")
#                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
####################################################################################################

# Example for Epic games version
# watchDir = os.path.expanduser("~/Documents/My Games/Sid Meier's Civilization VI (Epic)/Saves/Multi/auto/")

# Use current date to autogenerate new auto save file location under /data/auto/
# You can change name after the session (when you close this program)
now = datetime.now()
dt_string = now.strftime("CIV6_%Y_%m_%d__%H_%M_%S")
targetDir = os.getcwd() + "/data/auto/" + dt_string + "/"

if __name__ == '__main__':
    print("Starting file watcher: copying auto save files from '{}' to '{}'".format(watchDir, targetDir))
    w = Watcher(watchDir, targetDir)
    w.run()

