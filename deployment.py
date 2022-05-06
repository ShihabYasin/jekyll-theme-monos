import glob
import os

txtfiles = []
for file in glob.glob("pending_deployments/*"):
    txtfiles.append(file)


txtfiles = sorted(txtfiles)
print(txtfiles)

os.system('./git_commit_auto_script.sh')