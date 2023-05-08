
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import as_completed

import numpy as np
import pandas as pd
import time
from tqdm import tqdm 
import yt_dlp

from logger import Logger
import description
import paths

ydl_opts = {
    'outtmpl': f'{paths.DL_DIR}/%(id)s/%(id)s.mp4',
    'format': 'worstvideo[ext=mp4][height>=480]+worstaudio[ext=m4a]',
    'ignoreerrors': 'only_download',
    'quiet': True,
    'logger': Logger(),
    'no_color': True,
    'no_progress': True,
    'socket_timeout': 20,
}

def dl_videos_length_filter(info_dict, *, incomplete):
    duration = info_dict.get("duration")

    if duration and duration > 20 * 60:
        "La video est trop longue"

def dl_videos(urls):
    t_start = time.time()

    with yt_dlp.YoutubeDL({**ydl_opts, **{'match_filter': dl_videos_length_filter}}) as ydl:
        info = ydl.extract_info(urls, download=True)
        desc = info.get("description") if info else None

        if desc:
            description.save_description_parsed_urls(desc, f"{paths.DL_DIR}/{info['id']}/{info['id']}.desc.json")
    
    t_end = time.time()

    return urls, t_end - t_start

def dl_videos_parallel(urls):
    tasks_completed = 0
    tasks_total = len(urls)

    with tqdm(total=tasks_total) as pbar:
        with ProcessPoolExecutor(5) as pool:
            futures = [pool.submit(dl_videos, url) for url in urls]

            for res in as_completed(futures):
                res.result()
                pbar.update(1)

    return tasks_completed
