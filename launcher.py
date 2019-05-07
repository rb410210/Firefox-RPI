#!/usr/bin/env python

import sys
import json
import struct
import subprocess
import time

try:
    # Python 3.x version
    # Read a message from stdin and decode it.
    import urllib.parse as urlparse
    def getMessage():
        rawLength = sys.stdin.buffer.read(4)
        if len(rawLength) == 0:
            sys.exit(0)
        messageLength = struct.unpack('@I', rawLength)[0]
        message = sys.stdin.buffer.read(messageLength).decode('utf-8')
        return json.loads(message)

    # Encode a message for transmission,
    # given its content.
    def encodeMessage(messageContent):
        encodedContent = json.dumps(messageContent).encode('utf-8')
        encodedLength = struct.pack('@I', len(encodedContent))
        return {'length': encodedLength, 'content': encodedContent}

    # Send an encoded message to stdout
    def sendMessage(encodedMessage):
        sys.stdout.buffer.write(encodedMessage['length'])
        sys.stdout.buffer.write(encodedMessage['content'])
        sys.stdout.buffer.flush()

    while True:
        receivedMessage = getMessage()
        if receivedMessage.startswith('https://www.youtube.com/'):
            subprocess.check_call(['bash', '-c', 'ssh osmc@rpi \'tsp youtube-dl -o "/media/Elements/Youtube/%(title)s.%(ext)s" -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4" "' + receivedMessage + '"\''], shell = False)
        else:
            parsed = urlparse.urlparse(receivedMessage)
            vevoUrl = urlparse.parse_qs(parsed.query)['url'][0]
            subprocess.check_call(['bash', '-c', 'ssh osmc@rpi tsp "/usr/sbin/videoDownload \'' + vevoUrl + '\'" >>/tmp/vevo-output.txt'], shell = False)
        sendMessage(encodeMessage(receivedMessage))
except AttributeError:
    # Python 2.x version (if sys.stdin.buffer is not defined)
    # Read a message from stdin and decode it.
    def getMessage():
        rawLength = sys.stdin.read(4)
        if len(rawLength) == 0:
            sys.exit(0)
        messageLength = struct.unpack('@I', rawLength)[0]
        message = sys.stdin.read(messageLength)
        return json.loads(message)

    # Encode a message for transmission,
    # given its content.
    def encodeMessage(messageContent):
        encodedContent = json.dumps(messageContent)
        encodedLength = struct.pack('@I', len(encodedContent))
        return {'length': encodedLength, 'content': encodedContent}

    # Send an encoded message to stdout
    def sendMessage(encodedMessage):
        sys.stdout.write(encodedMessage['length'])
        sys.stdout.write(encodedMessage['content'])
        sys.stdout.flush()

    while True:
        receivedMessage = getMessage()
        # subprocess.check_call(['bash', '-c', '/usr/sbin/roku -w ' + receivedMessage + ' 1>/dev/null 2>&1'], shell = False)
        sendMessage(encodeMessage(receivedMessage))
