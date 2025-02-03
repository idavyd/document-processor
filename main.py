import config
import classes
import functions
import re
import shutil


for raw_file in config_copy.source_dir.iterdir():
    if raw_file.is_file():
        raw_reference, raw_doc_name, comment = functions_copy.unpack_file_name(raw_file)
        reference = functions_copy.review_reference(raw_reference, raw_file.parent)
        document = functions_copy.review_document_name(raw_doc_name, raw_file.parent)
        data = functions_copy.merge_csv_files(config_copy)

        if isinstance(reference, classes_copy.Oid):
            n_of_file_copies = 0
            oid_found = False
            for line in data:
                deal_type, ra_number, counter_deal = line[1], line[5], line[6]
                oid_cell, transport, credit_type = line[12], line[15], line[47]
                match = re.match(pattern=config_copy.patterns[1], string=ra_number)
                if oid_cell == reference.oid and match:
                    dst_path = config_copy.DEST_DIR_PATH_PHYSICAL + f'\\{ra_number}'
                    oid_found = True
                    if transport in config_copy.transport_group_1:
                        document.is_truck_related = True
                        if document.is_oid_truck_sensitive:
                            if deal_type == config_copy.deal_types[0]:
                                new_name = f'{dst_path}\\{ra_number}-{document.name}{raw_file.suffix}'
                                if comment is not None:
                                    new_name = f'{dst_path}\\{ra_number}-{document.name}-{comment}{raw_file.suffix}'
                                functions_copy.move_file(raw_file, new_name, ra_number, dst_path)
                                break
                            elif deal_type == config_copy.deal_types[1]:
                                config_copy.conflict_references.append(ra_number)
                                if len(config_copy.conflict_references) >= 2:
                                    selector = classes_copy.ReferenceSelector(config_copy.conflict_references)
                                    classes_copy.app.exec_()
                                    selected_ref = selector.get_selected_reference()
                                    if selected_ref is not None:
                                        dst_path = config_copy.DEST_DIR_PATH_PHYSICAL + f'\\{selected_ref}'
                                        new_name = f'{dst_path}\\{selected_ref}-{document.name}{raw_file.suffix}'
                                        if comment is not None:
                                            new_name = (f'{dst_path}\\{selected_ref}-{document.name}'
                                                        f'-{comment}{raw_file.suffix}')
                                        functions_copy.move_file(raw_file, new_name, selected_ref, dst_path)
                                    else:
                                        exit()
                        else:
                            new_name = f'{dst_path}\\{ra_number}-{reference.oid}-{document.name}{raw_file.suffix}'
                            if comment is not None:
                                new_name = (f'{dst_path}\\{ra_number}-{reference.oid}'
                                            f'-{document.name}-{comment}{raw_file.suffix}')
                            functions_copy.move_file(raw_file, new_name, ra_number, dst_path=dst_path)
                            functions_copy.sleep()
                            if deal_type == config_copy.deal_types[0]:
                                break
                            elif deal_type == config_copy.deal_types[1]:
                                n_of_file_copies += 1
                                if n_of_file_copies == 1:
                                    shutil.copyfile(new_name, raw_file)
                                elif n_of_file_copies == 2:
                                    break

                    elif transport in config_copy.transport_group_2:
                        document.is_marine_itt_related = True
                        if document.is_oid_marine_sensitive:
                            if (deal_type == config_copy.deal_types[0] or deal_type == config_copy.deal_types[0]
                                    and len(credit_type) > 0):
                                new_name = f'{dst_path}\\{ra_number}-{document.name}{raw_file.suffix}'
                                if comment is not None:
                                    new_name = f'{dst_path}\\{ra_number}-{document.name}-{comment}{raw_file.suffix}'
                                functions_copy.move_file(raw_file, new_name, ra_number, dst_path)
                                break
                            elif deal_type == config_copy.deal_types[1] and len(counter_deal) == 0:
                                config_copy.conflict_references.append(ra_number)
                                if len(config_copy.conflict_references) >= 2:
                                    selector = classes_copy.ReferenceSelector(config_copy.conflict_references)
                                    classes_copy.app.exec_()
                                    selected_ref = selector.get_selected_reference()
                                    if selected_ref is not None:
                                        dst_path = config_copy.DEST_DIR_PATH_PHYSICAL + f'\\{selected_ref}'
                                        new_name = f'{dst_path}\\{selected_ref}-{document.name}{raw_file.suffix}'
                                        if comment is not None:
                                            new_name = (f'{dst_path}\\{ra_number}-{document.name}'
                                                        f'-{comment}{raw_file.suffix}')
                                        functions_copy.move_file(raw_file, new_name, selected_ref, dst_path)
                                    else:
                                        exit()
                        else:
                            if (deal_type == config_copy.deal_types[0] or deal_type == config_copy.deal_types[0]
                                    and len(credit_type) > 0) and len(counter_deal) == 0:
                                new_name = f'{dst_path}\\{ra_number}-{reference.oid}-{document.name}{raw_file.suffix}'
                                if comment is not None:
                                    new_name = (f'{dst_path}\\{ra_number}-{reference.oid}'
                                                f'-{document.name}-{comment}{raw_file.suffix}')
                                functions_copy.move_file(raw_file, new_name, ra_number, dst_path=dst_path)
                                break
                            elif deal_type == config_copy.deal_types[1] and len(counter_deal) == 0:
                                document.b2b_sensitivity()
                                if document.is_oid_b2b_sensitive:
                                    config_copy.conflict_references.append(ra_number)
                                    if len(config_copy.conflict_references) >= 2:
                                        selector = classes_copy.ReferenceSelector(config_copy.conflict_references)
                                        classes_copy.app.exec_()
                                        selected_ref = selector.get_selected_reference()
                                        if selected_ref is not None:
                                            dst_path = config_copy.DEST_DIR_PATH_PHYSICAL + f'\\{selected_ref}'
                                            new_name = f'{dst_path}\\{selected_ref}-{reference.oid}-{document.name}{raw_file.suffix}'
                                            if comment is not None:
                                                new_name = (f'{dst_path}\\{selected_ref}-{reference.oid}-{document.name}'
                                                            f'-{comment}{raw_file.suffix}')
                                            functions_copy.move_file(raw_file, new_name, selected_ref, dst_path)
                                        else:
                                            exit()
                                else:
                                    new_name = f'{dst_path}\\{ra_number}-{reference.oid}-{document.name}{raw_file.suffix}'
                                    if comment is not None:
                                        new_name = (f'{dst_path}\\{ra_number}-{reference.oid}'
                                                    f'-{document.name}-{comment}{raw_file.suffix}')
                                    functions_copy.move_file(raw_file, new_name, ra_number, dst_path=dst_path)
                                    functions_copy.sleep()
                                    n_of_file_copies += 1
                                    if n_of_file_copies == 1:
                                        shutil.copyfile(new_name, raw_file)
                                    elif n_of_file_copies == 2:
                                        break

            if oid_found is False:
                functions_copy.show_fail_notification(f"{reference.oid} wasn't found", raw_file.parent)
                raise ValueError(f'{reference.oid} was not found')

        elif isinstance(reference, classes_copy.RightAngleNumber):
            n_of_file_copies = 0
            ra_number_found = False
            for line in data:
                deal_type, ra_number, oid_cell, transport = line[1], line[5], line[12], line[15]
                if ra_number == reference.ra_reference:
                    ra_number_found = True
                    dst_path = config_copy.DEST_DIR_PATH_PHYSICAL + f'\\{ra_number}'

                    if transport in config_copy.transport_group_1:
                        new_name = functions_copy.construct_new_name(dst_path, reference.ra_reference,
                                                                     document.name, raw_file.suffix, comment)
                        functions_copy.move_file(raw_file, new_name, ra_number, dst_path)
                        break

                    elif transport in config_copy.transport_group_2:
                        document.is_marine_itt_related = True

                    if document.is_oid_marine_sensitive:
                        new_name = functions_copy.construct_new_name(dst_path, reference.ra_reference,
                                                                     document.name, raw_file.suffix, comment)
                        functions_copy.move_file(raw_file, new_name, ra_number, dst_path)
                        break

                    else:
                        for row in data:
                            if reference.ra_reference == row[5]:
                                match = re.match(pattern=config_copy.patterns[0], string=row[12])
                                if match:
                                    config_copy.conflict_oid.add(row[12])
                        selected_oid = list(config_copy.conflict_oid)
                        if len(config_copy.conflict_oid) == 1:
                            new_name = f'{dst_path}\\{ra_number}-{selected_oid[0]}-{document.name}{raw_file.suffix}'
                            if comment is not None:
                                new_name = f'{dst_path}\\{ra_number}-{selected_oid[0]}-{document.name}-{comment}{raw_file.suffix}'
                            functions_copy.move_file(raw_file, new_name, ra_number, dst_path)
                            functions_copy.sleep()

                            if deal_type == config_copy.deal_types[1]:
                                document.b2b_sensitivity()
                                if document.is_oid_b2b_sensitive:
                                    exit()
                                else:
                                    shutil.copy(new_name, raw_file)
                                    for i in data:
                                        if selected_oid[0] == i[12] and i[5] != reference.ra_reference and re.match(pattern=config_copy.patterns[1],string=i[5]):
                                            shutil.copy(new_name, raw_file)
                                            dst_path = config_copy.DEST_DIR_PATH_PHYSICAL + f'\\{i[5]}'
                                            new_name = f'{dst_path}\\{i[5]}-{selected_oid[0]}-{document.name}{raw_file.suffix}'
                                            if comment is not None:
                                                new_name = f'{dst_path}\\{i[5]}-{selected_oid[0]}-{document.name}-{comment}{raw_file.suffix}'
                                            functions_copy.move_file(raw_file, new_name, i[5], dst_path)
                                            break
                        elif 1 < len(config_copy.conflict_oid) <= 5:
                            selector = classes_copy.ReferenceSelector(selected_oid)
                            classes_copy.app.exec_()
                            selected_ref = selector.get_selected_reference()
                            if selected_ref is not None:
                                dst_path = config_copy.DEST_DIR_PATH_PHYSICAL + f'\\{reference.ra_reference}'
                                new_name = f'{dst_path}\\{reference.ra_reference}-{selected_ref}-{document.name}{raw_file.suffix}'
                                if comment is not None:
                                    new_name = (f'{dst_path}\\{reference.ra_reference}-{selected_ref}-{document.name}'
                                                f'-{comment}{raw_file.suffix}')
                                functions_copy.move_file(raw_file, new_name, reference.ra_reference, dst_path)
                                functions_copy.sleep()
                                if deal_type == config_copy.deal_types[1]:
                                    document.b2b_sensitivity()
                                    if document.is_oid_b2b_sensitive:
                                        exit()
                                    else:
                                        print('test1')
                                        shutil.copy(new_name, raw_file)
                                        for i in data:
                                            if selected_oid[0] == i[12] and i[5] != reference.ra_reference:
                                                dst_path = config_copy.DEST_DIR_PATH_PHYSICAL + f'\\{i[5]}'
                                                new_name = f'{dst_path}\\{i[5]}-{selected_ref}-{document.name}{raw_file.suffix}'
                                                if comment is not None:
                                                    new_name = f'{dst_path}\\{i[5]}-{selected_ref}-{document.name}-{comment}{raw_file.suffix}'
                                                functions_copy.move_file(raw_file, new_name, i[5], dst_path)
                                                break
                                else:
                                    break
                        elif len(config_copy.conflict_oid) == 0:
                            new_name = functions_copy.construct_new_name(dst_path, reference.ra_reference,
                                                                         document.name, raw_file.suffix, comment)
                            functions_copy.move_file(raw_file, new_name, ra_number, dst_path)
                            break
                        else:
                            (functions_copy.show_fail_notification
                             (f'{reference.ra_reference} has more than 5 OIDs\nRename file with proper OID number',
                              raw_file.parent))
                            raise ValueError('Too many buttons to create')
            if not ra_number_found:
                functions_copy.show_fail_notification(f"{reference.ra_reference} wasn't found", raw_file.parent)
                raise ValueError(f'{reference.ra_reference} was not found')

        elif isinstance(reference, classes_copy.InMovement):
            functions_copy.file_document(raw_file, config_copy.dst_dir_physical,
                                         reference.internal_mov_reference, config_copy.dst_dir_physical)

        elif isinstance(reference, classes_copy.TNumber):
            functions_copy.file_document(raw_file, config_copy.dst_dir_certificates,
                                         reference.t_ref, config_copy.dst_dir_certificates)