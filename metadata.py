import yt_dlp

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

from logger import Logger
from description import save_description_parsed_urls

ydl_metadata_opts = {
    'ignoreerrors': 'only_download',
    'quiet': True,
    'logger': Logger()
}


def get_videos_metadata(urls):
    ydl = yt_dlp.YoutubeDL(ydl_metadata_opts)
    res = []
    urls = [urls] if type(urls) is not list else urls

    for url in urls:
        info = ydl.extract_info(url, download=False)

        if info is not None:
            res += [
                {
                    "videoID": url.strip(),
                    "metaData": info
                }
            ]

    return res


def get_videos_metadata_parallel(urls):
    pool = ThreadPoolExecutor()
    futures = [pool.submit(get_videos_metadata, url) for url in urls]
    res = []

    for future in as_completed(futures):
        res += future.result()

    return res


def update_video_durations_and_compute_descriptions(df, desc_path, filter=lambda x: True):
    urls = set(df['videoID'])
    metadata = get_videos_metadata_parallel(urls)

    for m in metadata:
        duration = m['metaData']['duration']
        description = m['metaData']['description']

        if filter(m):
            df.loc[df['videoID'] == m['videoID'], 'videoDuration'] = duration
            save_description_parsed_urls(
                description, f"{desc_path}/{m['videoID']}/{m['videoID'].urls.json}")
        else:
            df.drop(df.loc[df['videoID'] == m['videoID']])