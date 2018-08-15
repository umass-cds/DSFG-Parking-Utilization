
###########################################
#      DSFG ~ Katie House ~ 8/14/18
# DESCTIPTION: List Google Drive links for Automan
# INPUT: Google Drive File ID
# OUTPUT: Google Drive Folder ID
###########################################

from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file as oauth_file, client, tools
from apiclient import errors


def print_parents(service, file_id):
  """Print a file's parents.

  Args:
    service: Drive API service instance.
    file_id: ID of the file to print parents for.
  """
  try:
    parents = service.parents().list(fileId=file_id).execute()
    for parent in parents['items']:
      print('File Id: %s' % parent['id'])
  except error:
    print('An error occurred: %s' % error)

def main():    
    store = oauth_file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v2', http=creds.authorize(Http()))

    # List all image links in a .txt file
    print_parents(service, '1_3g_aKodcJxYnuMZObePMN77AjnQlBmM')
    
if __name__ == '__main__':
    main()
    