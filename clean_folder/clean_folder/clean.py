from pathlib import Path
import shutil
import sys
import re

"""Скрипт виконує сортування в заданній директорії, нормалізовує назви файлів та вкладених диреторій
Після закінчення роботи створюється текстовий файл data.txt, в якому міститься перелік файлівб
перелік відомих та невідомих розширень. Директорії оброблюються рекурсивно. """
names_dir = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
    "Documents": [
        ".txt",
        ".docx",
        ".doc",
        ".pdf",
        ".rtf",
        ".xls",
        ".xlsx",
        ".ppt",
        ".pptx",
    ],
    "Archives": [".tar", ".gz", ".7z", ".zip"],
    "Audio": [".mp3", "ogg", ".wav", ".amr"],
    "Video": [".avi", ".mov", ".mp4", ".mkv"],
    "Python": [".py", ".pyw"],
}

CYRILLIC = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
LATIN = (
    "a",
    "b",
    "v",
    "g",
    "d",
    "e",
    "e",
    "j",
    "z",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "r",
    "s",
    "t",
    "u",
    "f",
    "h",
    "ts",
    "ch",
    "sh",
    "sch",
    "",
    "y",
    "",
    "e",
    "yu",
    "ya",
    "je",
    "i",
    "ji",
    "g",
)
FOLDERS = []
translate_map = {}
for key, value in zip(CYRILLIC, LATIN):
    translate_map[ord(key)] = value
    translate_map[ord(key.upper())] = value.upper()

list_files = []
ext = set()
unknow = set()


def main():
    try:
        folder_for_scan = Path(sys.argv[1])  # r"C:\Users\hp\Desktop\sort"
    except IndexError as Err:
        sys.exit("Директорію для сортування не знайдено. Виконайте перезапуск")

    print(f"Початок сортування директорії {folder_for_scan.resolve()}")
    scan(folder_for_scan)
    print("Сортування закінчено!\n")
    data_output(list_files, ext, unknow)


def normalise(file_stem: str) -> str:
    new_name = file_stem.translate(translate_map)
    new_name = re.sub(r"\W", "_", new_name)
    return new_name


def handle_imgs(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / (normalise(filename.stem) + filename.suffix))
    list_files.append((normalise(filename.stem) + filename.suffix))
    ext.add(filename.suffix)


def handle_docs(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / (normalise(filename.stem) + filename.suffix))
    list_files.append((normalise(filename.stem) + filename.suffix))
    ext.add(filename.suffix)


def handle_audio(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / (normalise(filename.stem) + filename.suffix))
    list_files.append((normalise(filename.stem) + filename.suffix))
    ext.add(filename.suffix)


def handle_video(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / (normalise(filename.stem) + filename.suffix))
    list_files.append((normalise(filename.stem) + filename.suffix))
    ext.add(filename.suffix)


def handle_py(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / (normalise(filename.stem) + filename.suffix))
    list_files.append((normalise(filename.stem) + filename.suffix))
    ext.add(filename.suffix)


def handle_other(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / (normalise(filename.stem) + filename.suffix))
    list_files.append((normalise(filename.stem) + filename.suffix))
    unknow.add(filename.suffix)


def handle_archive(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalise(
        filename.name.replace(filename.suffix, "")
    )

    folder_for_file.mkdir(exist_ok=True, parents=True)
    shutil.unpack_archive(str(filename.resolve()), str(folder_for_file.resolve()))
    list_files.append((normalise(filename.stem) + filename.suffix))
    filename.unlink()


def handle_folder(folder: Path):
    try:
        folder.rmdir()
        print(f"Знайдено порожню директорію, яку буде видалено {folder}")
        return False
    except OSError:
        return True


def data_output(
    list_files: list,
    ext: set,
    unknow: set,
):
    print(f"ПЕРЕЛІК ФАЙЛІВ:")
    for i in list_files:
        print(i)

    print(f"\n ПЕРЕЛІК ВІДОМИХ РОШИРЕНЬ:")
    for i in ext:
        print(i)

    print(f"\n ПЕРЕЛІК НЕВІДОМИХ РОШИРЕНЬ:")
    for i in unknow:
        print(i)


def scan(folder: Path):
    for file in folder.iterdir():
        if file.is_file():
            suf = file.suffix
            if suf in names_dir["Images"]:
                handle_imgs(file, folder / "Images")
            elif suf in names_dir["Documents"]:
                handle_docs(file, folder / "Documents")
            elif suf in names_dir["Audio"]:
                handle_audio(file, folder / "Audio")
            elif suf in names_dir["Video"]:
                handle_video(file, folder / "Video")
            elif suf in names_dir["Python"]:
                handle_py(file, folder / "Python")
            elif suf in names_dir["Archives"]:
                handle_archive(file, folder / "Archives")
            else:
                handle_other(file, folder / "Other")
        elif file.name not in (
            "Images",
            "Documents",
            "Audio",
            "Video",
            "Python",
            "Archives",
            "Other",
        ):
            if handle_folder(file):
                scan(file)
                file.replace(folder / normalise(file.name))


if __name__ == "__main__":
    main()

# TODO: запускаємо:  python3 sort.py `назва_папки_для_сортування`
