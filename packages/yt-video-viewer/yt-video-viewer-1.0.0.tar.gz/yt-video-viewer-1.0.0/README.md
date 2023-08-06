Yt-Video-Viewer is a python library which watch the video till the length(time) provided using browser automation. 
It currently runs only on windows.

### Example
In this example we first import library, then we watched video using simple function.
```sh
from yt_video_viewer import *
youtube.watch_video(time='160', video_url='https://www.youtube.com/watch?v=LMmuChXra_M') #provide time in seconds
```

This module depends on the following python modules
* [requests](https://pypi.org/project/requests/)
* [btstudio](https://pypi.org/project/btstudio/)

#### BtStudio
[btstudio](https://pypi.org/project/btstudio/) is needed for browser automation. As soon as this library is imported in code, automated browser will open up in which video will be opened.

Complete documentation for YouTube Automation available [here](https://youtube-api.datakund.com/en/latest/)

### Installation

```sh
pip install yt-video-viewer
```

### Import
```sh
from yt_video_viewer import *
```

### Watch video
```sh
response=youtube.watch_video(time='160', video_url='video link')
```

### Send Feedback to Developers
```sh
btstudio.send_feedback(feedback="Need help with this ......")
```

### Contact Us
* [Telegram](https://t.me/datakund)
* [Website](https://datakund.com)

