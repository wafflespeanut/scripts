import os
from time import strftime as time

loc='C:\\Users\\Waffles Crazy Peanut\\Desktop\\Dropbox\\Diary\\'
months={'11':'November','10':'October','12':'December','1':'January','3':'March','2':'February','5':'May','4':'April','7':'July','6':'June','9':'September','8':'August'}

# Protection, Random stories, Location (self-modify & restart), Narrating, etc. are on the way...

def new():
    if not os.path.exists(loc+time('%Y')): os.mkdir(loc+time('%Y'))
    f=loc+time('%Y')+os.sep+months[time('%m')]+' ('+time('%Y')+')'
    if not os.path.exists(f): os.mkdir(f)
    File=f+os.sep+'Day '+time('%d')+' ('+months[time('%m')]+' '+time('%Y')+').txt'; f=open(File,'a')
    a=['['+time('%Y')+'-'+time('%m')+'-'+time('%d')+']'+' '+time('%H')+':'+time('%M')+':'+time('%S')+'\n']
    try: s=raw_input('''\nStart writing... (Press Ctrl+C when you're done!)\n\n\t'''); a.append('\t'+s)
    except KeyboardInterrupt: print 'Nothing written! Quitting...'; return None
    while True:
        try: s=raw_input(); a.append(s)
        except KeyboardInterrupt: break
    f.write('\n'.join(a)+'\n\n'); f.close()
    s=raw_input('\nSuccessfully written in file! Do you wanna see it (y/n)? ')
    if s=='y': os.startfile(File)

def diary():
    s=raw_input("\n\tWhat do you wanna do?\n\n\t\t1. Write today's story\n\t\t2. Random story\n\t\t3. View the story of someday\n\nChoice: ")
    if s=='1': new()
    elif s in '23': print '\nNot yet implemented - Will be done soon...'
    else: print '\nIllegal choice! Quitting...'
