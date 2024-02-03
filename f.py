import mimetypes

file_type, encoding = mimetypes.guess_type('ANDAMAN & NICOBAR_data/table_data_1')
print(f'Type: {file_type}, Encoding: {encoding}')
