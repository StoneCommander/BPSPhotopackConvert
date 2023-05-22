import PIL.Image
from zipfile import ZipFile
import os
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

pillow_heif.register_heif_opener()

"""
PhotopackConvert 0.3.1

Developed for BPS by Dallin Barker
Dallinbarker@gmail.com

"""

# init
root = TkinterDnD.Tk()
root.withdraw()
root.title('PhotopackConvert 0.3.1')
# define grid defaults
root.grid_rowconfigure(1, weight=1, minsize=50)
root.grid_rowconfigure(3, weight=1, minsize=50)
root.grid_columnconfigure(0, weight=1, minsize=30)
root.grid_columnconfigure(1, weight=1, minsize=30)
# Left label
Label(root, text='Drop Photo pack Zip File').grid(
                    row=0, column=0, padx=10, pady=5)
# right label
Label(root, text='Drop Output folder here').grid(
                    row=0, column=1, padx=10, pady=5, columnspan=2)
Label(root, text='drop storage folder here').grid(
                    row=2, column=1, padx=10, pady=5, columnspan=2)
# Left file drop box
filedrop = Listbox(root, name='fileDropbox', selectmode='extended', width=1, height=1)
filedrop.grid(row=1, column=0, padx=5, pady=5, sticky='news',rowspan=3)
filedrop.insert('end', 'Drag Zip file to extract')
# Right Output File path box
outfilepath = Listbox(root, name='outputFileSet', selectmode='extended', width=1, height=1)
outfilepath.grid(row=1, column=1, padx=5, pady=5, sticky='news')
outfilepath.insert('end', 'Drag or select Output folder')
# Right Storage File path box
storefilepath = Listbox(root, name='storeFileSet', selectmode='extended', width=1, height=1)
storefilepath.grid(row=3, column=1, padx=5, pady=5, sticky='ewsn')
storefilepath.insert('end', 'Drag or select Storage folder')

def returnContent():
    print(filedrop.get(0,0))
    print(outfilepath.get(0,0))
    print(storefilepath.get(0,0))


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
storefileselect = Frame(root)
storefileselect.grid(row=3, column=2, columnspan=2, pady=5, sticky='')
Button(storefileselect, text='...', command=lambda: selectFile(storefilepath), width=5).pack(side=TOP, padx=0)



# define action on file drop
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
                    print('Dropped file: "%s"' % f)
                    filedrop.delete(0,99)
                    filedrop.insert('end', f)

                                    
                else:
                    print('Not dropping file "%s": file does not exist.' % f)
        elif event.widget == outfilepath:
            print('OUT FOLDER')
            files = outfilepath.tk.splitlist(event.data)
            for f in files:
                if os.path.exists(f):
                    print('Dropped file: "%s"' % f)
                    outfilepath.delete(0,99)
                    outfilepath.insert('end', f)
                else:
                    print('Not dropping file "%s": file does not exist.' % f)
        elif event.widget == storefilepath:
            print('STORE FOLDER')
            files = storefilepath.tk.splitlist(event.data)
            for f in files:
                if os.path.exists(f):
                    print('Dropped file: "%s"' % f)
                    storefilepath.delete(0,99)
                    storefilepath.insert('end', f)
                else:
                    print('Not dropping file "%s": file does not exist.' % f)
        else:
            print('Error: reported event.widget not known')
    return event.action




# Total tile label
totalTime = Label(root, text='Total time:')
totalTime.grid(row=6, column=0, padx=10, pady=5,sticky='e')
totalTimeVal = Label(root, text='##:##')
totalTimeVal.grid(row=6, column=1, padx=10, pady=5,sticky='w')
startFiles = Label(root, text='start number of files:')
startFiles.grid(row=7, column=0, padx=10, pady=5,sticky='e')
startFilesVal = Label(root, text='##')
startFilesVal.grid(row=7, column=1, padx=10, pady=5,sticky='w')
numFiles = Label(root, text='number of files:')
numFiles.grid(row=8, column=0, padx=10, pady=5,sticky='e')
numFilesVal = Label(root, text='##')
numFilesVal.grid(row=8, column=1, padx=10, pady=5,sticky='w')
status = Label(root, text='Status:')
status.grid(row=9, column=0, padx=10, pady=5,sticky='e')
statusVal = Label(root, text='Inactive', fg='orange', width=30)
statusVal.grid(row=9, column=1, padx=0, pady=0, sticky="w")

def setStatus(text,fg="blue",statusVal=statusVal):
    print('update status')
    statusVal.config(text=str(text),fg=fg)
    root.update_idletasks()


def photopackConvert(ZipPath,inpath,outpath,statusVal=statusVal):
    other=[]
    pillow_heif.register_heif_opener()
    ZipPath = ZipPath.strip('"')
    startFilesVal.config(text=len(os.listdir(inpath)))
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
    print("Extracted")
    print(f"{times[0]-times[1]:0.4f}s")
    # iterate over files in
    # that directory
    i=1
    numPhotos = len(os.listdir(inpath))
    print(f"Num Photos: {numPhotos}")
    delay = []
    names = []
    for filename in os.listdir(inpath):
        f = os.path.join(inpath, filename)
        if filename in names:
            other.append(f'dupe;{filename}')
        else:
            names.append(filename)
        # checking if it is a file
        if os.path.isfile(f):
            brekup = filename.split('.')
            extntion = brekup.pop()
            if len(filename)> 8:
                setStatus(text=f"Converting: {filename[0:7]}...{extntion}",fg='blue')
            else:
                setStatus(text=f"Converting: {filename}",fg='blue')
            print("name: ",filename)
            title = '.'.join(brekup)
            if extntion.upper() == 'PDF':
                other.append(f'pdf')
                print('PDF, Skip')
                continue
            img = PIL.Image.open(f)
            size = img.size
            half = (round(size[0]/2),round(size[1]/2))
            print("Original size: ",size)
            img.thumbnail(half)
            nsize = img.size
            print("New size: ",nsize)
            if extntion.upper() == 'PNG':
                img.save(outpath+"/"+title+'.png')
            else:
                img.save(outpath+"/"+title+'.jpg')
            now = time.perf_counter()
            print(f"image {i}")
            print(now-times[0])
            print(f"+{now-times[len(times)-1]}")
            delay.append(now-times[len(times)-1])
            times.append(time.perf_counter())
        i+=1
    end = time.perf_counter()
    endNum = len(os.listdir(outpath))
    duration = end-times[0]
    return (end,endNum,duration,times,other)

def convertFiles(statusVal=statusVal,numFilesVal=numFilesVal,totalTimeVal=totalTimeVal):
    setStatus(text="Converting: Starting",fg='blue')
    Zipfile = filedrop.get(0,0)[0]
    outfile = outfilepath.get(0,0)[0]
    storefile = storefilepath.get(0,0)[0]
    data = photopackConvert(Zipfile,storefile,outfile)
    totalTimeVal.config(text=data[2])
    numFilesVal.config(text=data[1])
    if data[1]<30:
        if 'pdf' in data[4]:
            setStatus(text=f"Done. WARNING, Less than 30 files ({data[1]}), PDF in pack.",fg='red')
        else:
            setStatus(text=f"Done. WARNING, Less than 30 files ({data[1]})",fg='red')
    elif 'pdf' in data[4]:
        setStatus(text=f"Done. WARNING, PDF in pack, but more than 30 files  ({data[1]})",fg='orange')
    else:
        setStatus(text=f"Done. files converted",fg='green')

# convert button
ConvertButton = Frame(root)
ConvertButton.grid(row=4, column=0, columnspan=2, pady=5, sticky='new')
Button(ConvertButton, text='Convert', command=convertFiles, width=100, height=2, fg="green").pack(side=TOP, padx=5)
# horizontal divider
divide = ttk.Separator(root, orient='horizontal').grid(row=5, column=0, columnspan=3,pady=5,sticky='ew')
divide = ttk.Separator(root, orient='horizontal').grid(row=10, column=0, columnspan=3,pady=5,sticky='ew')
# DB creddits
Cred = Label(root, text='Developed for BPS by Dallin Barker', fg='orange')
Cred.grid(row=11, column=0, columnspan=3, padx=10, pady=5,sticky='n')
# Quit button
buttons = Frame(root)
buttons.grid(row=12, column=0, columnspan=3, pady=5)
Button(buttons, text='Quit', command=root.quit, fg='red').pack(side=LEFT, padx=5)
# Creddits button
def messageWindow():
    win = Toplevel()
    win.title('warning')
    message = "This will delete stuff"
    Label(win, text=message).pack()
    Button(win, text='Delete', command=win.destroy).pack()

Button(buttons, text='Credits', command= lambda: messagebox.showinfo("Credits","""
Developed by Dallin Barker for Bright Planet Solar
Ver: 0.3.1 5/22/23
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
storefilepath.drop_target_register(DND_FILES)
storefilepath.dnd_bind('<<Drop>>', drop)



root.update_idletasks()
root.deiconify()
root.mainloop()