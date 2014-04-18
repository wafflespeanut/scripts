import Feed_Parser
import string
import time
from Project import translate_html
from Tkinter import *

def process(url):
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

class NewsStory(object):
    def __init__(self, guid, title, subject, summary, link):
        self.g=guid
        self.t=title
        self.sub=subject
        self.sum=summary
        self.l=link
    
    def getGuid(self):
        return self.g
    def getTitle(self):
        return self.t
    def getSubject(self):
        return self.sub
    def getSummary(self):
        return self.sum
    def getLink(self):
        return self.l

class Trigger(object):
    def evaluate(self,story):
        raise NotImplementedError

class WordTrigger(Trigger):
    def __init__(self,word):
        self.word=word.lower()

    def isWordIn(self,text):
        replace = string.maketrans(string.punctuation, ' '*len(string.punctuation))
        self.text=text.lower().translate(replace)
        if self.word in self.text.split():
            return True
        else: return False

class TitleTrigger(WordTrigger):
    def evaluate(self,story):
        return self.isWordIn(story.getTitle())
    
class SubjectTrigger(WordTrigger):
    def evaluate(self,story):
        return self.isWordIn(story.getSubject())

class SummaryTrigger(WordTrigger):
    def evaluate(self,story):
        return self.isWordIn(story.getSummary())

class NotTrigger(Trigger):
    def __init__(self,trigger):
        self.trig=trigger

    def evaluate(self,story):
        return not self.trig.evaluate(story)

class AndTrigger(Trigger):
    def __init__(self,trig1,trig2):
        self.trig1=trig1
        self.trig2=trig2

    def evaluate(self,story):
        return self.trig1.evaluate(story) and self.trig2.evaluate(story)

class OrTrigger(Trigger):
    def __init__(self,trig1,trig2):
        self.trig1=trig1
        self.trig2=trig2

    def evaluate(self,story):
        return self.trig1.evaluate(story) or self.trig2.evaluate(story)

class PhraseTrigger(Trigger):
    def __init__(self,phrase):
        self.phrase=phrase

    def evaluate(self,story):
        if self.phrase in (story.getSubject() or story.getTitle() or story.getSummary()):
            return True
        else: return False

def filterStories(stories, triggerlist):
    work=[]
    for trigger in triggerlist:
        for story in stories:
            if trigger.evaluate(story):
                work.append(story)
    return work

def makeTrigger(triggerMap, triggerType, params, name):
    #Have to make some modifications here
    pass

def readTriggerConfig(filename):
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)
        
    triggers = []
    triggerMap = {}
    for line in lines:
        linesplit = line.split(" ")
        if linesplit[0] != "ADD":
            trigger = makeTrigger(triggerMap, linesplit[1], linesplit[2:], linesplit[0])
        else:
            for name in linesplit[1:]:
                triggers.append(triggerMap[name])
    return triggers
    
import thread

SLEEPTIME = 60


def main_thread(master):
    try:
        t1 = TitleTrigger("Obama")
        t2 = SubjectTrigger("Romney")
        t3 = PhraseTrigger("Election")
        t4 = OrTrigger(t2, t3)
        triggerlist = [t1, t4]
        
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)
        
        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)

        guidShown = []
        def get_cont(newstory):
            if newstory.getGuid() not in guidShown:
                cont.insert(END, newstory.getTitle()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.getSummary())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.getGuid())

        while True:
            print "Pulling stuff...",
            stories = process("http://news.google.com/?output=rss")
            stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))
            stories = filterStories(stories, triggerlist)
            map(get_cont, stories)
            scrollbar.config(command=cont.yview)
            
            print "Now sleeping..."
            time.sleep(SLEEPTIME)

    except Exception as e:
        print e

if __name__ == '__main__':
    root = Tk()
    root.title("RSS News Reader")
    thread.start_new_thread(main_thread, (root,))
    root.mainloop()
