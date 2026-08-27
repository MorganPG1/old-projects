from __future__ import annotations

import tkinter
import package.dcm as dcm


class UI:
    def __init__(self):
        self.root = tkinter.Tk()
        self.window = tkinter.Canvas(self.root, width=400, height=200, background="black")
        self.window.pack()
        self.indicatorUiList = []

    def mainLoop(self, indicatorlist:dict[str, dcm.Indicator]):
        ind = 0 
        self.window.delete("all")
        for name, indicator in indicatorlist.items():
            color = indicator.color.str
            isOn = indicator.isOn
            if not isOn:
                color = "white"
            x1 = 10+10*ind
            y1 = 10+10*ind
            x2 = 30+10*ind
            y2 = 30+10*ind
            self.window.create_oval(10,10,30,30, fill=color)
            ind+=1
            self.root.update()       
            self.root.update_idletasks()