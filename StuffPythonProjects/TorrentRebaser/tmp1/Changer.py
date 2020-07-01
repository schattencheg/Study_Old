import os
import glob
import fileinput
import shutil

class Changer:
    constA = b"xkzS1Lpl3f7"#"2374849e"
    constS = b"A93wDw45Vb7"#"2194943e"
    constM = b"oSJulLlHil7"#
    SToAOrAToS = "SToA"

    def __init__(self):
        self.moveFromDownloads()

        #lst = glob.glob("e:\Soft\System\Tools\_temp_from_folder\*.torrent")
        lst = glob.glob("*.torrent")
        total = 0
        if self.SToAOrAToS.upper == "ATOS":
            for x in lst:
                total += self.AToS(x)
        else:
            if self.SToAOrAToS.upper == "STOA":
                for x in lst:
                    total += self.SToA(x)
            else:
                if self.SToAOrAToS.upper == "AllTOM":
                    for x in lst:
                        total += self.AllToM(x)
        print("DONE: ",total)
        input("Press Enter to continue...")
        

    def SToA(self, path):
        return self.replace_text_in_file(path, self.constS, self.constA)

    def AToS(self, path):
        return self.replace_text_in_file(path, self.constA, self.constS)

    def AllToM(self, path):
        c1 = self.replace_text_in_file(path, self.constA, self.constM)
        c2 = self.replace_text_in_file(path, self.constS, self.constM)
        return c1 + c2

    def replace_text_in_file(self, fileToSearch, textToSearch, textToReplace):
        path = os.getcwd() + "\\temp\\"
        try:
            os.mkdir(path)
            print("Created: ",path)
        except OSError:
            pass
        filename = fileToSearch.split('\\')[-1]
        filenamewo = ".".join(fileToSearch.split('\\')[-1].split(".")[0:-1])
        filenamew = path + filenamewo + ".torrent"
        if os.path.exists(filenamew):
            os.remove(filenamew)
        os.rename(filename, filenamew)
        print(path + " -> " + filenamew)
        inputFile = open( filenamew, 'rb+')
        tempFile = open( filename, 'wb+')
        replaced = 0
        for line in inputFile:
            if textToSearch in line:
                replaced += 1
            tempFile.write( line.replace( textToSearch, textToReplace ) )
            #print(filenamew)
        inputFile.close()
        tempFile.close()
        return replaced

    def moveFromDownloads(self):
        downloadsPath = os.path.expanduser("~")+"\\Downloads"
        currentPath = os.getcwd()
        lst = glob.glob(downloadsPath + "\\*lab*.torrent")
        for f in lst:
            shutil.move(f, currentPath + "\\" + f.split("\\")[-1])



changer = Changer()
