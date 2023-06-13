# BPSPhotopackConvert
 Developed by Dallin Barker for Bright Planet Solar  
 **Ver: 0.4.0 5/22/23**
## Modules Used:
 Tkinter, TkinterDND2, Pillow, Pillow-heic.  
 Packaged with Pyinstaller  
## Contact:
Email Dallinbarker@gmail.com with any questions or concerns!
# Usage
## Download
download the latest version of the PhotopackConverter by clicking on the latest version on the right. or [CLICK HERE](https://github.com/StoneCommander/BPSPhotopackConvert/releases/latest)  
your computer may try to stop you from downloading it, due to it being an .EXE file. most browsers should let you keep it if you prompt it.
once it is downloaded. feel free to move to wherever you need it. to run it, just double click the icon.  
again, the computer likely will block your attempt. just click more info, then run anyway.
if you have any problems with downloading or running the program, contact me!
## setting up the converter
once the application oppens, it will look like this:
![Photo of the PhotopackConvert App](https://i.imgur.com/cZMlTHo.png)  
on your desktop. (or wherever you please) create 2 folders, one of them for internal storage, and one for the outputted photos, the name does not matter.  
I recomend keeping the folders somewhere acsessable, since you will need to reset them in the aplication each time you open it  
eventualy, I plan on making it save your choice, and remove the need for a storage folder entirely. but that will come later
once creted drag and drop your output folder onto the top right box. if you need to, click on the 3 dots to open up a file dialouge to help you locate the folder   
![Photo of the output folder being dragged to the output selction](https://i.imgur.com/K1DuWFh.png)  
then do the same thing with your storage folder  
![Photo of the storage folder being dragged to the storage selction](https://i.imgur.com/XJNHPSE.png)  
## using the converter  
to use the converter, download the google drive zip folder.    
**make sure you dont download the funding submision folder!** go into the folder, select all (ctrl+A), then right click and select download   
once the zip is downloaded, drag the zip folder onto the the Zip file box.  
![Photo of the Photopack zip folder being dragged to the zip file box](https://i.imgur.com/ykPhW27.png)  
then press convert! the photopack will automaticly go through and:
- extract all the photos
- convert HEIC photos into JPG's
- downsize all photos 50%  
cutting out the need for the time consuming conversion proscess  
then, open your output folder, and take the photos and upload them as you normaly would!
## recomended layout
to maximise efficency, i would recomend laying out your desktop in a way so you can easily acsess all the windos you need  
here is the layout i use:  
on the right, ihave a full chrome tab, with the photopack insightly list, parent projct, and install google drive  
on the left, i have it aranged so the sunrun community upload photos tab takes up the left side of my screen.  
the PhotopackConvert app is in the top right quadrant,  
and the output folder is in the bottom right quadrant.  
![photo of the layout described above](https://i.imgur.com/J3vwiQd.png)
you can arrange it however you want. but this way will allow you to take the zip file, drag it to the converter, then take the output files and drag them to the upload, without having to rearange your windows. 
## Errors
if you encounter an error, a window will pop up and tell you the error, and the status also list the errors.  
### Not Enough Photos
when you get this error, it means that the output folder contains less than 30 photos. this can happen for a number of reasons. if the only error is that there are less than 30 files, check to make sure that there are 30 photos in the zip file. if there are, and it still outputs less than 30. check to see if there are any weird file types. if you cant figure out the problem. Email me the BPS number and an explination. i will try to fgure it out, and see if there is an error in the code.
### PDF in pack
if you get this error, regardless if there are 30 photos or not. check the zip file to see which file is the PDF, it is most comonly the screenshots (30,31,70,70.1,70.2,75, and 77). if it is a reqired photo, then take a screenshot and redownload the zip. if it is not a required photo, move a diffrent photo into the funding sumbision and redownload the pack. 
### Duplicate Photos
if you get this error, it should tell you the filename that has a duplicate, and only one is kept. this happens when there are 2 photos with the same name, but diffrent exstention (Ex. 6.JPG and 6.HEIC). if this happens, you can rename one of the photos, or bring in an extra photo to replace it. 

# Changelog
## 1.0.0 6/13/23

### Main Features
- Storage folder is now automatically set, and was removed from the screen
- The selected output folder will now be remembered after you close the app

### Improvements
- You can now double click the output folder box to open the selected folder.
- updated stats bar to include photo pack size stats

### Internal changes
 - Reworked stats display internally
 - added debug mode for testing
 - added full preferences file reading and updating

**Full Changelog**: [0.4.2...1.0.0](https://github.com/StoneCommander/BPSPhotopackConvert/compare/0.4.2...1.0.0)

## 0.4.2, 6/6/23

### Improvements:
Added double click on folder.  
double click on the output or storage folder drop box to open the selected folder.

## 0.4.1, 5/25/23

### Improvements:
added photo size check, wont downsize photos smaller than 300KB

## 0.4.0, 5/22/23

### Main Feature
Add error check for duplicate photos.  
checks if there are multiple photos with the same name (different extension)  
will return an error when detected  
### Improvements
- changed how errors with converting are handled.
- added error windows for each error.   
### Bugs
- Fixed start number of files being inaccurate

## 0.3.1, 5/22/253
totally forgot to change the version and date in the code. oops (－‸ლ)

## 0.3.0, 5/22/23
Added button that links to the changelog.

## 0.2.0, 5/3/23
minor changes. visual improvements
(yes i know it doesnt fit Semantic Versioning. deal with it)

## 0.1.0, 5/1/23
first Release, general uses, fully functional.
