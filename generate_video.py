# 6Q1qxLZbq7nni2wt
import ffmpeg_streaming
from ffmpeg_streaming import Formats, Bitrate, Representation, Size
import sys
import datetime

def monitor(ffmpeg, duration, time_, time_left, process):
    """
    """
    per = round(time_ / duration * 100)
    sys.stdout.write(
        "\rTranscoding...(%s%%) %s left [%s%s]" %
        (per, datetime.timedelta(seconds=int(time_left)), '#' * per, '-' * (100 - per))
    )
    sys.stdout.flush()

video = ffmpeg_streaming.input('2.mp4')
print(video)
dash = video.dash(Formats.h264())
_144p  = Representation(Size(256, 144), Bitrate(95 * 1024, 64 * 1024))
_240p  = Representation(Size(426, 240), Bitrate(150 * 1024, 94 * 1024))
dash.auto_generate_representations()
print(dash)
dash.output('a.a.mpd', run_command="-vsync 1", monitor=monitor)