from ImagePipeline import process_image
from moviepy.editor import VideoFileClip


# select a video to work with
clip1 = VideoFileClip("test_videos/solidWhiteRight.mp4")
# clip1 = VideoFileClip("test_videos/solidYellowLeft.mp4")
# clip1 = VideoFileClip("test_videos/challenge.mp4")
process_clip = clip1.fl_image(process_image) #NOTE: this function expects color images!!

output = 'test_videos_output/solidWhiteRight.mp4'
# output = 'test_videos_output/solidYellowLeft.mp4'
# output = 'test_videos_output/challenge.mp4'
process_clip.write_videofile(output, audio=False)
