import PIL.Image
from zipfile import ZipFile
import os
import sys
import logging
from datetime import datetime
import pillow_heif
import shutil
import time
import platform
from tkinterdnd2 import *
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog as fd
from tkinter import messagebox
import webbrowser
import json
import default
import threading


version = 'v1.0.0'

"""
PhotopackConvert v1.0.0

Developed for BPS by Dallin Barker
Dallinbarker@gmail.com

"""

path = f"{os.path.expanduser('~')}\PhotopackConverData"
if not os.path.exists(f"{path}\logs") and os.path.exists(path):
    print('log path not found, creating')
    os.makedirs(f"{path}\logs")

# Logging exeption catcher
def exception_hook(exc_type, exc_value, exc_traceback):
   logging.error(
       "Uncaught exception",
       exc_info=(exc_type, exc_value, exc_traceback)
   )
   sys.exit()

# Logging init
def set_up_logger():
    date_time_obj = datetime.now()
    timestamp_str = date_time_obj.strftime("%d-%b-%Y_%H_%M_%S")
    filename = f"{path}\logs\log-"+f'{version}-'+f'{timestamp_str}.log'
    logging.basicConfig(filename=filename,level=logging.DEBUG)
    sys.excepthook = exception_hook

# custom print function for logging
def print(*txt,lvl=logging.INFO):
    txt = ''.join([str(x) for x in txt])
    __builtins__.print(txt)
    # print(txt)
    logging.log(lvl,txt)

if os.path.exists(path): set_up_logger()

pillow_heif.register_heif_opener()


# Get local user path
print(path)

# check if data folder exists
if not os.path.exists(path):
    print('path not found, creating')
    os.makedirs(path)
    os.makedirs(f"{path}\logs")
    print(os.path.exists(path),lvl=logging.DEBUG)

    result = messagebox.askquestion('Create Output folder', 'would you like to create and select a output folder on the desktop?')

    ddat = default.data
    
    if result == 'yes':
        # create desktop output folder
        os.makedirs(f"{os.path.expanduser('~')}\Desktop\output")
        ddat["fileLocations"]["Output"] = f"{os.path.expanduser('~')}\Desktop\output"
    os.makedirs(f"{os.path.expanduser('~')}\PhotopackConverData\Store")
    ddat["fileLocations"]["Storage"] = f"{os.path.expanduser('~')}\PhotopackConverData\Store"

    with open(f"{os.path.expanduser('~')}\PhotopackConverData\preferences.json", 'w') as f:
        json.dump(ddat, f)

        
    messagebox.showwarning('Restart','Photopack convert has set up neccicary files and will now quit. please restart the app to continue')
    quit()

    


else:
    print('path found, files:')
    for i in os.listdir(path):
        print(i)


# ---init---

# get preferences
preferences = None
with open(f"{os.path.expanduser('~')}\PhotopackConverData\preferences.json") as pref:
    preferences = json.load(pref)

# check and update file version
if preferences["fileVersion"] != default.data["fileVersion"]:
    print(preferences)
    for i in range(preferences["fileVersion"]+1,default.data["fileVersion"]+1):
        print(i,lvl=logging.DEBUG)
        print(default.newData[i],lvl=logging.DEBUG)
        preferences.update(default.newData[i])
    print(preferences,lvl=logging.DEBUG)
    preferences["fileVersion"] = default.data["fileVersion"]


with open(f"{os.path.expanduser('~')}\PhotopackConverData\preferences.json", 'w') as f:
    json.dump(preferences, f)

# Get debug value
debug = preferences["debug"]
print(debug,lvl=logging.DEBUG)


print(preferences,lvl=logging.DEBUG)

# Tkinter setup
root = TkinterDnD.Tk()
root.withdraw()
root.title(f'PhotopackConvert {version}')
# define grid defaults
root.grid_rowconfigure(1, weight=1, minsize=50)
root.grid_rowconfigure(3, weight=1, minsize=50)
root.grid_columnconfigure(0, weight=1, minsize=30)
root.grid_columnconfigure(1, weight=1, minsize=30)
# Left label
Label(root, text='Drop Photo pack Zip File').grid(
                    row=0, column=0, padx=5, pady=5)
# right label
Label(root, text='Drop Output folder here').grid(
                    row=0, column=1, padx=5, pady=5, columnspan=2)
# storage folder (if debug)
if debug:
    Label(root, text='drop storage folder here').grid(
                        row=2, column=1, padx=5, pady=5, columnspan=2)
else:
    Label(root, text='storage folder removed!').grid(
                        row=2, column=1, padx=5, pady=5, columnspan=2)
# Left file drop box
filedrop = Listbox(root, name='fileDropbox', selectmode='extended', width=1, height=1)
filedrop.grid(row=1, column=0, padx=5, pady=5, sticky='news',rowspan=3)
filedrop.insert('end', 'Drag Zip file to extract')
# Right Output File path box
outfilepath = Listbox(root, name='outputFileSet', selectmode='extended', width=1, height=1)
outfilepath.grid(row=1, column=1, padx=5, pady=5, sticky='news')
if preferences["fileLocations"]["Output"] == "Unset": outfilepath.insert('end', 'Drag or select Output folder')
else: outfilepath.insert('end', preferences["fileLocations"]["Output"])
# Right Storage File path box

if debug:
    storefilepath = Listbox(root, name='storeFileSet', selectmode='extended', width=1, height=1)
    storefilepath.grid(row=3, column=1, padx=5, pady=5, sticky='ewsn')
    storefilepath.insert('end', preferences["fileLocations"]["Storage"])

def returnContent():
    print(filedrop.get(0,0),lvl=logging.DEBUG)
    print(outfilepath.get(0,0),lvl=logging.DEBUG)
    print(storefilepath.get(0,0),lvl=logging.DEBUG)

# function for file dialouge button
def selectFile(drop):
    filename = fd.askdirectory()
    if filename == '':
        print('Empty, skip')
    else:
        print(f"New filepath: {filename}")
        drop.delete(0,99)
        drop.insert('end', filename)

# outfileselect button
outfileselect = Frame(root)
outfileselect.grid(row=1, column=2, columnspan=2, pady=5, sticky='')
Button(outfileselect, text='...', command=lambda: selectFile(outfilepath), width=5).pack(side=TOP, padx=0)
# storefileselect button
if debug:
    storefileselect = Frame(root)
    storefileselect.grid(row=3, column=2, columnspan=2, pady=5, sticky='')
    Button(storefileselect, text='...', command=lambda: selectFile(storefilepath), width=5).pack(side=TOP, padx=0)

# Tkinter DND Drop function
def drop(event):
    if event.data:
        print('Dropped data:\n', event.data)
        #print_event_info(event)
        if event.widget == filedrop:
            print('FILE DROP')
            # event.data is a list of filenames as one string;
            # if one of these filenames contains whitespace characters
            # it is rather difficult to reliably tell where one filename
            # ends and the next begins; the best bet appears to be
            # to count on tkdnd's and tkinter's internal magic to handle
            # such cases correctly; the following seems to work well
            # at least with Windows and Gtk/X11
            files = filedrop.tk.splitlist(event.data)
            for f in files:
                if os.path.exists(f):
                    print('Dropped file: "%s"' % f,lvl=logging.DEBUG)
                    filedrop.delete(0,99)
                    filedrop.insert('end', f)

                                    
                else:
                    print('Not dropping file "%s": file does not exist.' % f,lvl=logging.DEBUG)
        elif event.widget == outfilepath:
            print('OUT FOLDER')
            files = outfilepath.tk.splitlist(event.data)
            for f in files:
                if os.path.exists(f):
                    print('Dropped file: "%s"' % f,lvl=logging.DEBUG)
                    outfilepath.delete(0,99)
                    outfilepath.insert('end', f)
                    preferences["fileLocations"]["Output"] = str(f)
                else:
                    print('Not dropping file "%s": file does not exist.' % f,lvl=logging.DEBUG)
        elif event.widget == storefilepath:
            print('STORE FOLDER')
            files = storefilepath.tk.splitlist(event.data)
            for f in files:
                if os.path.exists(f):
                    print('Dropped file: "%s"' % f,lvl=logging.DEBUG)
                    storefilepath.delete(0,99)
                    storefilepath.insert('end', f)
                    preferences["fileLocations"]["Storage"] = str(f)
                else:
                    print('Not dropping file "%s": file does not exist.' % f,lvl=logging.DEBUG)
        else:
            print('Error: reported event.widget not known',lvl=logging.ERROR)
    

    with open(f"{os.path.expanduser('~')}\PhotopackConverData\preferences.json", 'w') as f:
        json.dump(preferences, f)
    return event.action


stats = Frame(root, highlightbackground='blue')
stats.grid(row=6, column=0, columnspan=3)
# progress bar (0,0)
Prog = ttk.Progressbar(stats,orient= HORIZONTAL)
Prog.grid(row=0,column=0,padx=5,pady=5,columnspan=4,sticky='new')

# progress pcnt (1,0)
ProgPcnt = Label(stats, text='Precent:')
ProgPcnt.grid(row=1, column=0, padx=5, pady=5,sticky='e')
ProgPcntVal = Label(stats, text='%##.##')
ProgPcntVal.grid(row=1, column=1, padx=5, pady=5,sticky='w')

# progress fraction (1,2)
ProgFract = Label(stats, text='Photos:')
ProgFract.grid(row=1, column=2, padx=5, pady=5,sticky='e')
ProgFractVal = Label(stats, text='##/##')
ProgFractVal.grid(row=1, column=3, padx=5, pady=5,sticky='w')

# Total time label (2,0)
totalTime = Label(stats, text='Total time:')
totalTime.grid(row=2, column=0, padx=5, pady=5,sticky='e')
totalTimeVal = Label(stats, text='##:##')
totalTimeVal.grid(row=2, column=1, padx=5, pady=5,sticky='w')
# start size label (2,2)
startSize = Label(stats, text='Start Size:')
startSize.grid(row=2, column=2, padx=5, pady=5,sticky='e')
startSizeVal = Label(stats, text='##.####')
startSizeVal.grid(row=2, column=3, padx=5, pady=5,sticky='w')
# Number of files in storage folder (3,0)
startFiles = Label(stats, text='start number of files:')
startFiles.grid(row=3, column=0, padx=5, pady=5,sticky='e')
startFilesVal = Label(stats, text='##')
startFilesVal.grid(row=3, column=1, padx=5, pady=5,sticky='w')
# start size label (3,2)
endSize = Label(stats, text='End Size:')
endSize.grid(row=3, column=2, padx=5, pady=5,sticky='e')
endSizeVal = Label(stats, text='##.####')
endSizeVal.grid(row=3, column=3, padx=5, pady=5,sticky='w')
# number of files in output folder (4,0)
numFiles = Label(stats, text='number of files:')
numFiles.grid(row=4, column=0, padx=5, pady=5,sticky='e')
numFilesVal = Label(stats, text='##')
numFilesVal.grid(row=4, column=1, padx=5, pady=5,sticky='w')
# start size label (4,2)
spaceSaved = Label(stats, text='Space Saved:')
spaceSaved.grid(row=4, column=2, padx=5, pady=5,sticky='e')
spaceSavedVal = Label(stats, text='##.####')
spaceSavedVal.grid(row=4, column=3, padx=5, pady=5,sticky='w')
# status of the app (5)
status = Label(stats, text='Status:')
status.grid(row=5, column=1, padx=5, pady=5,sticky='e')
statusVal = Label(stats, text='Inactive', fg='orange', width=50)
statusVal.grid(row=5, column=2, padx=0, pady=0, sticky="w")

# update status function.
def setStatus(text,fg="blue",statusVal=statusVal):
    print('update status',lvl=logging.DEBUG)
    statusVal.config(text=str(text),fg=fg)
    root.update_idletasks()

# gets size of all files in directory (in megabytes)
def get_dir_size(path='.'):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return round(total / (1024 * 1024),4)

# the main conversion function
def photopackConvert(ZipPath,inpath,outpath,statusVal=statusVal):
    other=[]
    pillow_heif.register_heif_opener()
    ZipPath = ZipPath.strip('"')
    root.update_idletasks()
    times = [time.perf_counter()]
    for filename in os.listdir(inpath):
        f = os.path.join(inpath,filename)
        if os.path.isdir(f):
            shutil.rmtree(f)
        else:
            os.remove(f)
    for filename in os.listdir(outpath):
        f = os.path.join(outpath,filename)
        os.remove(f)
    with ZipFile(ZipPath,"r") as zip_ref:
        zip_ref.extractall(inpath)
    times.append(time.perf_counter())
    startFilesVal.config(text=len(os.listdir(inpath)))
    startSizeVal.config(text=get_dir_size(inpath))
    SSize = get_dir_size(inpath)
    numFilesVal.config(text="##")
    totalTimeVal.config(text="##:##")
    endSizeVal.config(text="##.####")
    spaceSavedVal.config(text="##.####")
    print("Extracted")
    print(f"{times[0]-times[1]:0.4f}s")
    # iterate over files in
    # that directory
    i=1
    numPhotos = len(os.listdir(inpath))
    print(f"Num Photos: {numPhotos}")
    pcnt = 00
    Prog['value'] = 0
    ProgPcntVal.config(text=pcnt)
    ProgFractVal.config(text=f'0/{numPhotos}')
    delay = []
    names = []
    for filename in os.listdir(inpath):
        f = os.path.join(inpath, filename)
        # checking if it is a file
        if os.path.isfile(f):
            brekup = filename.split('.')
            extntion = brekup.pop()
            if len(filename)> 8:
                setStatus(text=f"Converting: {filename[0:7]}...{extntion}",fg='blue')
            else:
                setStatus(text=f"Converting: {filename}",fg='blue')
            print("name: ",filename,lvl=logging.DEBUG)
            title = '.'.join(brekup)
            print(f"title: {title}",lvl=logging.DEBUG)
            if title in names:
                other.append(f'dupe;{title}')
            else:
                names.append(title)
            if extntion.upper() == 'PDF':
                other.append(f'pdf')
                print('PDF, Skip',lvl=logging.WARN)
                continue
            img = PIL.Image.open(f)
            size = img.size
            space = os.stat(f).st_size
            half = (round(size[0]/2),round(size[1]/2))
            print("Original size: ",size,lvl=logging.DEBUG)
            print("Original space: ",space,lvl=logging.DEBUG)
            if int(space) >= 300000: 
                print('resize',lvl=logging.DEBUG)
                img.thumbnail(half)
            else:
                print('dont resize',lvl=logging.DEBUG)
            nsize = img.size
            print("New size: ",nsize,lvl=logging.DEBUG)
            if extntion.upper() == 'PNG':
                img.save(outpath+"/"+title+'.png')
                nspace = os.stat(outpath+"/"+title+'.png')
            else:
                img.save(outpath+"/"+title+'.jpg')
                nspace = os.stat(outpath+"/"+title+'.jpg').st_size
            print("New space: ",nspace,lvl=logging.DEBUG)
            now = time.perf_counter()
            ProgFractVal.config(text=f'{i}/{numPhotos}')
            pcnt = round((i/numPhotos)*100,4)
            Prog['value'] = pcnt
            ProgPcntVal.config(text=f'%{pcnt}')
            print(f"image {i}",lvl=logging.DEBUG)
            print(now-times[0],lvl=logging.DEBUG)
            print(f"+{now-times[len(times)-1]}",lvl=logging.DEBUG)
            delay.append(now-times[len(times)-1])
            times.append(time.perf_counter())
        i+=1
    end = time.perf_counter()
    endNum = len(os.listdir(outpath))
    duration = end-times[0]
    ESize = get_dir_size(outpath)
    Savings = SSize - ESize
    return (end,endNum,duration,times,other,names,ESize,Savings)
    #        0     1      2       3     4     5      6     7
# conversion manager
# this is what is called when the convert button is pressed. it gets the values and passes them into the photopackConvert function
def convertFiles(statusVal=statusVal,numFilesVal=numFilesVal,totalTimeVal=totalTimeVal):
    # ConvertButton["state"] = 'disabled'
    setStatus(text="Converting: Starting",fg='blue')
    Zipfile = filedrop.get(0,0)[0]
    outfile = outfilepath.get(0,0)[0]
    if debug:
        storefile = storefilepath.get(0,0)[0]
    else:
        storefile = preferences["fileLocations"]["Storage"]
    data = photopackConvert(Zipfile,storefile,outfile)
    print(data[4],lvl=logging.DEBUG)
    print(data[5],lvl=logging.DEBUG)
    totalTimeVal.config(text=round(data[2],4))
    numFilesVal.config(text=data[1])
    endSizeVal.config(text=data[6])
    spaceSavedVal.config(text=round(data[7],4))
    statStr = "Done"
    statClr = 'green'
    err = False
    if data[1]<30:
        statStr += f", Less than 30 files ({data[1]})"
        statClr = 'red'
        err = True
    if any("dupe" in s for s in data[4]):
        dupes = [s for s in data[4] if "dupe" in s]
        print(dupes,lvl=logging.WARN)
        sting = "Files found with same name, only one photo kept"
        statStr += ', Duplicate files Found'
        if not statClr == 'red': statClr = 'orange'
        for i in dupes:
            fname = i.split(';')[1]
            sting += f"\n {fname}"
        messagebox.showinfo("Duplicate Photos",sting)
        err = True
    if 'pdf' in data[4]:
        statStr += f", PDF in pack, but more than 30 files  ({data[1]})"
        if not statClr == 'red': statClr = 'orange'
        err = True
        messagebox.showinfo("PDF Found","PDF file found in pack")
    if not err:
        statStr += ', files converted'
    setStatus(text=statStr,fg=statClr)
    # ConvertButton["state"] = 'normal'

def convertThread():
    T = threading.Thread(target=convertFiles)
    T.start()

# convert button
ConvertButton = Frame(root)
ConvertButton.grid(row=4, column=0, columnspan=2, pady=5, sticky='new')
Button(ConvertButton, text='Convert', command=convertThread, width=100, height=2, fg="green").pack(side=TOP, padx=5)
# horizontal divider
divide = ttk.Separator(root, orient='horizontal').grid(row=5, column=0, columnspan=3,pady=5,sticky='ew')
divide = ttk.Separator(root, orient='horizontal').grid(row=7, column=0, columnspan=3,pady=5,sticky='ew')
# DB creddits
Cred = Label(root, text='Developed for BPS by Dallin Barker', fg='orange')
Cred.grid(row=8, column=0, columnspan=3, padx=5, pady=5,sticky='n')
# Quit button
buttons = Frame(root)
buttons.grid(row=9, column=0, columnspan=3, pady=5)
Button(buttons, text='Quit', command=root.quit, fg='red').pack(side=LEFT, padx=5)
# Creddits button
Button(buttons, text='Credits', command= lambda: messagebox.showinfo("Credits",f"""
Developed by Dallin Barker for Bright Planet Solar
Ver: {version} 6/13/23
Main Modules: Tkinter, TkinterDND2, Pillow, Pillow-heic
Packaged with Pyinstaller 
Contact: Dallinbarker@gmail.com with any questions or concerns!
"""), fg='blue').pack(side=LEFT, padx=5)
Button(buttons, text='Changelog', command= lambda: webbrowser.open_new(r"https://github.com/StoneCommander/BPSPhotopackConvert/tree/main#changelog") , fg='blue').pack(side=LEFT, padx=5)

# register file drops, and set drop action
filedrop.drop_target_register(DND_FILES)
filedrop.dnd_bind('<<Drop>>', drop)
outfilepath.drop_target_register(DND_FILES)
outfilepath.dnd_bind('<<Drop>>', drop)
def Oclick(event):
    path = outfilepath.get(0,0)[0]
    os.startfile(path)
outfilepath.bind('<Double-Button-1>',Oclick)
def Sclick(event):
    path = storefilepath.get(0,0)[0]
    os.startfile(path)
if debug:
    storefilepath.drop_target_register(DND_FILES)
    storefilepath.dnd_bind('<<Drop>>', drop)
    storefilepath.bind('<Double-Button-1>',Sclick)



root.update_idletasks()
root.deiconify()
root.mainloop()
