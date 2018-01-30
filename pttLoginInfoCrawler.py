# coding=big5
# Ref: http://mhwong2007.logdown.com/posts/314403
# Parameters: account, password (optional), board name
# Assumptions:
#   - File for this source is saved in big5 (ANSI)
#   - No "Announcement" in BBS
#   - Input parameters are correct
#   - Your account exists and currently is not login
#   - The account to be checked exists
# Notes:
#   - You may need to install "pyte" or other libs
import telnetlib, pyte, codecs
import os, sys, time, re, argparse, datetime

siteName = 'ptt.cc'

parser = argparse.ArgumentParser(description='PTT id checker')
parser.add_argument('selfaccount' , help='Your account')
parser.add_argument('selfpassword', help='Your password')
parser.add_argument('otheraccount', help='Account to be checked')
parser.add_argument('--interval'  , '-i', default=1200, type=int, help='Time interval (in sec) for repeating, non-positive number for no repeat')
parser.add_argument('--repeattime', '-r', default=48  , type=int, help='Repeat time')
parser.add_argument('--timeout'   , '-t', default=8   , type=int, help='Repeat time')

args = parser.parse_args()
account  = args.selfaccount
password = args.selfpassword
liar     = args.otheraccount
interval = args.interval
repeat   = args.repeattime
timeout  = args.timeout

tn = telnetlib.Telnet()
counter = 0

while True:
    try:
        # Login
        print('Login...')
        tn.open(siteName, 23, timeout)
        tn.read_until(bytes('�ΥH new ���U:', 'big5'), timeout)
        tn.write((account + '\r\n').encode('ascii'))
        tn.read_until(bytes('�п�J�z���K�X:', 'big5'), timeout)
        tn.write((password + '\r\n').encode('ascii'))
        time.sleep(3)
        tn.write('\r\n'.encode('ascii'))
        tn.read_until(bytes('���}�A�A��', 'big5'), timeout)

        # �i�J�d�� ID �e��
        print('Querying...')
        tn.write('t\r\nq\r\n'.encode('ascii'))
        tn.read_until(bytes('�п�J�ϥΪ̥N��:', 'big5'), timeout)
        tn.write((liar + '\r\n').encode('ascii'))
        content = ''
        while '���l��' not in content:
            content += tn.read_very_eager().decode('big5')

        # ��� ID
        ipStr = re.search('(\\d+\.){3}\\d+', content).group(0)
        nowStr = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        print('Result:', nowStr, ipStr)
        with codecs.open(liar + '.txt', 'a', encoding='utf8') as fout:
            fout.write(nowStr + ' ' + ipStr + '\r\n')

        tn.write('\x1B[D'.encode('ascii')) # left (?)
        tn.write('g'.encode('ascii'))      # Goodbye
        tn.write('\r\ny\r\n\r\n'.encode('ascii'))

    except Exception as e:
        nowStr = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        with codecs.open(liar + '.txt', 'a', encoding='utf8') as fout:
            fout.write(nowStr + ' FAIL: {}\r\n'.format(e))

    tn.close()
    
    counter += 1
    if(counter>=repeat):
        break
    
    if(interval>0):
        time.sleep(interval)
    else:
        break
