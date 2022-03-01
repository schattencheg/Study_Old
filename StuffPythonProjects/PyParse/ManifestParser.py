import json
import pathlib
import requests

paths = ["c:\\Program Files (x86)\\Steam\\steamapps\\", "d:\\install\SteamLibrary\steamapps\\", "e:\\SteamLibrary\\steamapps\\",
        'y:\\Games\\SteamLibrary\\steamapps\\', "\\192.168.0.100\\c\\Program Files (x86)\\Steam\\steamapps\\"]
paths = ["e:\\SteamLibrary\\steamapps\\"]

game_names = ['American Truck Simulator' ,'ARK' ,'Automachef' ,'Bee Simulator' ,'Braid' ,'Broforce' ,'Bulletstorm Full ClipEdition' ,'cargo commander' ,'Dead Mans Draw' ,'Divinity Original Sin Enhanced Edition' ,'Doodle God' ,'Duskers' ,'Eufloria HD' ,'Evoland 2' ,'Fury Unleashed' ,'Gems of War' ,'Gnomoria' ,'Guacamelee2' ,'Gunpoint' ,'Heroes of Might & Magic III - HD Edition' ,'Heroes of Might and Magic 5 Tribes of the East' ,'Homeworld' ,'I Hate Running Backwards' ,'In Other Waters' ,'Infectonator Survivors' ,'Legends of Idleon' ,'Life is Feudal Forest Village' ,'Main Assembly' ,'Maneater' ,'Murdered Soul Suspect' ,'Sanctum2' ,'Shadow of the Tomb Raider' ,'SHENZHEN IO' ,'Skyrim' ,'SniperGhostWarrior2' ,'Space Rangers HD A War Apart' ,'SpaceEngineers' ,'Supraland' ,'Syberia3' ,'Tesla vs Lovecraft' ,'The Sims 3' ,'Tower of Time' ,'Trailmakers' ,'Vampyr' ,'Warstone TD' ,'WeHappyFew' ,'WeNeedtoGoDeeper' ,'Worms Armageddon' ]
game_names = [x.lower() for x in game_names]

class ManifestParser:
    def __init__(self, path):
        pass
        #self.SteamApps = sorted([x['name'] for x in self.GetSteamApps()])
        #with open('your_file.txt', 'w', encoding="utf8") as f:
        #    for item in self.SteamApps:
        #        f.write("%s\n" % item)

    def GetFiles(self, path, mask):
        """
        Returns list of files in the _path_ by the _mask_
        """
        return [x.name for x in pathlib.Path(path).glob(mask)]

    def ExtractName(self, path):
        with open(path, 'r') as f:
            data = f.readlines()
            lines = ''.join(data).replace('\"','\n').split('\n')
            lines = [x.lstrip() for x in lines]
            lines = [x for x in lines if x != '']
            if 'installdir' in lines:
                return lines[lines.index('installdir') + 1]
            #elements = line.replace("\"","\n").replace("\n\n","").split("\t")
            #for line in data:
            #    #elements = line.replace("\n","").replace("\""," ").replace("\'","").split("\t")
            #    elements = line.replace("\"","\n").replace("\n","").split("\t")
            #    for element in elements:
            #        if "installdir" in element:
            #            return elements[-1]
        return ''

    def ListFiles(self, path):
        manifests = self.GetFiles(path, "*acf*")
        folders = self.GetFiles(path + "common\\", "*")
        return manifests, folders

    def GetAppId(self, name):
        try:
            appId = self.SteamApps.index(name)
        except:
            appId = None
        return appId

    def GetSteamApps(self):
        URL = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
        r = requests.get(url = URL, params = {}) 
        appList = json.loads(r.text)['applist']['apps']
        return appList

    def WriteManifest(self, id, name, path):
        with open(path + "appmanifest_" + str(id) + ".acf", 'w') as f:
            f.write("AppState\n")
            f.write("{\n")
            f.write("\"AppID\"  \"{}\"".format(id))
            f.write("\"Universe\" \"1\"")
            f.write("\"Universe\" \"1\"")
            f.write("\"installdir\" \"{}\"".format(name))
            f.write("\"StateFlags\" \"1026\"")
            f.write("}\n")

    def FindGamesWithoutManifest(self, path, comment = ""):
        print("Search for missing folders for existing manifests:")
        m, f = self.ListFiles(path)
        folderNames = []
        for manifest_name in m:
            pth = path + manifest_name
            name = self.ExtractName(pth)
            if not name is None:
                folderNames.append({"manifest_name":manifest_name, "name":name})
        #for i in range(len(folderNames)):
        #    print(m[i] + " " + folderNames[i])
        for pair in folderNames: # Folders from Manifest 
            manifest_name = pair['manifest_name']
            name = pair['name']
            if not name in f: # Folders from folder
                #print("This one {" + name + "} is not in the folders")
                print(manifest_name)
                appId = self.GetAppId(name)
                #if appId is None:
                #    print("NO ID:" + str(appId))
                #else:
                #    print("APPID: " + str(appId))
                #    self.WriteManifest(appId, name, path)
        print("Done!")

    def FindManifestsWithoutGames(self, path, comment = ""):
        print("Search for missing manifests for existing folders:")
        m, f = self.ListFiles(path)
        folderNames = []
        for name in m:
            pth = path + name
            name = self.ExtractName(pth)
            if not name is None:
                folderNames.append(name)
        for name in f: # Folders from folder
            if not name in folderNames: # Folders from Manifest
                #print("This one {" + name + "} is not in the manifests list")
                appId = self.GetAppId(name)
                if appId is None:
                    print("NO ID:" + str(appId))
                else:
                    print("APPID:" + str(appId))
                    #self.WriteManifest(appId, name, path)
        print("Done!")

    def CheckManifestsAgainstGamesList(self, manifests, game_names):
        for manifest in manifests:
            pass

for path in paths:
    print("\n\nWORKING WITH ", path)
    manifestParser1 = ManifestParser(path)
    ml, sl = manifestParser1.ListFiles(path)
    
    mans = {}
    names = {}
    arr = []
    for manifest_filename in ml:
        with open(path + manifest_filename) as f:
            mans[manifest_filename] = f.readlines()
            name = manifestParser1.ExtractName(path + manifest_filename).lower()
            names[manifest_filename] = name
            val = name + '  ' + manifest_filename
            arr.append(val)
            if not name in game_names:
                #print('-{:<20} {:>40}'.format(manifest_filename, name))
                #print('-' + val)
                #print('- ' + manifest_filename + ' ' + name + ' '  + ' not in games')
                pass
            else:
                #print('+{:<20} {:>40}'.format(manifest_filename, name))
                #print('+' + val)
                #print('+ ' + manifest_filename + ' ' + name + ' ')
                pass
    vals = list(names.values())
    vals.sort()
    arr.sort()
    for val in arr:
        print(val)
        
    manifestParser1.CheckManifestsAgainstGamesList()
    manifestParser1.FindGamesWithoutManifest(path, paths.index(path))
    manifestParser1.FindManifestsWithoutGames(path, paths.index(path))

#names = []
#namesForCheck = []
#files = getFiles(path, "*acf*")
#folders = getFiles(pathFldrs, "*")
## Check manifests
#for fn in files:
#    f = open(path + fn, 'r')
#    #loaded_json = json.load(f)
#    #for x in loaded_json:
#    #    print("%s: %d" % (x, loaded_json[x]))
#    for line in f:
#        if "name" in line:
#            name = line.split("\"")[-2]
#            namesForCheck.append(name)
#            if not name in folders:
#                name = "!!!! " + name
#            names.append(name + " - " + fn)
##Check folders
#print("\nFOLDERS")
#for f in folders:
#    if not f in namesForCheck:
#        print("!!!! "+f)
#print("\nNAMES")
#names.sort()
#for n in names:
#    print(n)
#        
#