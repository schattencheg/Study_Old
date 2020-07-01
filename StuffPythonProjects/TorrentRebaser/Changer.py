import sys
import os
import glob
import fileinput
import shutil
#from tqdm import tqdm

class Changer:
    constA = b"xkzS1Lpl3f7"#"2374849e"
    constS = b"A93wDw45Vb7"#"2194943e"
    constM = b"oSJulLlHil7"#
    SToAOrAToS = "AllToM"

    def __init__(self, args):
        self.moveFromDownloads()
        if (len(args) == 1):
            self.SToAOrAToS = "AllToS"
        else:
            self.SToAOrAToS = args[1]

        lst = glob.glob("*.torrent")
        for x in range(len(lst)):
            filename = lst[x].split('\\')[-1]
            os.rename(lst[x], lst[x].replace("orno",""))
            lst[x] = lst[x].replace("orno","")

        total = 0
        for x in lst:
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
        os.rename(filename, filename.replace("orno",""))
        filename = filename.replace("orno","")
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

    def moveFromDownloads(self):
        downloadsPath = os.path.expanduser("~")+"\\Downloads"
        currentPath = os.getcwd()
        lst = glob.glob(downloadsPath + "\\*lab*.torrent")
        for f in lst:
            shutil.move(f, currentPath + "\\" + f.split("\\")[-1])

changer = Changer(sys.argv)
