import os
import platform
import shutil
import fire
import re
from PIL import Image
from datetime import datetime
from typing import List, Optional
from pyfiglet import Figlet
try:
    from win32com.propsys import propsys, pscon
except:
    pass


def main(path: Optional[str] = None) -> None:
    __print_logo('files organizer')
    fire.Fire(__organize)


def __print_logo(text_logo: str) -> None:
    figlet = Figlet(font='slant')
    print(figlet.renderText(text_logo))


def __organize(path: Optional[str] = None, no_backup: Optional[bool] = False) -> None:
    if path is None:
        path = os.getcwd()

    try:
        print('Reading files, please wait. (Lendo arquivos, aguarde)')
        files_path_list = __get_files_path(path)
        __exit_if_no_files(files_path_list)
        filenames = __get_filenames_without_extension(files_path_list)

        if not no_backup:
            print('Creating backup, please wait. (Criando backup, aguarde)')
            old_folder_name = __create_folder(path, 'Organizer Backup')
            __copy_files_to_backup_folder(
                path, files_path_list, old_folder_name)

        print('Organizing files, please wait. (Organizando arquivos, aguarde)')
        __organize_by_date(path, files_path_list, filenames)
        print('\nSuccessful! (Sucesso!)\n')
    except Exception as e:
        print(f'Error: {str(e)}')


def __get_files_path(path: str) -> List[str]:
    files_path_list = list()
    # TODO: ask for file types
    for file in os.listdir(path):
        # if file.endswith(".url") or file.endswith(".URL"):
        #    files_path_list.append(os.path.join(path, file))
        if not os.path.isdir(os.path.join(path, file)):
            files_path_list.append(os.path.join(path, file))
    return files_path_list


def __exit_if_no_files(files_path_list: List[str]) -> None:
    if len(files_path_list) <= 0:
        print('No files to organize!')
        exit()


def __get_filenames_without_extension(files_path_list: List[str]) -> List[str]:
    filenames = list()
    for path in files_path_list:
        filenames.append(os.path.splitext(os.path.basename(path))[0])
    return filenames


def __create_folder(path: str, folder_name: str) -> str:
    if path is None:
        path = os.getcwd()

    if not os.path.isdir(os.path.join(path, folder_name)):
        os.mkdir(os.path.join(path, folder_name))
    return folder_name


def __copy_files_to_backup_folder(
        path: str,
        files_path_list: List[str],
        backup_folder_name: str
) -> None:
    for file_path in files_path_list:
        shutil.copy(file_path, os.path.join(path, backup_folder_name))


def get_date_taken_from_image(path: str) -> str:
    try:
        im = Image.open(path)
        exif = im.getexif()
        return str(datetime.strptime(exif.get(36867), '%Y:%m:%d %H:%M:%S').strftime('%Y-%m'))
    except:
        return None


def get_date_taken_from_video(path: str) -> str:
    try:
        properties = propsys.SHGetPropertyStoreFromParsingName(path)
        dt = properties.GetValue(pscon.PKEY_Media_DateEncoded).GetValue()

        if not isinstance(dt, datetime):
            return str(datetime.fromtimestamp(int(dt)).strftime('%Y-%m'))
        else:
            return str(datetime.strptime(str(dt).strip('+00:00'), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m'))
    except:
        return None


def get_date_from_filename(filename: str) -> str:
    def is_date_valid(year, month, day):
        try:
            year = int(year)
            month = int(month)
            day = int(day)
            if year <= 1900 or year >= (datetime.now().year + 100):
                return False
            if month <= 0 or month > 12:
                return False
            if day <= 0 or day > 31:
                return False
            return True
        except:
            return False

    # REGEX yyyy-mm-dd ([0-9]{4})[-]([0-9]{2})[-]([0-9]{2})
    matches = re.findall("([0-9]{4})[-]([0-9]{2})[-]([0-9]{2})", filename)
    try:
        if is_date_valid(matches[0][0], matches[0][1], matches[0][2]):
            return f'{matches[0][0]}-{matches[0][1]}'
    except IndexError:
        pass

    # REGEX yyyy_mm_dd ([0-9]{4})[_]([0-9]{2})[_]([0-9]{2})
    matches = re.findall("([0-9]{4})[_]([0-9]{2})[_]([0-9]{2})", filename)
    try:
        if is_date_valid(matches[0][0], matches[0][1], matches[0][2]):
            return f'{matches[0][0]}-{matches[0][1]}'
    except IndexError:
        pass

    # REGEX dd-mm-yyyy ([0-9]{2})[_]([0-9]{2})[_]([0-9]{4})
    matches = re.findall("([0-9]{2})[_]([0-9]{2})[_]([0-9]{4})", filename)
    try:
        if is_date_valid(matches[0][2], matches[0][1], matches[0][0]):
            return f'{matches[0][2]}-{matches[0][1]}'
    except IndexError:
        pass

    # REGEX dd_mm_yyyy ([0-9]{2})[_]([0-9]{2})[_]([0-9]{4})
    matches = re.findall("([0-9]{2})[_]([0-9]{2})[_]([0-9]{4})", filename)
    try:
        if is_date_valid(matches[0][2], matches[0][1], matches[0][0]):
            return f'{matches[0][2]}-{matches[0][1]}'
    except IndexError:
        pass

    # REGEX yyyymmdd (?:\D)(\d{4})(\d{2})(\d{2})(?:\D)
    matches = re.findall("([0-9]{4})([0-9]{2})([0-9]{2})", filename)
    try:
        if is_date_valid(matches[0][0], matches[0][1], matches[0][2]):
            return f'{matches[0][0]}-{matches[0][1]}'
    except IndexError:
        pass

    # REGEX ddmmyyyy (?:\D)(\d{2})(\d{2})(\d{4})(?:\D)
    matches = re.findall("([0-9]{2})([0-9]{2})([0-9]{4})", filename)
    try:
        if is_date_valid(matches[0][2], matches[0][1], matches[0][1]):
            return f'{matches[0][2]}-{matches[0][1]}'
    except IndexError:
        pass

    return False


def get_creation_date(path: str) -> str:
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    try:
        if platform.system() == 'Windows':
            return str(datetime.fromtimestamp(int(os.path.getctime(path))).strftime('%Y-%m'))
        else:
            stat = os.stat(path)
            try:
                # Mac
                return str(datetime.fromtimestamp(int(stat.st_birthtime)).strftime('%Y-%m'))
            except AttributeError:
                # We're probably on Linux. No easy way to get creation dates here,
                # so we'll settle for when its content was last modified.
                return str(datetime.fromtimestamp(int(stat.st_mtime)).strftime('%Y-%m'))
    except:
        return None


def __organize_by_date(path: str, files_path_list: List[str], filenames: List[str]) -> None:
    for file_path, filename in zip(files_path_list, filenames):
        try:
            folder_name = get_date_taken_from_image(file_path)
            if not folder_name:
                folder_name = get_date_taken_from_video(file_path)
            if not folder_name:
                folder_name = get_date_from_filename(filename)
            if not folder_name:
                folder_name = get_creation_date(file_path)
            if not folder_name:
                folder_name = 'No Date'

            __create_folder(path, folder_name)
            shutil.move(file_path, os.path.join(path, folder_name))

        except Exception as e:
            print(e)
