import sys
from pathlib import Path

jpeg_files = list()
png_files = list()
jpg_files = list()
svg_files = list()
txt_files = list()
docx_files = list()
doc_files = list()
pdf_files = list()
xlsx_files = list()
pptx_files = list()
mp3_files = list()
ogg_files = list()
wav_files = list()
amr_files = list()
avi_files = list()
mp4_files = list()
mov_files = list()
mkv_files = list()
zip_files = list()
gz_files = list()
tar_files = list()
folders = list()
archives = list()
others = list()
unknown = set()
extensions = set()

registered_extensions = {
    'JPEG': jpeg_files,
    'PNG': png_files,
    'JPG': jpg_files,
    'SVG': svg_files,
    'DOC': doc_files,
    'TXT': txt_files,
    'DOCX': docx_files,
    'PDF': pdf_files,
    'XLSX': xlsx_files,
    'PPTX': pptx_files,
    'MP3': mp3_files,
    'OGG': ogg_files,
    'WAV': wav_files,
    'AMR': amr_files,
    'AVI': avi_files,
    'MP4': mp4_files,
    'MOV': mov_files,
    'MKV': mkv_files,
    'ZIP': zip_files,
    'GZ': gz_files,
    'TAR': tar_files
}

def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()

def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('JPEG', 'PNG', 'JPG', 'SVG', 'TXT', 'DOCX', 'DOC', 'PDF', 'XLSX', 'PPTX', 'MP3', 'OGG', 'WAV', 'AMR', 'AVI', 'MP4', 'MOV', 'MKV', 'ZIP', 'GZ', 'TAR', 'OTHER'):
                folders.append(item)
                scan(item)
            continue

        extension = get_extensions(file_name=item.name)
        new_name = folder/item.name
        if not extension:
            others.append(new_name)
        else:
            try:
                container = registered_extensions[extension]
                extensions.add(extension)
                container.append(new_name)
            except KeyError:
                unknown.add(extension)
                others.append(new_name)

if __name__ == '__main__':
    path = sys.argv[1]
    #print(f"Start in {path}")

    folder = Path(path)

    scan(folder)


