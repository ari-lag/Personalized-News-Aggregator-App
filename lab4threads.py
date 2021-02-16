# Arianna-Rae Lagman
# Spring 2020
# Using multithreading, web API access
# An app that lets user choose news sources, get the latest headlines, and read the news article online

import threading
import requests
import tkinter as tk
import webbrowser
import tkinter.messagebox as tkmb


class DisplayWin(tk.Toplevel):
    """Class to create display window to present latests headlines of user's choice of news sources"""
    
    def __init__(self, master, sourceChoices, sources):
        """Constructor for DisplayWin class
            Use of listbox filled with news source and their headline title
        """
        super().__init__(master)
        self.sources = sources
        self.title("Headlines")
        tk.Label(self, text="Click on a headline to read the article", fg='black').grid()
        self.F = tk.Frame(self)
        self.F.grid()
        self.S = tk.Scrollbar(self.F)
        self.LB = tk.Listbox(self.F, height=20, width=100, yscrollcommand=self.S.set)
        self.S.config(command=self.LB.yview)
        self.LB.grid()
        self.S.grid(row=0, column=1, sticky='ns')
        
        threads = []
        headlines = []
        for i in sourceChoices:
            t = threading.Thread(target = self.getHeadlines, args = (i, headlines))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        
        self.LB.insert(tk.END, *headlines)                                                                 
        self.LB.bind('<<ListboxSelect>>', self.selectEvent)
        self.transient(master)
        self.focus_set()
        self.grab_set()
        
    def getHeadlines(self, choice, headlinesList):
        """Perameters: index of choosen news source and list of headlines to append to
            Calls def choicesAPI to get headlines of news source
        """
        print("start: " + str(choice))
        self.data = []
        name = self.sources[choice]
        headlineList = self.choicesAPI(name)
        for article in headlineList:
            if len(article[1]) != 0:
                self.data.append(article)
                page = article[0] + ": " + article[1]
                headlinesList.append(page)
        print("done: " + str(choice))
        
    def  selectEvent(self, event):
        """Event: user clicks headline
            Opens url of user's choice in webbrowser
        """
        widget = event.widget
        selection = list(widget.curselection())
        i = selection[0]
        url = self.data[i][2]
        webbrowser.open(url)                                                
        
    def choicesAPI(self, sourceName):
        """Parameter: name of news source
            API calls for top headlines
            Returns list of all the latest headlines from news source 
        """
        name = sourceName.lower()
        name = name.replace(" ", "-")
        url2 = ('https://newsapi.org/v2/top-headlines?sources={}&apiKey=e54615b4418844db88ebe1cc4ac0cd33'.format(name))
        data = requests.get(url2)
        results = data.json()
        articles = results['articles']
        headlines = []
        for i in articles:
            article = []
            name = i['source']
            article.append(name['name'])
            article.append(i['title'])
            article.append(i['url'])
            headlines.append(article)
        return headlines 


class MainWin(tk.Tk):
    """Class to create main window that interacts with user"""
    
    def __init__(self):
        """Constructor for MainWin class
            Calls def sourcesAPI to get all news sources in the United States
            Displays main window with a listbox of news sources
            User is able to pick at least one news source
        """
        super().__init__()
        self.title("Latest Headlines")
        tk.Label(self, text="Choose your news sources", fg='blue').grid()
        self.F = tk.Frame(self)
        self.F.grid()
        self.S = tk.Scrollbar(self.F)
        self.LB = tk.Listbox(self.F, height=20, width=30, yscrollcommand=self.S.set, selectmode='multiple')
        self.S.config(command=self.LB.yview)
        self.LB.grid()
        self.S.grid(row=0, column=1, stick='ns')
        names = self.sourcesAPI()
        self.LB.insert(tk.END, *names)
        tk.Button(self, text="OK", command=lambda: self.setChoice(names)).grid()
        
        
    def setChoice(self, names):
        """Parameter: names
            Caslls DisplayWin class to create display window
           Also notifies user if they have not select at least one
        """
        self.choice = self.LB.curselection()
        if len(self.choice) == 0:
            tkmb.showinfo("Note", "Choose one or more news source.", parent=self)
        else:
            displayWin = DisplayWin(self, self.choice, names)
            self.LB.selection_clear(0, tk.END)
        
    def getChoice(self):
        """Returns choices"""
        return self.choice
    
    def sourcesAPI(self):
        """API call for all the news sources in the United States
           Returns a list of news sources 
        """
        url1 = ('https://newsapi.org/v2/sources?language=en&country=us&apiKey=e54615b4418844db88ebe1cc4ac0cd33')
        response = requests.get(url1)
        details = response.json()
        sources = details['sources']
        names = []
        for source in sources:
            name = source['name']
            names.append(name)
        return names
         
        
win = MainWin()
win.mainloop()