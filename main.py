import yt_dlp
import sys


def get_info(url):
    options = {
        'simulate': True,
        'quiet': True
    }

    ydl = yt_dlp.YoutubeDL(options)

    try:
        video_info = ydl.extract_info(url=url)
        # video_json_info = json.dumps(video_info)

        formats = video_info.get("formats", None)
        v_formats = {}
        a_formats = {}
        v_count = 1

        for video_format in formats:
            if video_format['protocol'] == 'https' and video_format['resolution'] != 'audio only':
                v_formats[v_count] = video_format
                v_count += 1

        for audio_format in formats:
            if audio_format['ext'] == 'm4a' or audio_format['ext'] == 'webm':
                a_formats[audio_format['ext']] = audio_format

        video_data = {
            'title': video_info.get('title', None),
            'thumbnail': video_info.get('thumbnail', None),
            'v_formats': v_formats,
            'a_formats': a_formats
        }

        return video_data
    except Exception as ex:
        print(f"[!] {ex}")
        raise "Please check the URL!"


def download_video(url, video, title, audio=''):
    if audio:
        options = {
            'format': f'{video["format_id"]}+{audio["format_id"]}',
            'outtmpl': f'data/{title}'
        }
    else:
        options = {
            'format': f'{video["format_id"]}',
            'outtmpl': f'data/{title}'
        }

    try:
        ydl = yt_dlp.YoutubeDL(options)
        ydl.extract_info(url=url)

        return "[INFO] Video Downloaded! Enjoy :)"
    except Exception as ex:
        raise ex


def main():
    url = input('Enter URL address: ')
    url = url.strip()
    video_data = get_info(url=url)
    title = video_data['title']
    available_video_formats = video_data['v_formats']
    available_audio_formats = video_data['a_formats']

    print(f"[INFO] {title}\n{'-' * 50}")
    print("Select the desired video format:")

    for k, v in available_video_formats.items():
        print(f"{k} - {v['format_id']}({v['resolution']})|{v['ext']}")

    v_format = int(input("Enter a number, for example 2: "))

    if v_format not in available_video_formats:
        print("This format is not available, check the data!")
        sys.exit()

    if available_audio_formats:
        print("Select the desired audio format:")
        for k, v in available_audio_formats.items():
            print(f"{k} - {v['format_id']}({v['resolution']})")

        a_format = input("Enter a number, for example m4a: ")

        if a_format not in available_audio_formats:
            print("This format is not available, check the data!")
            sys.exit()
        print(download_video(url, video=available_video_formats[v_format], audio=available_audio_formats[a_format], title=title))
    print(download_video(url, video=available_video_formats[v_format], title=title))


if __name__ == '__main__':
    main()
