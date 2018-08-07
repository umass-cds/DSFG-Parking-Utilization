###########################################
#      DSFG ~ Katie House ~ 8/6/18
# DESCTIPTION: List Google Drive links for Automan
# INPUT: Google Drive folder ID
# OUTPUT: .txt link to pictures in Google Drive
###########################################


from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file as oauth_file, client, tools
from apiclient import errors

# What permission does the API have:
SCOPES = 'https://www.googleapis.com/auth/drive.metadata'

def list_parking_image_links(service, folder_id):
  """List image links in Google Drive Folder.
  Args:
    service: Drive API service instance.
    folder_id: ID of the folder to print files from.
  """
  page_token = None
  f = open('parking-800by600-data-links.txt','w')
  while True:
    try:
      param = {}
      if page_token:
        param['pageToken'] = page_token
      children = service.children().list(
          folderId=folder_id, **param).execute()
      for child in children.get('items', []):
        link = 'https://drive.google.com/uc?id=' + child['id']
        print(link)
        f.write(link + ',\n')
      page_token = children.get('nextPageToken')
      if not page_token:
        break
    except errors.HttpError:
      print('Error: %s' % errors.HttpError)
      break

def main():    
    store = oauth_file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v2', http=creds.authorize(Http()))

    # List all image links in a .txt file
    list_parking_image_links(service, '10HIEz9f-RUa6V9QaLFoLXJICqQPy_F3S')
    
if __name__ == '__main__':
    main()
    