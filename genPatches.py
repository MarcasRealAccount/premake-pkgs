import os
import datetime

for pkg in os.listdir("newPatches"):
	path      = "newPatches/" + pkg
	repo      = ""
	branch    = ""
	commit    = ""
	committer = ""
	with open(path + "/info.txt", mode="r") as f:
		repo      = f.readline().strip()
		temp      = f.readline().strip().split("+")
		branch    = temp[0]
		if len(temp) > 1:
			commit = temp[1]
		committer = f.readline().strip()
	print(f"{repo}\n{branch}\n{committer}")
	os.system(f"git clone --depth=1 --branch={branch} {repo} newPkgs/{pkg}/")
	if len(commit) > 0:
		os.system(f"git -C newPkgs/{pkg}/ checkout {commit}")
	latestCommit = ""
	with open(f"newPkgs/{pkg}/.git/HEAD", mode="r") as f:
		latestCommit = f.readline().strip()
	now             = datetime.datetime.now()
	patch           = f"From {latestCommit} Mon Sep 17 00:00:00 2001\nFrom: {committer}\nDate: {now:%a, %d %b %Y %H:%M:%S %z}\nSubject: [PATCH] Add premake scripts :>\n\n---\n"
	patchHeader     = ""
	patchHeaderEnd  = ""
	patchBody       = ""
	totalFileCount  = 0
	totalInsertions = 0
	for f in os.listdir(path):
		if f == "info.txt":
			continue
		plusses     = ""
		fileContent = ""
		lineCount   = 0
		with open(path + "/" + f) as ff:
			totalFileCount += 1
			for line in ff:
				fileContent     += '+' + line.rstrip() + '\n'
				lineCount       += 1
				plusses         += "+"
				totalInsertions += 1
			if lineCount == 0:
				lineCount        = 1
				fileContent      = "+\n"
				plusses          = "+"
				totalInsertions += 1
		patchHeader    += f" {f} | {lineCount} {plusses}\n"
		patchHeaderEnd += f" create mode 100644 {f}\n"
		patchBody      += f"diff --git a/{f} b/{f}\nnew file mode 100644\n--- /dev/null\n+++ b/{f}\n@@ -1,0 +1,{lineCount} @@\n{fileContent}\\ No newline at end of file\n"
	patch += f"{patchHeader} {totalFileCount} files changed, {totalInsertions} insertions(+)\n{patchHeaderEnd}\n{patchBody}"
	patch += "--\n2.38.1.windows.1"
	with open(f"patches/pkg-{pkg}.patch", mode="w") as f:
		f.write(patch)