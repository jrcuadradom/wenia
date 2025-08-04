# Geolocation project
_This project looks for addresses in PDF files and create a list of homonyms based on them looking the similarity of an address and its homonym._

## The code
_This project was done in Python 3.10. It calls AWS S3, Geocoding and Google Maps APIs to get coordinates and mark address in maps._
1. The Document*.pdf files in /Documents are pushed to S3 and the code looks for addresses in them.
2. With the address grabbed from the Document*.pdf the code create a list of homonyms that are stored in *addresses.xlsx and pushed to S3.
3. Each homonym is compared with the original address to have a similarity value.
4. Those addresses with the similarity above 90% are stored in *addresses_validated.xlsx and pushed to S3.
5. The coordinates of the addresses are got from the google API and marked in a map stored in /.


### How to run it.
To test the code calling the APIs of AWS and Google you have to create a file called 'keys.env' in / with the below structure.
```
API_KEY = your_google_key (from Geocoding API)
MAP_KEY = your_map_key (from Maps JavaScript API)
AWS_KEY = your_aws_key
AWS_SECRET_KEY = your_aws_secret_key
BUCKET = your_s3_bucket
```

Create a folder Documents/ in S3

The Documents folder in this repository shows you the documents and the addresses processed (*addresses.xlsx and *addresses_validated.xlsx)

__To protect the keys the *map.html file is stored in the local disk__







