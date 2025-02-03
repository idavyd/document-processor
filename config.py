from pathlib import Path
from string import punctuation


naming_convention = ['ANX7', 'NOMDP', 'ATR', 'NOMINSP', 'BL', 'NOMLP', 'CC', 'OBQ', 'CD', 'PL', 'CM', 'PLAN', 'CMR',
                     'PoS', 'COA', 'PPINV', 'COO', 'PTS', 'COQ', 'Q88', 'CR', 'RECAPBRK', 'DDC', 'RECAPEXT', 'DEMB',
                     'RECAPFIX', 'DEMOWN', 'RECAPINT', 'DEMS', 'SAD', 'DN', 'SAD1', 'DR', 'SAD2', 'EAD', 'SAD3', 'EUR1',
                     'SBLC', 'EXD', 'SD', 'FIXCONFIRM', 'SDS', 'FCR', 'SDR', 'FOR', 'SLD', 'INV', 'SoF', 'ITS', 'SP',
                     'IRC', 'SR', 'LAYC', 'STMD', 'LC', 'STR', 'LoP', 'STSR', 'LR', 'TL', 'LASTCAR', 'UR',
                     'MARPOL', 'VO', 'NOA', 'WS', 'NOR', 'WTN', 'NOAD', 'SWIFT', 'LOP']

oid_denied_names_marine = ['RECAPEXT', 'RECAPFIX', 'RECAPBRK', 'RECAPINT', ]

oid_denied_names_trucks = ['SBLC', 'RECAPEXT', 'RECAPINT', 'RECAPFIX', 'RECAPBRK', 'NOMLP', 'NOMDP', 'NOMINSP', 'Q88',
                           'SDS', 'PLAN']
ra_conflict_names_marine_b2b = ['NOMLP', 'NOMDP', 'NOMINSP', 'SBLC', 'INV',]

transport_group_1 = ['Truck', 'ISO Tanks']
transport_group_2 = ['Barge', 'Vessel', 'ITT', 'Storage']
deal_types = ['Single Buy/Sell', 'B2B']
products = ['FAME', 'FO', 'GO']
patterns = [r'^\d{4,6}$', r'^[A-Za-z]{5}\d{2}[Tt][SsPp]\d{4}$', r'^[Ii][Nn]\d{8}', r'[Tt]\d{8}']
conflict_references = []
conflict_oid = set()
CSV_FILE_PATH = r'C:\Users\IDavydenko\ACT Commodities\Fuels-MO - Ops books\Export from BI report'
SOURCE_DIR_PATH = r'C:\Python'
DEST_DIR_PATH_PHYSICAL = r'C:\Users\IDavydenko\ACT Commodities\Fuels-MO - Deals'
DEST_DIR_PATH_CERTIFICATES = r'C:\Users\IDavydenko\ACT Commodities\Fuels-MO - Certificate Deals'
dst_dir_physical = Path(DEST_DIR_PATH_PHYSICAL)
dst_dir_certificates = Path(DEST_DIR_PATH_CERTIFICATES)
source_dir = Path(SOURCE_DIR_PATH)
successful_icon_path = r'C:\Users\IDavydenko\OneDrive - ACT Commodities\Desktop\project1\Success.png'
failed_icon_path = r'C:\Users\IDavydenko\OneDrive - ACT Commodities\Desktop\project1\Fail.ico'
toaster_app_id = 'Document Filing'
specials_chars = list(punctuation.replace('+', ''))
