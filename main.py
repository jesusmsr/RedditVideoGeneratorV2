from moviepy.editor import *
import moviepy.editor as mpe

import reddit, screenshot, time, subprocess, random, configparser, sys, math
from os import listdir
from os.path import isfile, join
import os
import glob

SONGS_DIRECTORY = 'Music'

def createVideo():
    config = configparser.ConfigParser()
    config.read('config.ini')
    outputDir = config["General"]["OutputDirectory"]

    startTime = time.time()

    # Get script from reddit
    # If a post id is listed, use that. Otherwise query top posts
    if (len(sys.argv) == 2):
        script = reddit.getContentFromId(outputDir, sys.argv[1])
    else:
        postOptionCount = int(config["Reddit"]["NumberOfPostsToSelectFrom"])
        script = reddit.getContent(outputDir, postOptionCount)
    fileName = script.getFileName()

    # Create screenshots
    screenshot.getPostScreenshots(fileName, script)

    # Setup background clip
    bgDir = config["General"]["BackgroundDirectory"]
    bgPrefix = config["General"]["BackgroundFilePrefix"]
    bgFiles = [f for f in listdir(bgDir) if isfile(join(bgDir, f))]
    bgCount = len(bgFiles)
    bgIndex = random.randint(0, bgCount-1)
    backgroundVideo = VideoFileClip(
        filename=f"{bgDir}/{bgPrefix}{bgIndex}.mp4", 
        audio=False).subclip(0, script.getDuration())
    w, h = backgroundVideo.size

    def __createClip(screenShotFile, audioClip, marginSize):
        imageClip = ImageClip(
            screenShotFile,
            duration=audioClip.duration
            ).set_position(("center", "center"))
        imageClip = imageClip.resize(width=(w-marginSize))
        videoClip = imageClip.set_audio(audioClip)
        videoClip.fps = 1
        return videoClip

    # Create video clips
    print("Editing clips together...")
    clips = []
    marginSize = int(config["Video"]["MarginSize"])
    clips.append(__createClip(script.titleSCFile, script.titleAudioClip, marginSize))
    for comment in script.frames:
        clips.append(__createClip(comment.screenShotFile, comment.audioClip, marginSize))

    # Merge clips into single track
    contentOverlay = concatenate_videoclips(clips).set_position(("center", "center"))
    
    # Pick random background song
    songs = [file for file in os.listdir(SONGS_DIRECTORY) if os.path.isfile(os.path.join(SONGS_DIRECTORY, file))]
    
    random_file = random.choice(songs)
    print(f"Randomly selected song: {random_file}")
    print(random_file)
    background_music = AudioFileClip(f'{SONGS_DIRECTORY}/{random_file}')
    
    # Pick a random part of the song
    max_start_time = background_music.duration - contentOverlay.duration
    start_time = random.uniform(0, max_start_time)
    
    random_clip = background_music.subclip(start_time, start_time + contentOverlay.duration).fx(afx.volumex, 0.1)  
    
    final_audio = CompositeAudioClip([contentOverlay.audio, random_clip])

    # Compose background/foreground
    final = CompositeVideoClip(
        clips=[backgroundVideo, contentOverlay], 
        size=backgroundVideo.size).set_audio(final_audio)
    final.duration = script.getDuration()
    final.set_fps(backgroundVideo.fps)

    # Write output to file
    print("Rendering final video...")
    bitrate = config["Video"]["Bitrate"]
    threads = config["Video"]["Threads"]
    outputFile = f"{outputDir}/{fileName}.mp4"
    final.write_videofile(
        outputFile, 
        codec = 'mpeg4',
        threads = threads, 
        bitrate = bitrate
    )
    print(f"Video completed in {time.time() - startTime}")
    
    temp_files = glob.glob('Voiceovers/temp/*')
    screenshots = glob.glob('Screenshots/*')
    
    for f in screenshots:
        os.remove(f)
    
    for f in temp_files:
        os.remove(f)
    
    print(f"Removed temp files")

    # Finish
    print("Video is ready to upload!")
    print(f"Title: {script.title}  File: {outputFile}")
    endTime = time.time()
    print(f"Total time: {endTime - startTime}")

def rename_files(directory_path, template="ShortTemplate"):
    # Get a list of files in the directory
    files = os.listdir(directory_path)
    for index, filename in enumerate(files):
        # Construct the full file path
        old_file_path = os.path.join(directory_path, filename)
        # Get the file extension (if any)
        _, file_extension = os.path.splitext(filename)
        # Create new file name with the desired template
        new_file_name = f"{template}_{index}{file_extension}"
        new_file_path = os.path.join(directory_path, new_file_name)
        # Rename the file
        os.rename(old_file_path, new_file_path)
        print(f"Renamed '{filename}' to '{new_file_name}'")
        
if __name__ == "__main__":
    
    background_videos_directory_path = 'BackgroundVideos'
    #rename_files(background_videos_directory_path)
    
    createVideo()