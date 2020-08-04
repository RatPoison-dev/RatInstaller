import subprocess, string, random, requests, zipfile, os, glob, shutil, pygit2
from clint.textui import progress

def downloadFileWithBar(path, link):
    r = requests.get(link, stream=True)
    with open(path, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
            if chunk:
                f.write(chunk)
                f.flush()

def searchDir(path):
    for file in os.listdir():
        if (path in file):
            return True
    return False

for file in glob.glob("version.txt"):
    # Autoupdate
    with open(file) as f:
        c = f.readlines()
        origin_version = c[0].replace("\n", "")
        origin_branch = c[1].replace("\n", "")
        r = requests.get(f"https://raw.githubusercontent.com/TheFuckingRat/RatPoison/{origin_branch}/version.txt")
        remote_text = r.text.split("\n")
        remote_version = remote_text[0]
        if (remote_version != origin_version):
            print("Versions doesn't match. Redownloading RatPoison")
            new_path = f"RatPoison-{origin_branch}/"
            pygit2.clone_repository(f"https://github.com/TheFuckingRat/RatPoison.git", new_path, checkout_branch=origin_branch)
            if (searchDir("jdk")):
                shutil.move("jdk-14.0.2", new_path)
            os.chdir(f"RatPoison-{origin_branch}/")
    break

JDK_LINK = "https://download.java.net/java/GA/jdk14.0.2/205943a0976c4ed48cb16f1043c5c647/12/GPL/openjdk-14.0.2_windows-x64_bin.zip"
JDK_ZIP_NAME = "JDK.zip"

def getRandomName():
    s = ""
    for _ in range(10):
        s += random.choice(string.ascii_uppercase)
    return s

if (not searchDir("jdk")):
    print("Downloading JDK...")
    downloadFileWithBar(JDK_ZIP_NAME, JDK_LINK)
    with zipfile.ZipFile(JDK_ZIP_NAME) as zip_ref:
        zip_ref.extractall("")
    # Set JAVA_HOME and PATH
    os.environ["JAVA_HOME"] = os.path.join(os.getcwd(), "jdk-14.0.2")
    os.environ["PATH"] = os.environ["PATH"]+";"+os.path.join(os.environ["JAVA_HOME"], "bin")

# BUILD
print("Building RatPoison...")
subprocess.run(["gradlew.bat", "RatPoison"])
if (input() in ["y", "yes"]):
    random_name = getRandomName()
    for d in os.listdir("build/"):
        if ("RatPoison" in d):
            for file in os.listdir(f"build/{d}"):
                path = f"build/{d}/{file}"
                if (os.path.isfile(path)):
                    ext = os.path.splitext(file)[1]
                    os.rename(path, f"build/{d}/{random_name}{ext}")