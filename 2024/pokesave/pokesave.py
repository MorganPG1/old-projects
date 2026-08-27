from typing import BinaryIO
from pokelist import pokemon_list, glitch_pokemon_list,idToText,moves_list

def readByte(f:BinaryIO, pos:int):
    f.seek(pos, 0)
    return f.read(1)

def readBytes(f:BinaryIO, pos:int, numOfBytes:int):
    f.seek(pos, 0)
    return bytearray(f.read(numOfBytes))

def padBytearray(data:bytearray, padding:int, length:int):
    if len(data) < length:
        return data + bytearray([padding]) * (length - len(data))
    return data

def calculateChecksum(data:bytearray):
    checksum = 255
    for byte in data:
        checksum = (checksum - byte) % 256
    return checksum
class PKMNStr():
    def __init__(self, txt:bytearray) -> None:
        self.text = ""
        for byte in txt:
            
            if byte == 0x50:
                #print("END")
                break
            #print(hex(byte))
            self.text += idToText[byte]
        pass
    @classmethod
    def encode(c, txt:str, addTerminator:bool=True):
        result = bytearray()
        for char in txt:
            if char in idToText[113::]:
                
                byteOfChar = idToText[113::].index(char)
                result.append(byteOfChar+113)
                #print(idToText[byteOfChar+113])
        result.append(0x50)
        return result
    @classmethod
    def new(c, txt:str):
        return c(c.encode(txt))

class Pokemon():
    def __init__(self, data:bytearray, nickname:PKMNStr) -> None:
        self.species = data[0]
        self.isGlitch = False
        if self.species > len(pokemon_list)-1:
            self.isGlitch = True
            self.speciesName = glitch_pokemon_list[self.species-190]
        else:
            self.speciesName = pokemon_list[self.species]
            if self.speciesName == "MissingNo.":
                self.isGlitch = True
        
        self.nickname = nickname.text
        

        self.hp = data[1:3]
        self.type1 = data[5]
        self.type2 = data[6]
        self.catchRate = data[7]
        self.moves = data[0x8:0x0C]
        self.otID = data[0x0C:0x0E]
        self.exp = data[0x0E:0x11]
        self.hpStat = data[0x11:0x13]
        self.defStat = data[0x13:0x15]
        self.speedStat = data[0x17:0x19]
        self.specialStat = data[0x19:0x1B]
        self.ivData = data[0x1B:0x1D]
        self.movePP = data[0x1D:0x21]
        self.level = data[21]
        self.maxHP = data[0x22:0x24]
        self.attack = data[0x24:0x26]
        self.defence = data[0x26:0x28]
        self.speed = data[0x28:0x2A]
        self.special = data[0x2A:0x2C]

        self.hp = int.from_bytes(self.hp)
        self.otID = int.from_bytes(self.otID)
        self.exp = int.from_bytes(self.exp)
        self.hpStat = int.from_bytes(self.hpStat)
        self.defStat = int.from_bytes(self.defStat)
        self.speedStat = int.from_bytes(self.speedStat)
        self.specialStat = int.from_bytes(self.specialStat)
        self.maxHP = int.from_bytes(self.maxHP)
        self.attack = int.from_bytes(self.attack)
        self.defence = int.from_bytes(self.defence)
        self.speed = int.from_bytes(self.speed)
        self.special = int.from_bytes(self.special)
        pass
    @classmethod
    def encode(
        c,
        species:int,
        movePP:list, 
        exp:int, 
        level:int, 
        type1:int, 
        maxHP:int=25, 
        hp:int=25, 
        type2:int=0, 
        moves:list[int]=[33], 
        otID:int=0, 
        hpStat:int=25,
        defStat:int=25,
        speedStat:int=25,
        specialStat:int=25,
        ivData:bytearray=[125,125],
        attack:int=25,
        defence:int=25,
        speed:int=25,
        special:int=25,
    ):
        result = bytearray()
        result[0] = species
        result[1:3] = hp.to_bytes(2,"little")
        result[3] = level
        result[4] = 0
        result[5] = type1,
        result[6] = type2,

        
class PKMNParty():
    def __init__(self, data:bytearray) -> None:
        self.count = data[0]
        self.pokenon:list[Pokemon] = []
        for i in range(0,self.count):
            offset = 0x8+(0x2C*i)
            nicknameOffset = 0x152+(0xb*i)
            species = data[i+1]
            pkmn = data[offset:offset+0x2c]
            self.pokemon.append(Pokemon(pkmn, PKMNStr(data[nicknameOffset:nicknameOffset+0xb])))
        pass
    def encode(self,pokemonList:list[Pokemon],otNames:list[PKMNStr]=[PKMNStr.new("Red")]*6):
        result = bytearray()
        result[0] = len(pokemonList)
        for i in range(0,len(pokemonList)):
            result[i+1] = pokemonList[i].species
        padBytearray(result, 0xff, 8)
        
class HallOfFamePokemon():
    def __init__(self,pokemon:bytearray) -> None:
        
        species = pokemon[0]
        level = pokemon[1]
        nickname = pokemon[0x2:0xB]
        nicknameDecoded = PKMNStr(nickname).text
        self.species = species
        self.isGlitch = False
        if species > len(pokemon_list)-1:
            self.isGlitch = True
            self.speciesName = glitch_pokemon_list[species-190]
        else:
            self.speciesName = pokemon_list[species]
            if self.speciesName == "MissingNo.":
                self.isGlitch = True
        self.level = level
        self.name = nicknameDecoded
        pass
    @classmethod
    def encode(c, species:int, level:int, name:str):
        result = bytearray()
        #print(type(species))
        #print(type(level))
        #print(type(name))
        result.append(species)
        result.append(level)
        name = PKMNStr.encode(name)
        if len(name) < 0xb:
            name += bytearray([0x50]) * (0xb-len(name))
        result += name
        result += bytearray([0x00])*3
        return result
    @classmethod
    def new(c, species:int, level:int, name:str):
        return c(c.encode(species, level, name))
class HallOfFameEntry():
    def __init__(self, pokemonList:bytearray) -> None:
        self.pokemon:list[HallOfFamePokemon] = []
        for pokemon in range(0,6):
            offset = ((pokemon*0x10))
            pokemonData = pokemonList[offset:offset+0x10]
            if pokemonList[offset] == 0xff:
                break
            pokemonDecoded = HallOfFamePokemon(pokemonData)
            self.pokemon.append(pokemonDecoded)
        pass
    @classmethod
    def encode(c, pokemonList:list[HallOfFamePokemon]):
        result = bytearray()
        for pokemon in pokemonList:
            result += pokemon.encode(pokemon.species, pokemon.level, pokemon.name)
        result = padBytearray(result,0xff,0x60)
        return result
    @classmethod
    def new(c, pokemonList:list[HallOfFamePokemon]):
        return c(c.encode(pokemonList))
class SaveFile():
    def __init__(self, hallOfFame:list[HallOfFameEntry]=[], mainData:bytearray=padBytearray(bytearray(), 0xff,2000), box1:bytearray=padBytearray(bytearray(), 0xff, 2000), box2:bytearray=padBytearray(bytearray(), 0xff, 2000)) -> None:
        self.hallOfFame = hallOfFame
        self.mainData = mainData
        self.box1 = box1
        self.box2 = box2

        money = mainData[0x5b:0x5e]
        plrName = mainData[:0xb]
        rivalName = mainData[0x5e:0x5e+0xb]
        self.plrName = PKMNStr(plrName)
        self.rivalName = PKMNStr(rivalName)
        self.money = ""
        for byte in money:
            hmoney = hex(byte)[2:].rjust(2,"0")
            self.money += hmoney
        self.money = int(self.money)
        self.party = PKMNParty(mainData[0x994:0xB28])

        #print("Player money:",self.money)
    def save(self, path:str):
        save = open(path, "wb")
        data = bytearray([0xff]) * 0x598
        #print(hex(len(data)))
        for entry in self.hallOfFame:
            encodedEntry = entry.encode(entry.pokemon)
            
            
            data += encodedEntry
            if self.hallOfFame.index(entry) == 50:
                break
        data = padBytearray(data, 0xff,0x2598)

        #print(checksum,self.mainData[0xF8B])
        self.mainData[:0xb] = self.plrName.encode(self.plrName.text)
        self.mainData[0x5e:0x5e+0xb] = self.plrName.encode(self.plrName.text)
        self.mainData[0x2B6] = len(self.hallOfFame)

        m = str(self.money).rjust(6,"0")
        
        self.mainData[0x5b] = int(m[0:2])
        self.mainData[0x5c] = int(m[2:4])
        self.mainData[0x5d] = int(m[4:6])


        checksum = calculateChecksum(self.mainData[:0xF8B])
        self.mainData[0xf8b] = checksum

        data += self.mainData
        data = padBytearray(data, 0xff,0x4000)
        data+= self.box1
        data = padBytearray(data, 0xff,0x6000)
        data+= self.box2
        data = padBytearray(data, 0xff, 8000)
        
        save.write(data)
        save.close()
    @classmethod
    def load(cl, path:str):
        save = open(path, "rb")
        entries = readByte(save,0x284E)
        entries = int.from_bytes(entries, "little")
        entryList = []
        for i in range(0,entries):
            
            start = 0x598+(i*0x60)
            #print(hex(start))
            entry = readBytes(save,0x598, 0x60)
            #print(hex(len(entry)))
            #print(readBytes(save, 0x598, 0x60))
            '''
            hexStr = ""
            for val in entry:
                hexStr += hex(val) + " "
            print(hexStr)
            '''
            #print(len(pokemon_list))
            #print(len(glitch_pokemon_list))
            #print(len(pokemon_list) + len(glitch_pokemon_list))
            '''
            for pokemon in pokemon_list:
                print(pokemon_list.index(pokemon), pokemon)
            '''
            '''
            for pokemon in range(0,6):
                offset = ((pokemon*0x10))
                species = entry[offset]
                nickname = entry[offset+2: offset+0xB]
                nicknameDecoded = PKMNStr(nickname).text
                #print(hex(offset), hex(species))
                if species == 0xff:
                    break
                if species > len(pokemon_list):
                    print(f"Pokemon: {glitch_pokemon_list[species - 191]}, Level: {entry[offset+1]}, Nickname:{nicknameDecoded}")
                else:
                    print(f"Pokemon: {pokemon_list[species]}, Level: {entry[offset+1]}, Nickname:{nicknameDecoded}")
            '''
            entryDecoded = HallOfFameEntry(entry)
            entryList.append(entryDecoded)
        '''
        hexStr = ""
        for val in entryDecoded.encode(entryDecoded.pokemon):
            hexStr += hex(val) + " "
        print(hexStr)
        for pokemon in entryDecoded.pokemon:
            print(pokemon.speciesName)
            print(pokemon.level)
            print(pokemon.name)
        '''
        mainData = readBytes(save,0x2598,0x2000)
        box1 = readBytes(save, 0x4000,0x2000)
        box2 = readBytes(save,0x6000,0x2000)

        return SaveFile(entryList, mainData,box1,box2)
        
s = SaveFile.load("Pokemon.sav")

s.hallOfFame.append(
    HallOfFameEntry.new(
        [
            HallOfFamePokemon.new(0xB0, 5, "test1"), #Should make a Level 5 Charmander named test1 in the Hall Of Fame Entry 2
            HallOfFamePokemon.new(0xB1, 5, "test2"), #Should make a Level 5 Squirtle named test2 in the Hall Of Fame Entry 2
        ]
    )
)

s.plrName = PKMNStr(PKMNStr.encode("",False))
s.save("pokemon3.sav")