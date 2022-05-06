import glob
import os
import shutil
import time

txtfiles = []
for file in glob.glob("pending_deployments/*"):
    txtfiles.append(file)

txtfiles = sorted (txtfiles)
for idx, file in enumerate(txtfiles):
    shutil.copy (file, '_posts/')
    os.system ('./git_commit_auto_script.sh')
    time.sleep(45)
    print (idx, file)
    break

