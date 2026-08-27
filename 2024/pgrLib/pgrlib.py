import os
import json
import base64
version = "a0.1"

class Resource():
    def __init__(self, data:bytes, fileName:str, tags:dict=None) -> None:
        '''
        Used to define a resource/file, \n
        data is a bytes object, \n
        fileName is the filename used when exporting with .save(), \n
        tags are the tags assigned to the resource.
        '''
        self.data = data
        self.fileName = fileName
        if tags:
            self.tags = tags
        else:
            self.tags = {}
        pass
    @classmethod
    def fromFile(cls, pathToFile):
        '''
        Loads a resource from a file.\n
        pathToFile is a string containing the path to the desired file
        '''
        File = open(pathToFile, "rb")
        data = File.read()
        File.close()
        return cls(data, os.path.basename(pathToFile))
    
    def encode(self):
        encodedBytes = base64.b64encode(self.data)
        return encodedBytes.decode()
    
    def getFileName(self):
        return self.fileName
    def getData(self):
        return self.data
    def getTags(self):
        return self.tags
    def addTag(self, tag, value):
        self.tags[tag] = value
    def save(self, dest:str=None):
        if not dest:
            dest = self.fileName
        File = open(dest, "wb")
        File.write(self.data)

class PGRFileException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
class PGR():
    def __init__(self, filePath:str=None) -> None:
        '''
        Create an PGR file or read from an existing one\n
        filePath: Path to PGR file (optional)
        '''
        if filePath:
            if isinstance(filePath, str): #Check if filepath is a string
                if os.path.exists(filePath): #Check if file exists
                    try:
                        f = open(filePath)
                        self.PGRDict = json.load( #Load JSON into PGRDict
                            f
                        )
                        f.close()

                        self.PGRDict["Version"]
                        self.PGRDict["Author"]
                        self.PGRDict["Title"]
                        self.PGRDict["Resources"]
                        self.PGRDict["Tags"]
                    except Exception:
                        raise PGRFileException("PGR File malformed, read failed")
                else:
                    raise PGRFileException("File does not exist")
            else:
                raise PGRFileException("Filepath is not a string")
        else:
            self.PGRDict = {
                "Version": version,
                "Author": "Undefined",
                "Title": "PGRFile",
                "Resources": {},
                "Tags": {},
            }
        pass

    def setAuthor(self, author:str):
        '''
        Set the author of the PGR File
        '''
        self.PGRDict["Author"] = author
    def setTitle(self,title:str):
        '''
        Set the title of the PGR File
        '''
        self.PGRDict["Title"] = title
    def getResources(self):
        resources:dict = self.PGRDict["Resources"]
        resourceList:list[Resource] = []
        for k,v in resources.items():
            decodedValue = base64.b64decode(v)
            tags = {}
            if k in self.PGRDict["Tags"]:
                tags = self.PGRDict["Tags"][k]
            resourceList.append(Resource(
                decodedValue,
                k,
                tags
            ))
        return resourceList
    def addResource(self, resource:Resource):
        resourceDict = self.PGRDict["Resources"]
        tagDict = self.PGRDict["Tags"]
        resourceDict[resource.getFileName()] = resource.encode()
        if len(resource.getTags()) > 0:
            tagDict[resource.getFileName()] = resource.getTags()
    def getAuthor(self):
        return self.PGRDict["Author"]
    def getTitle(self):
        return self.PGRDict["Title"]
    def getVersion(self):
        return self.PGRDict["Version"]
    def save(self, dest):
        f = open(dest, "w")
        json.dump(self.PGRDict, f)
        f.close()
