	commit    = ""
		temp      = f.readline().strip().split("+")
		branch    = temp[0]
		if len(temp) > 1:
			commit = temp[1]
	os.system(f"git clone --depth=1 --branch={branch} {repo} newPkgs/{pkg}/")
	if len(commit) > 0:
		os.system(f"git -C newPkgs/{pkg}/ checkout {commit}")
	with open(f"newPkgs/{pkg}/.git/HEAD", mode="r") as f: