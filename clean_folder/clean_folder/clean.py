import sys
from pathlib import Path
import random
import re
import patoolib
# Словник з категоріями файлів та їх розширеннями
CATEGORIES = {
    "Audio": [".mp3", ".aiff", ".wav", ".aac", ".flac"],
    "Documents": [".docx", ".doc", ".txt", ".pdf", ".xls", ".xlsx", ".pptx", ".rtf"],
    "Video": [".avi", ".mp4", ".mov", ".mkv", ".mpeg"],
    "Image": [".jpeg", ".png", ".pcd", ".jpg", ".svg", ".tiff", ".raw", ".gif", ".bmp"],
    "Archive": [".zip", ".7-zip", ".7zip", ".rar", ".gz", ".tar"],
    "Book": [".fb2", ".mobi"]
}
# Функція для нормалізації імені файлу
def normalize(name):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                   "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    TRANS = {}
    for c, t in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = t
        TRANS[ord(c.upper())] = t.upper()
    name = name.translate(TRANS)
    name = re.sub(r"[^a-zA-Z0-9.]", "_", name) 
    return name
# Функція для переміщення файлу у відповідну категорію
def move_file(file: Path, root_dir: Path, category: str) -> None:
    target_dir = root_dir.joinpath(category)
    if not target_dir.exists():
        target_dir.mkdir()
    new_name = target_dir.joinpath(normalize(file.stem) + file.suffix)
    if new_name.exists():
        new_name = new_name.with_name(
            f"{new_name.stem}-{random.randint(0, 100)}{file.suffix}")
    file.rename(new_name) 
# Функція для визначення категорії файлу за його розширенням
def get_category(file: Path) -> str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"    
# Функція для сортування файлів у кореневій папці
def sort_folder(path: Path) -> None:
    for item in path.glob("**/*"):
        if item.is_file():
            category = get_category(item)
            move_file(item, path, category)    
# Функція для видалення порожніх папок
def delete_empty_folders(path: Path) -> None:
    for folder in list(path.glob("**/*"))[::-1]:
        if folder.is_dir() and not any(folder.iterdir()):
            is_category_folder = any(cat in CATEGORIES.keys() for cat in folder.name)
            if not is_category_folder:
                folder.rmdir()
# Функція для розпакування архівів
def unpack_archives(path: Path) -> None:
    archive_folder = path.joinpath("Archive")
    for file_name in archive_folder.glob("*"):
        if file_name.is_file():
            extract_folder = file_name.stem
            extract_path = archive_folder.joinpath(extract_folder)
            extract_path.mkdir(exist_ok=True)
            patoolib.extract_archive(str(file_name), outdir=str(extract_path))    

# Основна функція
def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder"
    
    if not path.exists():
        return f"Folder with path {path} dos`n exists."
    sort_folder(path)
    unpack_archives(path)
    delete_empty_folders(path)
    return "All done"

# Точка входу
if __name__ == "__main__":
    print(main())
    