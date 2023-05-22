# imports
import os
import platform
from tkinterdnd2 import *
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from main import photopackConvert
# init
root = TkinterDnD.Tk()
root.withdraw()
root.title('TkinterDnD demo')
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
numFiles = Label(root, text='num of files:')
numFiles.grid(row=7, column=0, padx=10, pady=5,sticky='e')
numFilesVal = Label(root, text='##')
numFilesVal.grid(row=7, column=1, padx=10, pady=5,sticky='w')
status = Label(root, text='Status: ')
status.grid(row=8, column=0, padx=10, pady=5,sticky='e')
statusVal = Label(root, text='Inactive', fg='orange')
statusVal.grid(row=8, column=1, padx=10, pady=5,sticky='w')


def convertFiles(statusVal=statusVal,numFilesVal=numFilesVal,totalTimeVal=totalTimeVal):
    statusVal.config(text="Converting",fg='blue')
    Zipfile = filedrop.get(0,0)[0]
    outfile = outfilepath.get(0,0)[0]
    storefile = storefilepath.get(0,0)[0]
    data = photopackConvert(Zipfile,storefile,outfile)
    totalTimeVal.config(text=data[2])
    numFilesVal.config(text=data[1])
    if data[1]<30:
        statusVal.config(text=f"Done. WARNING, Less than 30 files ({data[1]})",fg='red')
    else:
        statusVal.config(text=f"Done. files converted",fg='green')

# convert button
ConvertButton = Frame(root)
ConvertButton.grid(row=4, column=0, columnspan=2, pady=5, sticky='new')
Button(ConvertButton, text='Convert', command=convertFiles, width=100).pack(side=TOP, padx=5)
# horizontal divider
divide = ttk.Separator(root, orient='horizontal').grid(row=5, column=0, columnspan=2,pady=5,sticky='ew')
divide = ttk.Separator(root, orient='horizontal').grid(row=9, column=0, columnspan=2,pady=5,sticky='ew')
# Quit button
QuitButton = Frame(root)
QuitButton.grid(row=10, column=0, columnspan=2, pady=5)
Button(QuitButton, text='Quit', command=root.quit).pack(side=LEFT, padx=5)

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