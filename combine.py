import Image
import math
import operator

def find_common(im1, im2):
    sector = int(im1.size[0] *0.002)
    l = im1.crop((im1.size[0]-sector,0,im1.size[0], im1.size[1]))
    rms_list= []
    for i in range(0,1000):
        r = im2.crop((i,0,sector+i, im2.size[1]))
        h1 = l.histogram()
        h2 = r.histogram()
        rms = math.sqrt(reduce(operator.add,
            map(lambda a,b: (a-b)**2, h1, h2))/len(h1))
        rms_list.append(rms)
    m = min(rms_list)
    return (rms_list.index(m), sector)

def merge_images(im1, im2, rshift, sector):
    w = im1.size[0]
    temp = im1.crop((0,0,im2.size[0]-rshift, im2.size[1]))
    
    new_im = Image.new("RGB",(w * 2 - rshift -sector,im2.size[1]), "black")
    new_im.paste(im2,(w-rshift,0))
    new_im.paste(temp,(0,0))

 
    return new_im
    

def main():
    im1 = Image.open('photo/1.jpg')
    im2 = Image.open('photo/2.jpg')
    ralign, sector = find_common(im1, im2)
    new_im = merge_images(im1, im2, ralign,sector )
    new_im.save('test.jpg','JPEG')
    
main()
