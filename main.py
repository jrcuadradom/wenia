import difflib
import os
import boto3
import requests
from openpyxl import Workbook, load_workbook
from dotenv import load_dotenv


ADDRESS_STREET = ['CRA', 'Carrera', 'Calle', 'Cl', 'Transversal', 'Tv']
ADDRESS_NUM = ['#','No', 'Num', 'Numero']
ADDRESS_DIV = ['-',' ']
wb_name = "addresses.xlsx"
wb_accuracy = "addresses_validated.xlsx"
NORMAL_ADDRESS = {'CRA': 'CRA', 'Kra': 'CRA', 'Carrera': 'CRA', '#': '#','No': '#', 'Num': '#', 'Calle': 'Calle','Cl': 'Calle', 'Tv': 'Transversal', 'Transversal': 'Transversal','Numero': '#'}
map_html= "map.html"



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
    for x in ADDRESS_STREET:
        for y in ADDRESS_NUM:
            for z in ADDRESS_DIV:
                direccion = x + ' ' + split_address[1] + ' '+ y + ' '+ split_address[2] + ' ' + z + ' '+ split_address[3]
                homonyms.append(direccion.replace('   ',' '))
    homonyms_to_excel(homonyms, 'homonyms')
    return homonyms

def homonyms_to_excel(data, type):
    wb = Workbook()
    ws = wb.active
    index = 1
    #while index <= len(data):
    if(type == 'homonyms'):
        for j in data:
            ws['A'+str(index)] = j
            index+=1
        wb.save("Documents/" + wb_name)
    elif(type == 'accuracy'):
        for j in data:
            ws['A' + str(index)] = j[0]
            ws['B' + str(index)] = j[1]
            ws['C' + str(index)] = j[2]
            index += 1
        wb.save("Documents/" + wb_accuracy)

def normalize_address(address):
    split_address = address.replace('-', '').split()
    direccion = NORMAL_ADDRESS[split_address[0]] + ' ' + split_address[1]+ ' ' + NORMAL_ADDRESS[split_address[2]] +' ' + split_address[3] + ' - ' + split_address[4]
    return direccion
def accuracy_check(address_original):
    accuracy_list=[]
    all = []
    address_original_low = normalize_address(address_original).lower()
    wb = load_workbook("Documents/"+wb_name)
    sheet = wb.active
    for row in range(1,sheet.max_row+1):
        value = sheet['A'+str(row)].value
        normal_address = normalize_address(value).lower()
        similitud = difflib.SequenceMatcher(None,address_original_low, normal_address).ratio()
        #to find the similarity without normalized address
        #similitud = difflib.SequenceMatcher(None, address_original_low, value.lower()).ratio()
        if(similitud > 0.9):
            accuracy_list.append(value)
            accuracy_list.append(similitud)
            coords = get_geo_location(value)
            accuracy_list.append(str(coords[0]) +', ' + str(coords[1]))
            all.append(accuracy_list.copy())
            accuracy_list.clear()
    homonyms_to_excel(all, 'accuracy')
    return accuracy_list


def get_geo_location(direccion):
    load_dotenv('keys.env')
    api_key = os.getenv("API_KEY")
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
            "address": direccion+', Bogota',
            "key": api_key
    }
    respond = requests.get(url, params=params)
    data = respond.json()
    coord = data['results'][0]['geometry']['location']
    return coord['lat'], coord['lng']


def load_map():
    load_dotenv('keys.env')
    map_key = os.getenv("MAP_KEY")
    checked_coors = []
    wb = load_workbook("Documents/"+wb_accuracy)
    sheet = wb.active
    for row in range(1, sheet.max_row + 1):
        value = sheet['C' + str(row)].value
        if value not in checked_coors:
            checked_coors.append(value)
    with open(map_html,'w') as f:
        f.write(f"""
        <html>
  <head>
    <title>Add a Map with Markers using HTML</title>

    <link rel="stylesheet" type="text/css" href="./style.css" />
    <script type="module" src="./index.js"></script>
  </head>
  <body>
    <gmp-map
      center="4.6548449,-74.1586209"
      zoom="10"
      map-id="DEMO_MAP_ID"
      style="height: 500px"
    >""")
        for coor in checked_coors:
            f.write(f"""<gmp-advanced-marker
            position="{coor}"
            ></gmp-advanced-marker>
            """)
        f.write(f"""< / gmp-map >
    <script
      src="https://maps.googleapis.com/maps/api/js?key={map_key}&libraries=maps,marker&v=beta"
      defer
    ></script>
  </body>
</html>
        """)

if __name__ == '__main__':
    contenido = get_document('Documents/doc1.txt')
    excel = find_homonyms(contenido)
    accuracy_check(contenido)
    load_map()




