import base64
import os
import sys

import eml_parser


def main():
    if len(sys.argv) == 2:
        if sys.argv[1] == 'test':
            CEDS_LOG_PATH = './'
    else:
        CEDS_LOG_PATH = '/home/ceds_log/cbm_zip/'
    eml_pipe = sys.stdin.read().encode()
    ep = eml_parser.parser.EmlParser(include_attachment_data=True)
    eml = ep.decode_email_bytes(eml_pipe)
    if eml.get('attachment'):
        for i in eml['attachment']:
            x = base64.b64decode(i['raw'])
            with open(CEDS_LOG_PATH + i['filename'], 'wb') as f:
                f.write(x)
            os.system('/home/ceds_log/github/cbm-email-ziplog-to-file/trigger.sh ' + i['filename'] + '>/tmp/' + i['filename'] + ' 2>&1')
    else:
        print('No Attachment')


if __name__ == '__main__':
    main()
