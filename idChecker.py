# coding=utf-8
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
#   - Remember to download uao_decode (https://gist.github.com/andycjw/5617496)
import telnetlib, pyte, uao_decode, codecs
import os, sys, time, re, argparse, datetime

siteName = 'ptt.cc'

parser = argparse.ArgumentParser(description='PTT id checker')
parser.add_argument('selfaccount' , help='Your account')
parser.add_argument('selfpassword', help='Your password')
parser.add_argument('otheraccount', help='Account to be checked')
parser.add_argument('--interval'  , '-i', default=0, type=int, help='Time interval (in sec) for repeating, non-positive number for no repeat')
parser.add_argument('--repeattime', '-r', default=1, type=int, help='Repeat time')

args = parser.parse_args()
account  = args.selfaccount
password = args.selfpassword
liar     = args.otheraccount
interval = args.interval
repeat   = args.repeattime

tn = telnetlib.Telnet()
counter = 0

while True:
    # Login
    print 'Login...'
    tn.open(siteName)
    tn.read_until('或以 new 註冊:')
    tn.write(account + '\r\n')
    tn.read_until('請輸入您的密碼:')
    tn.write(password + '\r\n')
    time.sleep(3)
    tn.write('\r\n')
    tn.read_until('離開，再見')

    # 進入查詢 ID 畫面
    print 'Querying...'
    tn.write('t\r\nq\r\n')
    tn.read_until('請輸入使用者代號:')
    tn.write(liar + '\r\n')
    content = ''
    while '五子棋'.decode('uao_decode', 'ignore') not in content:
        content += tn.read_very_eager().decode('uao_decode', 'ignore')

    # 抓取 ID
    ipStr = re.search('(\\d+\.){3}\\d+', content).group(0)
    nowStr = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    print 'Result:', nowStr, ipStr
    with codecs.open(liar + '.txt', 'a', encoding='utf8') as fout:
        fout.write(nowStr + ' ' + ipStr + '\r\n')

    tn.write('\x1B[D') # left (?)
    tn.write('g')      # Goodbye
    tn.write('\r\ny\r\n\r\n')
    tn.close()
    
    counter += 1
    if(counter>=repeat):
        break
    
    if(interval>0):
        time.sleep(interval)
    else:
        break
