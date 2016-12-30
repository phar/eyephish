from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cv2
import numpy
import operator
import argparse
import itertools

###############
# -phar
##############

DIALECTS = {
"latin":			(0x0000,0x007f),
"cyrillic":			(0x0400,0x04ff),
"greek":			(0x0370,0x03ff),
"armenian":			(0x0530,0x058f),
"hebrew":			(0x0590,0x05ff),
"arabic":			(0x0600,0x06ff),
"cherokee":         (0x13a0,0x13ff),
"kanji":			(0x4E00,0x9FBF),
"hiragana":			(0x3040,0x309F),
"katakana":			(0x30A0,0x30FF),
"bopomofo":			(0x3100,0x312f),
"thai":				(0x0e00,0xe7f)


}



def get_homograph_canvas_size(im, contour):
	maxx = 0
	minx = im.shape[0]
	maxy = 0
	miny = im.shape[1]
	
	for c in contour:
		(x,y,w,h) = cv2.boundingRect(c)
		
		if x < minx:
			minx = x
		if y < miny:
			miny = y
		if (x + w) > maxx:
			maxx = (x + w)
		if (y + h) > maxx:
			maxy = (y + h)
	return (minx,maxx,miny,maxy)




def homograph_score(im1, c1, im2, c2):
	im3 = cv2.absdiff(im1,im2)
	#cv2.imshow("Keypoints", im1)
	#cv2.imshow("Keypoints2", im2)
	#cv2.imshow("Keypoints3", im3)
	#cv2.waitKey(200)

	#ok mr o'horo... just the bare match
	basic_score =  im3.sum()/(im3.shape[0] * im3.shape[1])

	#try a wide match (stretch im2 to the width of im1 and try it again
	#	tim = Image.fromarray(im1)
	
	(minx1,max1,miny1,maxy1) = get_homograph_canvas_size(im1,c1)
	(minx2,max2,miny2,maxy2) = get_homograph_canvas_size(im2,c2)
	
	c1xr = float(max2-minx2)/float(max1-minx1)
#	c1yr = (may2-miny2)/(may1-miny1)
	c1yr = 1.0

	print float(max2-minx2),float(max1-minx1),c1xr
	
#convert to PIL then resize and recenter it
	tim = Image.fromarray(im2)
	cv2.imshow("boooout1", numpy.array(tim))
	tim = tim.resize((int(im1.shape[1] * c1xr), int(im2.shape[0] / c1yr)), Image.ANTIALIAS)

	cv2.imshow("boooin", numpy.array(im1))
	cv2.imshow("boooout2", numpy.array(tim))
	cv2.waitKey(100)
	return basic_score


def get_centroidized_unicode_img(testchr,font, fontsize = 16,chrwidth = 1):

	ttf=ImageFont.truetype(font, fontsize)

	testw = 40 * chrwidth
	testh = 40

#crap out an image with a charcter in it, in a reasonable location
	im1 = Image.new("RGB", (testw,testh), "white")
	ImageDraw.Draw(im1).text((testh/3,testw/3),testchr, fill='black', font=ttf)
	imx = numpy.array(im1)

#find contours of the image we place
	imgray = cv2.cvtColor(imx,cv2.COLOR_BGR2GRAY)
	ret,thresh = cv2.threshold(imgray,127,255,cv2.THRESH_BINARY)
	contours,j = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	im3 = cv2.drawContours(imx, contours[1:], -1, (0,255,0), 1)

#calculate the centroid of all the marks making up the charcter
	cxx = []
	cxy = []
	for c in contours[1:]:
		
		M = cv2.moments(c)
		try:
			cxx.append(int(M['m10']/M['m00']))
			cxy.append(int(M['m01']/M['m00']))
		except:
#			cv2.imshow("booo", numpy.array(imx))
#			cv2.waitKey(100)
			pass

	if  len(cxx):
		cx = sum(cxx) / len(cxx)
	else:
		cx = 0
	if  len(cxy):
		cy = sum(cxy) / len(cxy)
	else:
		cy = 0
	cx =  (testw/2) - (cx - (testw/3))
	cy = (testh/2) - (cy - (testh/3))

#recreate the image with the character now centered
	im1 = Image.new("RGB",  (testw,testh), "white")
#	ImageDraw.Draw(im1).text((cx,cy),testchr, fill='black', font=ttf) #X and Y
	ImageDraw.Draw(im1).text((cx,0),testchr, fill='black', font=ttf) #X only

	return (numpy.array(im1),contours[1:])


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--inputstring",type=str, help="string you would like to generate look-a-likes for, can be unicode",required=True)
	parser.add_argument("--threshold", default=5, type=float, help="set the visual match threshold, lower is a better match")
	parser.add_argument("--dialect", type=str, help="which unicode tableset to look to generation from (%s)" % ",".join(DIALECTS),required=True)
	parser.add_argument("--font",default = "Arial", type=str, help="font to use, Arial,Tahoma for browsers")
	parser.add_argument("--multichr",default = 0,type=int, help="enable multi letter matches, takes longer")
	parser.add_argument("--multichrmax",default = 2,type=int, help="maximum number of characters to try matching, more takes longer, default 2")

	args = parser.parse_args()

	newstring = []
	stringoptions = []
	
	if args.multichr == 0:
		letterscnt = 1
	else:
		letterscnt = args.multichrmax

	for i in args.inputstring:
		(im1,contours1) = get_centroidized_unicode_img(i,args.font,chrwidth=letterscnt)
		hscores = {}
		thistring = []
		thistring.append(i)
		
		chrrange = [ unichr(x) for x  in range(DIALECTS[args.dialect][0],DIALECTS[args.dialect][1])]
						  
		for e in itertools.combinations_with_replacement(chrrange,letterscnt):
			(im2,contours2) = get_centroidized_unicode_img("".join(e),args.font,chrwidth=letterscnt)
			
			hscores[e] = homograph_score(im1, contours1, im2,contours2)

		sortedhscores = sorted(hscores.items(), key=operator.itemgetter(1))
		for score in sortedhscores:
			if score[1] < args.threshold:
				thistring.append(score[0])
			else:
				break

		stringoptions.append(thistring)

	done = 0
	i = 0
	while done == 0:
		fc = 0
		if i == 0:
			lbuff = ['*']
		else:
			lbuff = ['>']
		for s in stringoptions:
			try:
				lbuff.append( s[i])
			except:
				fc += 1
				lbuff.append(" ")
		i+=1
		if fc == len(stringoptions):
			done = 1
		else:
			print "".join(lbuff), lbuff[1:]
