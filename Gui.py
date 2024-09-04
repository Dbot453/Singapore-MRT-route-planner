import tkinter as tk
import graphTraversal as gt
class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Shortest Path Finder")
        self.root.geometry("800x600")
        # self.root.configure(background="white")
        
        self.start = tk.StringVar()
        self.end = tk.StringVar()
        
        self.startLabel = tk.Label(self.root, text="Start Station", font="Helvetica 12 bold") 
        self.endLabel = tk.Label(self.root, text="End Station", font="Helvetica 12 bold")
        
        self.startEntry = tk.Entry(self.root, textvariable=self.start)
        self.endEntry = tk.Entry(self.root, textvariable=self.end)
        
        sub_btn=tk.Button(self.root,text = 'Submit', command = GUI.findPath())
        
        self.startLabel.grid(row=0, column=0)
        self.endLabel.grid(row=1, column=0)
        self.startEntry.grid(row=0, column=1)
        self.endEntry.grid(row=1, column=1)
        sub_btn.grid(row=2, column=1)
        
        self.root.mainloop()
        
        
    def findPath():
        start=self.__.start.get()
        end=self.__end.get()
        self.__start.set("")
        self.__end.set("")
        print(gt.getShortestPath(start,end)) 
        
GUI()