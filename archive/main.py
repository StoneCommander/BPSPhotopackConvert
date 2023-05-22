from PIL import Image
import console
from zipfile import ZipFile
import os
import pillow_heif
import shutil
import time
from pdf2image import convert_from_path

pillow_heif.register_heif_opener()

# image = Image.open('working/18.HEIC')

# image.save('working/18.jpg')

def photopackConvert(ZipPath,inpath,outpath):
	ZipPath = ZipPath.strip('"')
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
	for filename in os.listdir(inpath):
		f = os.path.join(inpath, filename)
		# checking if it is a file
		if os.path.isfile(f):
			print("name: ",filename)
			brekup = filename.split('.')
			extntion = brekup.pop()
			title = '.'.join(brekup)
			if extntion == "pdf":
				img = convert_from_path(f)
			else:
				img = Image.open(f)
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
			console.pbar(i/numPhotos,'_',showPcnt=True)
			console.line('=')
		i+=1
	end = time.perf_counter()
	endNum = len(os.listdir(outpath))
	duration = end-times[0]
	return (end,endNum,duration,times)

inpath = r"C:\Users\Dallin Barker\Documents\PhotopackConverrt\Input"
outpath = r"C:\Users\Dallin Barker\Documents\PhotopackConverrt\out"
first = True

if __name__ == "__main__":
	while True:
		console.clear()
		console.line('=')
		photopackConvert(input("Zip File Path: "),inpath,outpath)


