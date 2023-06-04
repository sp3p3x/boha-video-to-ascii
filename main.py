import cv2, os, shutil, sys
from PIL import Image

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

def main(video_path):
    video_path=str(video_path)
    vid_name=video_path.split(sep="/")
    vid_name=str(vid_name[len(vid_name)-1])
    vid_name=vid_name.removesuffix(".mp4")

    if img_exist:
        func=input("Use cached PNG? [y/n]: ")
        if func == "y":
            generate_img=False
        elif func == "n":
            shutil.rmtree(vid_name+"_Images", ignore_errors=True)
            generate_img=True                     
            img_exist=True

    fps,number_images = vid_to_img(video_path,vid_name,generate_img)

if len(sys.argv) != 2:
    print("Usage: ./converter.py <video_path>")
    sys.exit()

video_path = str(sys.argv[1])

if __name__ == '__main__':
    main(video_path)