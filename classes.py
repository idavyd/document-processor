import config
import sys
import os
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QMessageBox
from functions import show_fail_notification

app = QApplication(sys.argv)


class Document:
    def __init__(self, name: str, file_path):
        self.name = name
        self.is_truck_related = None
        self.is_marine_and_itt_related = None
        self.is_oid_truck_sensitive = None
        self.is_oid_marine_sensitive = None
        self.is_oid_b2b_sensitive = None
        self.file_path = file_path

    @property
    def is_truck_related(self):
        return self._is_truck_related

    @is_truck_related.setter
    def is_truck_related(self, value: bool):
        self._is_truck_related = value
        if value:
            self.check_oid_sensitivity()

    @property
    def is_marine_itt_related(self):
        return self._is_marine_itt_related

    @is_marine_itt_related.setter
    def is_marine_itt_related(self, value: bool):
        self._is_marine_itt_related = value
        if value:
            self.check_oid_sensitivity()

    def check_oid_sensitivity(self):
        name_breakdown = self.name.split('+')
        if self.is_truck_related:
            if len(name_breakdown) == 1:
                if any(name in config_copy.oid_denied_names_trucks for name in name_breakdown):
                    self.is_oid_truck_sensitive = True
                else:
                    self.is_oid_truck_sensitive = False
            elif len(name_breakdown) > 1:
                if any(doc in config_copy.oid_denied_names_trucks for doc in name_breakdown):
                    show_fail_notification(f'Please file the set "{self.name}" separately', self.file_path)
                    raise ValueError(
                        'Invalid document name format. Batch  can not contain oid sensitive document name')
                else:
                    self.is_oid_truck_sensitive = False
        elif self.is_marine_itt_related:
            if len(name_breakdown) == 1:
                if any(name in config_copy.oid_denied_names_marine for name in name_breakdown):
                    self.is_oid_marine_sensitive = True
                else:
                    self.is_oid_marine_sensitive = False
            elif len(name_breakdown) > 1:
                if any(doc in config_copy.oid_denied_names_marine for doc in name_breakdown):
                    show_fail_notification(f'Please file the set "{self.name}" separately', self.file_path)
                    raise ValueError('Invalid document name format. Batch  can not contain oid sensitive document name')
                else:
                    self.is_oid_marine_sensitive = False

    def b2b_sensitivity(self):
        name_breakdown = self.name.split('+')
        if len(name_breakdown) == 1:
            oid_sensitive_name = any(doc in config_copy.ra_conflict_names_marine_b2b for doc in name_breakdown)
            if oid_sensitive_name:
                self.is_oid_b2b_sensitive = True
            else:
                self.is_oid_marine_sensitive = False
        elif len(name_breakdown) > 1:
            oid_sensitive_name = any(doc in config_copy.ra_conflict_names_marine_b2b for doc in name_breakdown)
            if oid_sensitive_name:
                self.is_oid_marine_sensitive = True
                show_fail_notification(f'Please file the set "{self.name}" separately', self.file_path)
                raise ValueError('Invalid document name format. Batch  can not contain oid sensitive document name')
            else:
                self.is_oid_marine_sensitive = False
        else:
            raise ValueError('Invalid document name format')


class Oid:
    def __init__(self, oid: str):
        self.oid = oid


class RightAngleNumber:
    def __init__(self, ra_reference: str):
        self.ra_reference = ra_reference


class InMovement:
    def __init__(self, internal_mov_reference: str):
        self.internal_mov_reference = internal_mov_reference


class TNumber:
    def __init__(self, t_ref: str):
        self.t_ref = t_ref


class ReferenceSelector(QDialog):
    def __init__(self, references):
        super().__init__()
        self.references = references
        self.selected_reference = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        for i, reference in enumerate(self.references):
            button = QPushButton(reference)
            button.clicked.connect(lambda checked, ref=reference: self.select_reference(ref))
            layout.addWidget(button)

        # Add exit button
        exit_button = QPushButton('Exit')
        exit_button.clicked.connect(self.exit_application)
        layout.addWidget(exit_button)

        self.setLayout(layout)
        self.setWindowTitle('Select the correct deal number')
        self.setFixedSize(400, 300)
        self.show()

    def select_reference(self, reference):
        self.selected_reference = reference
        QMessageBox.information(self, 'Reference Selected', f'You selected: {reference}')
        self.close()

    def get_selected_reference(self):
        return self.selected_reference

    def exit_application(self):
        QMessageBox.information(self, 'Exiting', 'Exiting the application now...')
        QApplication.quit()
        sys.exit()



class FileHandler(QDialog):
    def __init__(self, existing_file_path, new_file_path,reference):
        super().__init__()
        self.existing_file_path = existing_file_path
        self.new_file_path = new_file_path
        self.user_choice = None
        self.reference = reference
        self.init_ui()


    def init_ui(self):
        layout = QVBoxLayout()

        # message = f'The file "{os.path.basename(self.new_file_path)}" already exists. What would you like to do?'
        self.setWindowTitle('File Conflict')

        # Add buttons for actions
        replace_button = QPushButton('Replace')
        replace_button.clicked.connect(self.replace_file)
        layout.addWidget(replace_button)

        keep_both_button = QPushButton('Keep Both')
        keep_both_button.clicked.connect(self.keep_both_files)
        layout.addWidget(keep_both_button)

        exit_button = QPushButton('Exit')
        exit_button.clicked.connect(self.exit_application)
        layout.addWidget(exit_button)

        self.setLayout(layout)
        self.setWindowTitle(f'{self.reference}  - Same file name already exists')
        self.setFixedSize(400, 200)
        self.show()

    def replace_file(self):
        os.remove(self.new_file_path)
        os.rename(self.existing_file_path, self.new_file_path)
        QMessageBox.information(self, 'File Replaced',
                                f'The file "{os.path.basename(self.new_file_path)}" has been replaced.')
        self.close()

    def keep_both_files(self):
        base, ext = os.path.splitext(self.new_file_path)
        new_file_path = f"{base}1{ext}"
        os.rename(self.existing_file_path, new_file_path)
        QMessageBox.information(self, 'File Kept',
                                f'A copy of the file "{os.path.basename(self.new_file_path)}" '
                                f'has been saved as "{os.path.basename(new_file_path)}".')
        self.close()

    def exit_application(self):
        QMessageBox.information(self, 'Exiting', 'Exiting the application now...')
        QApplication.quit()  # Exit the application
        sys.exit()  # Ensure the script terminates

    def get_user_choice(self):
        return self.user_choice
