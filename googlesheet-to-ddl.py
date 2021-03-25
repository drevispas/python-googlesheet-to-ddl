from __future__ import print_function
import pickle
import os.path
import struct
import time
from random import SystemRandom
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1Sb0MC15LSKdRjcST51siXnBhWUeNkQCdohlCtKuUNjY'
SAMPLE_RANGE_NAME = '참고.BS_금융기관ID!A4:E'


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials-brad.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        _MAX_COUNTER_VALUE = 0xFFFFFF
        _inc = SystemRandom().randint(0, _MAX_COUNTER_VALUE)
        for row in values:
            # Generate an organizationObjectId according to MongoDB ObjectId source code.
            # See (https://github.com/mongodb/mongo-python-driver).
            # 4 bytes current time
            oid = struct.pack(">I", int(time.time()))
            # 5 bytes random
            oid += os.urandom(5)
            # 3 bytes inc
            oid += struct.pack(">I", _inc)[1:4]
            hex_string = oid.hex()
            _inc = (_inc + 1) % (_MAX_COUNTER_VALUE + 1)
            # Print columns A and E, which correspond to indices 0 and 4.
            writer = 'brad@rainist.com'
            print("insert into connect_organization"
                  "(sector,industry,organization_id,organization_objectid,organization_status,is_deleted"
                  ",created_at,created_by,updated_at,updated_by)"
                  " values "
                  "('finance','%s','%s','%s','active',false,current_timestamp,'%s',current_timestamp,'%s');" % (
                      row[3][1:], row[4], hex_string, writer, writer))


if __name__ == '__main__':
    main()
