from PIL import Image
import numpy as np
import sys

def cutDown (Matrix, Value):
	for y in range(0, len(Matrix)):
		for x in range(0, len(Matrix[0])):
			if(np.abs(Matrix[y][x]) < Value):
				Matrix[y][x] = 0 + 0j
			else:
				Matrix[y][x] = np.around(Matrix[y][x])
	return Matrix
		
def m2f (Matrix, File):
	outfile = open(File+".txt", "w")
	outfile.write(str(len(Matrix)) + " " + str(len(Matrix[0]))+"\n")
	
	for y in range (0, len(Matrix)):
		for x in range(0, len(Matrix[0])):
			if(np.abs(Matrix[y][x] != 0)):
				outfile.write(str(y) + " " + str(x) + " " + str(Matrix[y][x])+"\n")
	outfile.close()
	
ImageFile = sys.argv[1]	#ime fajla

if(ImageFile[-4:] == ".jpg"):	#fft
	
	Value = int(sys.argv[2]) 	#vse nizje vrednosti v fft2 porezemo
	
	photo = Image.open(ImageFile).convert('L')	#odprem sliko v crno beli
	photo.show()
	
	data = np.asarray(photo)	#matrika sivosti slike
	dataFFT = np.fft.rfft2(data)	#fft2 matrike
	
	dataFFTNovo = cutDown(dataFFT, Value)	#porezem vrednosti in zaokrozim
	m2f(dataFFTNovo, ImageFile)				#shranim novo fft matriko v fajel
	
	dataNovo = np.fft.irfft2(dataFFTNovo)	#pretvorim nazaj v podatke
	Image.fromarray(dataNovo.astype(np.uint8)).show()	#prikazem rezulata

elif(ImageFile[-4:] == ".txt"):
	#ifft
	file = open(ImageFile, "r")
	lines = file.readlines()
	size = lines[0].strip().split(" ")
	
	MatrixFFT = [[0 for x in range(int(size[1]))] for y in range(int(size[0]))] 
	
	for lineId in range(1, len(lines)):
		data = lines[lineId].split(" ")
		y = int(data[0])
		x = int(data[1])
		value = complex(data[2])

		MatrixFFT[y][x] = value
		
	
	file.close()

	dataNovo = np.fft.irfft2(MatrixFFT)	#pretvorim nazaj v podatke
	Image.fromarray(dataNovo.astype(np.uint8)).show()	#prikazem rezulata

else:
	print ".jpg or .txt or die()"

