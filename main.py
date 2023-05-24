import cv2, os

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
