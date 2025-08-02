import boto3
from openpyxl import Workbook, load_workbook


ADDRESS_STREET = ['CRA', 'Kra', 'Carrera', 'Calle', 'Transversal']
ADDRESS_NUM = ['#','No', 'Num', 'Numero']
ADDRESS_DIV = ['-',' ']
wb_name = "addresses.xlsx"
NORMAL_ADDRESS = {'CRA': 'CRA', 'Kra': 'CRA', 'Carrera': 'CRA'}

def connect_to_bucket():
    s3_client = boto3.resource('s3',

                               aws_access_key_id='your_key',
                               aws_secret_access_key='your_secret_key',
                               region_name='us-west-1')

    bucket_name = 'bucket_name'
    s3client_bucket = s3_client.Bucket(bucket_name)
    return s3client_bucket

def upload_document(document, file_path):
    file = file_path
    object_key = '/carpeta/'.file_path
    connect_to_bucket().upload_file(file, object_key)

def get_document(file_path):
    #file = file_path
    #object_key = '/carpeta/'.file_path
    #get_file = connect_to_bucket().Object(file, object_key)
    #content = get_file.get()['Body'].read().decode('utf-8')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    print(content)
    return content

def find_homonyms(content):
    homonyms = []
    split_address = content.replace('#', '').replace('-','').split()
    #print(partes)
    for x in ADDRESS_STREET:
        for y in ADDRESS_NUM:
            for z in ADDRESS_DIV:
                direccion = x + ' ' + split_address[1] + ' '+ y + ' '+ split_address[2] + ' ' + z + ' '+ split_address[3]
                homonyms.append(direccion.replace('   ',' '))
    print(homonyms)
    return homonyms

def homonyms_to_excel(data):
    wb = Workbook()
    ws = wb.active
    index = 1
    #while index <= len(data):
    for j in data:
        ws['A'+str(index)] = j
        index+=1
        #print(j, index)

    wb.save("Documents/"+wb_name)

def accuracy_check(address_original):
    address_original_low = address_original.lower()
    homonyms_address_low = homonyms_address.lower()
    wb = load_workbook("Documents/"+wb_name)
    sheet = wb.active
    for row in sheet['A'+sheet.max_row]:
        print(row)





if __name__ == '__main__':
    contenido = get_document('Documents/doc1.txt')
    excel = homonyms_to_excel(find_homonyms(contenido))
    accuracy_check(contenido)




