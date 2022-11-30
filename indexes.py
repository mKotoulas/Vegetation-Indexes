from constants import *
from PIL import Image
import numpy as np   
import matplotlib.pyplot as plt    
from os import makedirs,listdir 
from pathlib import Path   

def calculate_gli(img):
    arr = np.asarray(img).astype(float) 
    gli_array = (2*arr[:,:,1]-arr[:,:,0]-arr[:,:,2])/(2*arr[:,:,1]+arr[:,:,0]+arr[:,:,2])            
    gli_array[np.isnan(gli_array)] = 0  
    return gli_array  

def calculate_vari(img):  
    arr = np.asarray(img).astype(float) 
    vari_array = (arr[:,:,1]-arr[:,:,0])/(arr[:,:,1]+arr[:,:,0]-arr[:,:,2])           
    vari_array[np.isnan(vari_array)] = 0 
    return vari_array  

def calculate_vigreen(img):
    arr = np.asarray(img).astype(float) 
    vi_array = (arr[:,:,1]-arr[:,:,0])/(arr[:,:,1]+arr[:,:,0])             
    vi_array[np.isnan(vi_array)] = 0  
    return vi_array
  

def create_images(img_path,color,index_name): 
    img = Image.open(img_path) 
    if img.mode!="RGB":return  
    if index_name=='VARI':array=calculate_vari(img)
    elif index_name=="VI":array=calculate_vigreen(img)  
    else:array=calculate_gli(img)   
    vmin = np.percentile(array, 10)  
    vmax = np.percentile(array, 90)  
    fig, ax = plt.subplots(figsize = (10,5), dpi =200) #plt.subplots(figsize=(6,3),dpi=200)     
    cim = ax.imshow(array, vmin = vmin, vmax = vmax,cmap=color,aspect="auto") 
    cbar= fig.colorbar(cim)  
    cbar.set_label(index_name)    
    ax.set_xticks([])
    ax.set_yticks([])
    if index_name=="VARI":
        if color=="gray":save_path=f"{VARI_IMAGES_GRAY}/{img_path.stem}_grayscale{img_path.suffix}"
        else:save_path=f"{VARI_IMAGES_COLOR}/{img_path.stem}_colormap{img_path.suffix}"  
    if index_name=="GLI":
        if color=="gray":save_path=f"{GLI_IMAGES_GRAY}/{img_path.stem}_grayscale{img_path.suffix}" 
        else:save_path=f"{GLI_IMAGES_COLOR}/{img_path.stem}_colormap{img_path.suffix}" 
    if index_name=="VI": 
        if color=="gray":save_path=f"{VI_IMAGES_GRAY}/{img_path.stem}_grayscale{img_path.suffix}" 
        else:save_path=f"{VI_IMAGES_COLOR}/{img_path.stem}_colormap{img_path.suffix}"  
    fig.savefig(save_path)    
    plt.close(fig)

def prepare_folders(*files):
    for file in files:makedirs(file,exist_ok=True)           


prepare_folders(INPUT_IMAGES_PATH,OUTPUT_IMAGES_PATH,VARI_IMAGES_GRAY,VARI_IMAGES_COLOR,GLI_IMAGES_GRAY,GLI_IMAGES_COLOR,VI_IMAGES_GRAY,VI_IMAGES_COLOR)    
np.seterr(divide='ignore', invalid='ignore') 
for img in listdir(INPUT_IMAGES_PATH):
    img_path=Path(f"{INPUT_IMAGES_PATH}/{img}")
    if img_path.suffix in IMG_EXTENSIONS:
        for index in ["VARI","GLI","VI"]:
            create_images(img_path,"gray",index)  
            create_images(img_path,"RdYlGn",index)     
print("Done.\nYou can find the images in the output folder!")
        

        
         







   
