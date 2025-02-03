import time
import config
import classes
from re import match
import os
import csv
from winotify import Notification, audio


def unpack_file_name(raw_file):
    split_result = [i.strip() for i in raw_file.stem.split('-')]
    for part in split_result:
        if any(ch in config_copy.specials_chars for ch in part):
            show_fail_notification(f'"{part}" contains special characters', raw_file.parent)
            raise ValueError('Special characters can not be part of the file name ')
    if len(split_result) == 2:
        unpacked_file_reference, unpacked_document_name = split_result
        unpacked_file_comment = None
    elif len(split_result) == 3:
        unpacked_file_reference, unpacked_document_name, unpacked_file_comment = split_result
        if len(unpacked_file_comment) == 0:
            unpacked_file_comment = None
    else:
        show_fail_notification('Invalid file format', raw_file.parent)
        raise ValueError('Invalid file name format')
    return unpacked_file_reference.upper(), unpacked_document_name.upper(), unpacked_file_comment


def review_reference(file_reference: str, file_path):
    if match(pattern=config_copy.patterns[0], string=file_reference):
        return classes_copy.Oid(file_reference)
    elif match(pattern=config_copy.patterns[1], string=file_reference):
        return classes_copy.RightAngleNumber(file_reference)
    elif match(pattern=config_copy.patterns[2], string=file_reference):
        return classes_copy.InMovement(file_reference)
    elif match(pattern=config_copy.patterns[3], string=file_reference):
        return classes_copy.TNumber(file_reference)
    else:
        show_fail_notification(f'Invalid reference -  "{file_reference}"', file_path)
        raise ValueError(f'{file_reference} - Does not match any pattern')


def review_document_name(doc_name: str, file_path):
    name_breakdown = [i.strip() for i in doc_name.split('+')]
    if any(name not in config_copy.naming_convention for name in name_breakdown):
        show_fail_notification(f'Invalid doc name - "{doc_name}"', file_path)
        raise ValueError('Invalid document name format.')
    else:
        doc_name = '+'.join(name_breakdown)
        reviewed_document = classes_copy.Document(doc_name, file_path)
        return reviewed_document


def merge_csv_files(config):
    info = []
    for product_type in config.products:
        path = os.path.join(config.CSV_FILE_PATH, product_type, 'PlannedTransfer.csv')
        with open(path, 'r') as file:
            csv_file = csv.reader(file, delimiter=',')
            for i in csv_file:
                info.append(i)
    return info




def move_file(raw_file, new_name: str, ra_number: str, dst_path: str):
    try:
        os.rename(raw_file, new_name)
        show_notification_success(ra_number, dst_path)
    except FileNotFoundError:
        show_fail_notification(f'Folder does not exist - "{ra_number}"', raw_file.parent)
        exit()
    except PermissionError:
        show_fail_notification('Document is in use', raw_file.parent)
        exit()
    except FileExistsError:
        file_handler = classes_copy.FileHandler(raw_file, new_name,ra_number)
        file_handler.exec_()
        show_notification_success(ra_number, dst_path)


def file_document(raw_file, path_object, reference,dst):
    folder_found = False
    for folder in path_object.iterdir():
        if folder.name == reference:
            folder_found = True
            dst_path = f'{dst}\\{folder.name}\\{raw_file.name}'
            dst_folder = f'{dst}\\{folder.name}'
            move_file(raw_file, dst_path, reference, dst_folder)
    if not folder_found:
        show_fail_notification(f'"{reference}" was not found', raw_file)


def show_notification_success(folder_name, dst_path):
    success_toaster = Notification(app_id=config_copy.toaster_app_id, title='Operation Successful',
                                   msg=f'Final Destination - {folder_name}',
                                   duration='short',
                                   icon=config_copy.successful_icon_path)
    success_toaster.add_actions(label='Open Folder', launch=dst_path)
    success_toaster.set_audio(audio.Default, loop=False)
    success_toaster.show()


def show_fail_notification(msg: str, file_path: str):
    fail_toaster = Notification(app_id=config_copy.toaster_app_id, title='Operation Failed',
                                msg=msg,
                                duration='short',
                                icon=config_copy.failed_icon_path)
    fail_toaster.add_actions(label='Open File', launch=file_path)
    fail_toaster.set_audio(audio.IM, loop=False)
    fail_toaster.show()


def sleep():
    time.sleep(3)


def construct_new_name(dst_path, ra_reference, document_name, raw_file_suffix, comment=None):
    if comment is not None:
        return f'{dst_path}\\{ra_reference}-{document_name}-{comment}{raw_file_suffix}'
    else:
        return f'{dst_path}\\{ra_reference}-{document_name}{raw_file_suffix}'




