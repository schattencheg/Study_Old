import sys
import os
import re
import glob
import fileinput
import shutil
from tqdm import tqdm

d = dict()
d['a'] = 1


class Changer:
    constA = b"xkzS1Lpl3f7"#"2374849e"
    constS = b"A93wDw45Vb7"#"2194943e"
    constM = b"oSJulLlHil7"#
    SToAOrAToS = "AllToM"

    def __init__(self, args):
        self.prefix = "orno"
        self.prefix = "asdfasdforno"
        self.moveFromDownloads()
        self.moveFromFolder()
        if (len(args) == 1):
            self.SToAOrAToS = "AllToS"
        else:
            self.SToAOrAToS = args[1]

        lst = glob.glob("*.torrent")
        for x in tqdm(range(len(lst))):
            filename = lst[x].split('\\')[-1]
            os.rename(lst[x], lst[x].replace(self.prefix,""))
            lst[x] = lst[x].replace(self.prefix,"")

        total = 0
        for x in tqdm(lst):
            if self.SToAOrAToS.upper() == "ATOS":
                total += self.AToS(x)
            if self.SToAOrAToS.upper() == "STOA":
                total += self.SToA(x)
            if self.SToAOrAToS.upper() == "ALLTOM":
                total += self.AllToM(x)
            if self.SToAOrAToS.upper() == "ALLTOS":
                total += self.AllToS(x)
            if self.SToAOrAToS.upper() == "ALLTOA":
                total += self.AllToA(x)
            self.find_image(x)
        print("DONE: ",total)

    def SToA(self, path):
        return self.replace_text_in_file(path, self.constS, self.constA)

    def AToS(self, path):
        return self.replace_text_in_file(path, self.constA, self.constS)

    def AllToM(self, path):
        c1 = self.replace_text_in_file(path, self.constA, self.constM)
        c2 = self.replace_text_in_file(path, self.constS, self.constM)
        return c1 + c2

    def AllToS(self, path):
        c1 = self.replace_text_in_file(path, self.constA, self.constS)
        c2 = self.replace_text_in_file(path, self.constM, self.constS)
        return c1 + c2

    def AllToA(self, path):
        c1 = self.replace_text_in_file(path, self.constM, self.constA)
        c2 = self.replace_text_in_file(path, self.constS, self.constA)
        return c1 + c2

    def replace_text_in_file(self, fileToSearch, textToSearch, textToReplace):
        path = os.getcwd() + "\\temp\\"
        try:
            os.mkdir(path)
            print("Created: ",path)
        except OSError:
            pass
        filename = fileToSearch.split('\\')[-1]
        os.rename(filename, filename.replace(self.prefix,""))
        filename = filename.replace(self.prefix,"")
        filenamewo = ".".join(fileToSearch.split('\\')[-1].split(".")[0:-1])
        filenamew = path + filenamewo + ".torrent"
        if os.path.exists(filenamew):
            os.remove(filenamew)
        os.rename(filename, filenamew)
        inputFile = open( filenamew, 'rb+')
        tempFile = open( filename, 'wb+')
        replaced = 0
        for line in inputFile:
            if textToSearch in line:
                replaced += 1
            tempFile.write( line.replace( textToSearch, textToReplace ) )
        inputFile.close()
        tempFile.close()
        return replaced

    def moveFromFolder(self, path = "y:\\Soft\\Share\\temp"):
        downloadsPath = path
        currentPath = os.getcwd()
        lst = glob.glob(downloadsPath + "\\*lab*.torrent")
        lst = glob.glob(downloadsPath + "\\*.torrent")
        for f in lst:
            shutil.move(f, currentPath + "\\" + f.split("\\")[-1])

    def moveFromDownloads(self):
        downloadsPath = os.path.expanduser("~")+"\\Downloads"
        currentPath = os.getcwd()
        lst = glob.glob(downloadsPath + "\\*lab*.torrent")
        for f in lst:
            shutil.move(f, currentPath + "\\" + f.split("\\")[-1])

    def find_image(self, filename):
        return None
        path = os.getcwd() + "\\temp\\"
        try:
            os.mkdir(path)
            print("Created: ",path)
        except OSError:
            pass
        filename = filename.split('\\')[-1]
        inputFile = open( filename, 'rb+')

        #(?=comment)(http.+)(?:created)
        #pattern = re.compile("<(\d{4,5})>")
        #for i, line in enumerate(open('test.txt')):
        #    for match in re.finditer(pattern, line):
        #        print 'Found on line %s: %s' % (i+1, match.group())


        inputFile.close()
        return None

changer = Changer(sys.argv)
