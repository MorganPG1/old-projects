import fpdf
import dtc_parser.parser as parser
pdf = fpdf.FPDF()
pdf.add_page()
pdf.add_font('Arial2', 'BI', 'c:/windows/fonts/arialbi.ttf', uni=True)  # added line
pdf.add_font('Arial2', 'I', 'c:/windows/fonts/ariali.ttf', uni=True)  # added line
pdf.add_font('Arial2', 'B', 'c:/windows/fonts/arialbd.ttf', uni=True)  # added line
pdf.set_font("Arial2", style="BU",size=50)
pdf.text(50,25, "Fault Report")

log = open("log.log", "r")
lines = log.readlines()
parse = parser.DTCParser()

class ecu:
    def __repr__(self) -> str:
        return f"<ECU <{self.name}> Faults: {len(self.faultList)}, Responsive: {self.responded}>"
    def __str__(self) -> str:
        return f"{self.name} - {len(self.faultList)} faults, Is responding: {self.responded}"
        pass
    def __init__(self, name:str,responded:bool=True) -> None:
        self.responded = responded
        self.faultList:parser.DTC = []
        
        self.name = name
        self.shortName = name.split("(")[0].replace(" ", "")
    def addFault(self, fault:parser.DTC):
        print(len(self.faultList), self.name)
        self.faultList.append(fault)

ecuList:list[ecu] = [

]

currentEcu = 0
for line in lines:
    line = line.replace("\n", "")
    if line.startswith("NO RESPONSE"):
        ecuList[currentEcu].responded = False
    else:

        split = line.split("-")
        size = len(split)
        if size > 1:
            if size >= 8:
                ecuName = split[4]
                if ecuName != "END":
                    ecuList.append(ecu(ecuName))
                    currentEcu = len(ecuList)-1
            else:
                print(len(split), split, line, currentEcu)
                code = split[2]
                state = split[3]
                dtc = parse.parse_code_asDTC(code)
                dtc.state = state
                print(dtc, currentEcu,ecuList[currentEcu].faultList)
                
                ecuList[currentEcu].addFault(dtc)
            

print(ecuList)

pdf.set_font("Arial2", "B", 15)
index = 0
line = 1
x = 0
firstPage = True
for ecu2 in ecuList:
     
    if index >= 9:
        line += 1
        x = 0
        index = 0
    text = ecu2.shortName
    if len(ecu2.faultList) > 0:
        text += f" ({len(ecu2.faultList)})"
        pdf.set_text_color(255,0,0)
    elif not ecu2.responded:
        pdf.set_text_color(205,205,205)
    else:
        pdf.set_text_color(0,255,0)
    print(text)
    #x = 10 + index*10

    print(x)
    pdf.text(5+x, 50+10*line, text)
    x += pdf.get_string_width(text) + 5
    
    index += 1


pdf.set_text_color(0,0,0)
for ecu2 in ecuList:
    if len(ecu2.faultList) > 0:
        line += 1
        if firstPage:
            y = 50
        else:
            y = 0

        
        y += 10*line

        text = ecu2.name
        pdf.text(5,y, text)

        for fault in ecu2.faultList:
            fault:parser.DTC
            line += 0.5
            if firstPage:
                y = 50
            else:
                y = 0
            y += 10*line
            

            pdf.set_font_size(13)
            text = f"{fault.dtc} ({fault.state}) - {fault.description}"
            pdf.text(5,y, text)
            if pdf.h - 20 < y:
                firstPage = False
                line = 1
                pdf.add_page()
        if pdf.h - 20 < y:
            firstPage = False
            line = 1
            pdf.add_page()



pdf.output("faults.pdf")

a = ecu("ECU1")
b = ecu("ECU2")
print(len(a.faultList), len(b.faultList))