import cv2, os, shutil, sys, imgkit
from PIL import Image, ImageOps

def vid_to_img(video_path, vid_name, generation):
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count/fps
    minutes = int(duration/60)
    seconds = duration%60

    print('FPS = ' + str(fps))
    print('Total frames = ' + str(frame_count))
    print('Duration (S) = ' + str(duration))
    print('duration (M:S) = ' + str(minutes) + ':' + str(seconds))

    success, image = video.read()
    counter = 1

    if generation:
        os.mkdir(vid_name+'_Images')
        while success:
            cv2.imwrite(vid_name+"_Images/Image{0}.png".format(str(counter)), image)
            success, image = video.read()
            print(f"Frame number: {counter}/{frame_count}")
            counter+=1

    if not generation:
        file_count = len(next(os.walk(vid_name+"_Images"))[2])
        counter += file_count

    return fps, (counter-1)

def get_image_info(image_path):
    initial_image = Image.open(image_path)     
    width,height = initial_image.size                     
    initial_image = initial_image.resize((round(width*1.05),height)) 
    return initial_image        

def correctSize(image, final_width = 200):
    width, height = image.size                     
    final_height = int((height*final_width)/width)    
    image = image.resize((final_width,final_height)) 
    return image

def grayscale_image(image):
    image_bw = ImageOps.grayscale(image) 
    return image_bw

def ascii_conversion(bw_image,ascii_string = [" ",".",":","-","=","+","`","'","*","#","%","@","&"]): 
    pixels = bw_image.getdata()           
    ascii_image_list = []             
    for pixel in pixels:               
        ascii_converted = int((pixel*len(ascii_string))/256) 
        ascii_image_list.append(ascii_string[ascii_converted]) 
    return ascii_image_list 

def get_color(image):                
    pixels = image.getdata()
    return pixels

def rgb_ascii(ascii_list, image, color,image_pos,vid_name):
    file = open(vid_name+'_HtmlImages/Html{0}.html'.format(str(image_pos)),"w") 
    file.write("""                                                                                              
            <!DOCTYPE html>
            <html>
            <body style='background-color:black'>
            <pre style='display: inline-block; border-width: 4px 6px; border-color: black; border-style: solid; background-color:black; font-size: 32px ;font-face: Montserrat;font-weight: bold;line-height:60%'>""") 

    width, height = image.size
    counter = 0                       
    for j in ascii_list:
        color_hex = '%02x%02x%02x' % color[counter] 
        counter+=1
        if (counter % width) != 0:                 
            file.write("<span style=\"color: #{0}\">{1}</span>".format(color_hex,j))    
        else:
            file.write("<br />") 
    file.write("""</pre></body>
        </html>""")                
    file.close() 

def bw_ascii(ascii_list, image, image_pos,vid_name):
    file = open(vid_name+'_bwHtmlImages/bwHtml{0}.html'.format(str(image_pos)),"w") 
    file.write("""                                                                                              
            <!DOCTYPE html>
            <html>
            <body style='background-color:black'>
            <pre style='display: inline-block; border-width: 4px 6px; border-color: black; border-style: solid; background-color:black; font-size: 32px ;font-face: Montserrat;font-weight: bold;line-height:60%'>""") 

    width, height = image.size
    counter = 0                       
    for j in ascii_list:
        counter+=1
        if (counter % width) != 0:                 
            file.write("<span style= color:#ffffff>{0}</span>".format(j))    
        else:
            file.write("<br />") 
    file.write("""</pre></body>
        </html>""")                
    file.close() 

def export_video(vid_name, fps, number_images):
    print("Generating RGB ASCII video...")
    res = Image.open(vid_name+'_TextImages/Image1.png').size 
    video = cv2.VideoWriter(vid_name+'_rgb_ascii.mp4',cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),int(fps),res)
    for j in range(1,number_images+1):                 
        print("Writing frames... [{0}/{1}]".format(j,number_images+1))              
        video.write(cv2.imread(vid_name+'_TextImages/Image{0}.png'.format(str(j)))) 
    video.release()
    print("RGB ASCII Video Exported...")

    print("Generating BW ASCII video...")
    res = Image.open(vid_name+'_bwTextImages/bwImage1.png').size 
    video = cv2.VideoWriter(vid_name+'_bw_ascii.mp4',cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),int(fps),res)
    for j in range(1,number_images+1):                 
        print("Writing frames... [{0}/{1}]".format(j,number_images+1))              
        video.write(cv2.imread(vid_name+'_bwTextImages/bwImage{0}.png'.format(str(j)))) 
    video.release()
    print("BW ASCII Video Exported...")

def main(video_path):
    config = imgkit.config(wkhtmltoimage=r'wkhtmltoimage.exe')     

    video_path=str(video_path)
    vid_name=video_path.split(sep="/")
    vid_name=str(vid_name[len(vid_name)-1])
    vid_name=vid_name.removesuffix(".mp4")

    generate_img = True
    img_exist = os.path.isdir(vid_name+"_Images/") 

    if img_exist:
        func=input("Use cached PNG? [y/n]: ")
        if func == "y":
            generate_img=False
        elif func == "n":
            shutil.rmtree(vid_name+"_Images", ignore_errors=True)
            generate_img=True                     
            img_exist=True

    fps,number_images = vid_to_img(video_path,vid_name,generate_img)

    for i in range(1,number_images+1):
        print("Rendering... [{0}/{1}]".format(i,number_images+1))              
        image = get_image_info(vid_name+'_Images/Image{0}.png'.format(str(i)))
        correctedImage = correctSize(image)
        bw_image = grayscale_image(correctedImage)             
        converted_list = ascii_conversion(bw_image) 
        color_list = get_color(correctedImage)
        bw_ascii(converted_list, correctedImage,i,vid_name)
        rgb_ascii(converted_list, correctedImage,color_list,i,vid_name)
        imgkit.from_file(vid_name+'_bwHtmlImages/bwHtml{0}.html'.format(str(i)), vid_name+'_bwTextImages/bwImage{0}.png'.format(str(i)), config = config) 
        imgkit.from_file(vid_name+'_HtmlImages/Html{0}.html'.format(str(i)), vid_name+'_TextImages/Image{0}.png'.format(str(i)), config = config) 
    
    print("Rendering complete!")

    export_video(vid_name, fps, number_images)

if len(sys.argv) != 2:
    print("Usage: ./converter.py <video_path>")
    sys.exit()

video_path = str(sys.argv[1])

if __name__ == '__main__':
    main(video_path)