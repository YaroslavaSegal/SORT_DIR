import sys
import shutil
from pathlib import Path

import scan
import normalize

def handle_file(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder / normalize.normalize(path.name))

def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    if path.name.endswith('.zip'):
        new_name = normalize.normalize(path.name).replace(".zip", '')
    elif path.name.endswith('.gz'):
        new_name = normalize.normalize(path.name).replace(".gz", '')
    elif path.name.endswith('.tar'):
        new_name = normalize.normalize(path.name).replace(".tar", '')

    archive_folder = target_folder / new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(path, archive_folder)
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    except FileNotFoundError:
        archive_folder.rmdir()
        return
    path.unlink()


def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass


def main(folder_path):
    # print(folder_path)
    scan.scan(folder_path)
    images_files = scan.jpeg_files + scan.jpg_files + scan.png_files + scan.svg_files
    documents_files = scan.txt_files + scan.doc_files + scan.docx_files + scan.pdf_files + scan.xlsx_files + scan.pptx_files
    audio_files = scan.mp3_files + scan.ogg_files + scan.wav_files + scan.amr_files
    video_files = scan.avi_files + scan.mp4_files + scan.mov_files + scan.mkv_files
    archive_files = scan.zip_files + scan.gz_files + scan.tar_files
    known_extension = images_files + documents_files + audio_files + video_files + archive_files
    dict_files = {"images": images_files, "documents": documents_files, 'audio': audio_files, 'video': video_files, 'other': scan.others}
    for key, value in dict_files.items():
        for file in value:
            handle_file(file, folder_path, key)
    for file in archive_files:
        handle_archive(file, folder_path, 'archives')
    remove_empty_folders(folder_path)


if __name__ == '__main__':
    path = sys.argv[1]
    print(f'Start in {path}')

    folder = Path(path)

    main(folder.resolve())
    for item in folder.iterdir():
        print(item.name, end=' ')
        for file in item.iterdir():
            print(file.name, end=" ")
        print("")

    print(f"All extensions: {scan.extensions}")
    print(f"Unknown extensions: {scan.unknown}")