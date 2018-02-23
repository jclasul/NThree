
# coding: utf-8

# In[324]:


import PIL
import numpy as np
import pandas as pd
import os, sys
import matplotlib.pyplot as plot

FILE_DIR = "C:/Users/jan.claes/Desktop/EXP_3"

FileLS = []
for file in os.listdir(FILE_DIR):
    if file.endswith(('.jpg','.png','.PNG')) and file.find("_REDUCED") <= 4:
        FileLS.append(file)

COUNT = 0
while COUNT < len(FileLS):

    # In[297]:


    size = (1280,1280)
    FILE_PATH = os.path.join(FILE_DIR,FileLS[COUNT])
    img = PIL.Image.open(FILE_PATH).convert("RGB").resize(size)
    size = img.size


    # In[298]:


    img.show()


    # In[299]:


    '''# MAKE BLACK IMAGE
    size = (1280,1280)
    img = PIL.Image.new("RGB",size=size, color='black')
    img_l = img.load()'''


    # In[300]:


    '''# TESTING
    rand = np.random.randint(140,200,2)

    place = np.random.randint(0,3,2)
    ls = [0,0,0]

    ls[place[0]] = rand[0]
    ls[place[1]] = rand[1]

    PIL.Image.new("RGB", size=(128,128), color=tuple(ls))'''


    # In[301]:


    '''randnr = np.random.randint(0,img.size[0]+1-100,(25,2))

    for randi,randj in randnr:

            
        try:
            for i in range(randi,randi+np.random.randint(10,128)):
                if i % 50 == 0 or i == 0:
                    rand = np.random.randint(140,168,2)
                    place = np.random.randint(0,3,2)
                    ls = [0,0,0]
                    ls[place[0]] = rand[0]
                    ls[place[1]] = rand[1]
                    colours = tuple(ls)
                else:
                    colours = tuple(ls)
                for j in range(randj,randj+np.random.randint(0,255)):         
                    PIL.Image.Image.getdata(img).putpixel((i,j),colours)
                    
            for j in range(randi,randi+np.random.randint(10,128)):
                if j % 50 == 0 or j == 0:
                    rand = np.random.randint(140,168,2)
                    place = np.random.randint(0,3,2)
                    ls = [0,0,0]
                    ls[place[0]] = rand[0]
                    ls[place[1]] = rand[1]
                    colours = tuple(ls)
                else:
                    colours = tuple(ls)
                for i in range(randj,randj+np.random.randint(0,255)):         
                    PIL.Image.Image.getdata(img).putpixel((i,j),colours)
                    
                    
        except IndexError:
            continue
    img'''


    # In[302]:


    img_resize = img.resize((128,128))
    #plot.imshow(img_resize)


    # In[303]:


    img_np = np.asarray(img)
    '''
    red = img_np[:,:,0]
    img_red = PIL.Image.fromarray(red)

    green = img_np[:,:,1]
    img_green = PIL.Image.fromarray(green)

    blue = img_np[:,:,2]
    img_blue = PIL.Image.fromarray(blue) '''


    # In[304]:


    LS = []

    for i in range(0,len(img_np)):
        for j in range(0,len(img_np)):
            #if (img_np[i,j,0] > 120 and img_np[i,j,1] < 100 and img_np[i,j,2] < 100) or (img_np[i,j,0] > 90 and img_np[i,j,1] < 35 and img_np[i,j,2] < 35):
            if (img_np[i,j,0] > 90 and img_np[i,j,1] < 85 and img_np[i,j,2] < 85): 

                LS.append(tuple([i,j]))


    # In[305]:


    ne = PIL.Image.new("RGB", size=size, color=tuple([0,0,0]))
    #ne = img
    #ne.putalpha(128)
    colours = tuple([167,0,0])
    for i,j in LS:
        try:      
            PIL.Image.Image.getdata(ne).putpixel((j,i),colours)
        except IndexError:
            continue  

    #ne.show()


    # In[306]:


    LS = []

    img_np = np.asarray(img_resize)
    colours = tuple([167,0,0])

    for i in range(0,len(img_np)):
        for j in range(0,len(img_np)):
            if img_np[i,j,0] > 100 and img_np[i,j,1] < 100 and img_np[i,j,2] < 100:
                LS.append(tuple([i,j]))
                
    neSMALL = PIL.Image.new("RGB", size=tuple([len(img_np),len(img_np)]), color=tuple([0,0,0]))
    #neSMALL = img_resize
    #neSMALL.putalpha(85)
    for i,j in LS:
        try:
            PIL.Image.Image.getdata(neSMALL).putpixel((j,i),colours)        
        
        except IndexError:
            continue
            
    #neSMALL.show()


    # In[307]:


    imgs = [neSMALL.resize(img.size),ne.resize(img.size),img.resize(img.size)]
    OO = np.hstack(np.asarray(img) for img in imgs)
    IMG = PIL.Image.fromarray(OO)
    #IMG.show()


    # In[308]:


    FT, EXT = os.path.splitext(os.path.split(FILE_PATH)[-1])
    REF = FT + "_REDUCED_OVERLAY" + EXT
    REF = os.path.join(os.path.split(FILE_PATH)[0],REF)

    IMG.save(REF)


    # In[309]:


    red_vals = pd.DataFrame(np.asarray(ne)[:,:,0])


    # In[310]:


    LS = []
    LS_R = []

    for j in range(0,red_vals.shape[1]):
        if red_vals.iloc[:,j].sum() != 0:
            LS.append(j)
            
    for i in range(0,red_vals.shape[1]):
        if red_vals.iloc[i,:].sum() != 0:
            LS_R.append(i)
                


    # In[311]:


    REDUCED = PIL.Image.fromarray(np.asarray(red_vals.iloc[LS_R,LS]))


    # In[313]:


    REDUCED.show()


    # In[314]:


    FT, EXT = os.path.splitext(os.path.split(FILE_PATH)[-1])
    REF = FT + "_REDUCED" + EXT
    REF = os.path.join(os.path.split(FILE_PATH)[0],REF)

    REDUCED.save(REF)


    # In[315]:


    RED_np = np.asarray(REDUCED.resize(img_resize.size))


    # In[316]:


    #PIL.Image.fromarray(RED_np).show()


    # In[317]:


    FT, EXT = os.path.splitext(os.path.split(FILE_PATH)[-1])
    REF = FT + "_REDUCED_small" + EXT
    REF = os.path.join(os.path.split(FILE_PATH)[0],REF)

    PIL.Image.fromarray(RED_np).save(REF)

    COUNT += 1


    # In[318]:


    '''
    imgs = [img_red.convert("RGB"),img_green.convert("RGB"),img_blue.convert("RGB"),img]
    OO = np.hstack(np.asarray(img) for img in imgs)
    IMG = PIL.Image.fromarray(OO)
    IMG'''


    # In[319]:


    '''PIL.Image.new("RGB", size=(128,128), color=tuple([167,0,0]))'''


    # In[320]:


    '''I = 200
    J = 1000
    STEP = 200
    img_np = np.asarray(img)

    croped = tuple([I,J,I+STEP,J+STEP])
    img_crop = PIL.Image.Image.crop(img,croped)
    img_crop_red = PIL.Image.fromarray(np.asarray(pd.DataFrame(img_np[:,:,0]).loc[J:J+STEP,I:I+STEP])).convert("RGB")
    img_crop_green = PIL.Image.fromarray(np.asarray(pd.DataFrame(img_np[:,:,1]).loc[J:J+STEP,I:I+STEP])).convert("RGB")
    img_crop_blue = PIL.Image.fromarray(np.asarray(pd.DataFrame(img_np[:,:,2]).loc[J:J+STEP,I:I+STEP])).convert("RGB")'''


    # In[321]:


    '''plot.figure()
    print("RGB Image resized ALL")
    plot.imshow(img.resize(tuple([STEP,STEP])))
    plot.show()
    print("RGB Image cropped")
    plot.imshow(img_crop)
    plot.show()
    print("Red Image")
    plot.imshow(img_crop_red)
    plot.show()
    print("Green Image")
    plot.imshow(img_crop_green)
    plot.show()
    print("Blue Image")
    plot.imshow(img_crop_blue)
    plot.show()'''


    # In[322]:


    '''redie = np.asarray(img_crop_red)[:,:,0] '''


    # In[323]:


    '''LS = []

    for i in range(0,len(redie)):
        for j in range(0,len(redie)):
            if redie[i,j] < 210 and redie[i,j] > 100 and np.asarray(img_crop_blue)[i,j,0] < 20 and np.asarray(img_crop_green)[i,j,0] < 20:
                LS.append(tuple([i,j]))'''

