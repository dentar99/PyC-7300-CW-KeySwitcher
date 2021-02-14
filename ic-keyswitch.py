#!/usr/bin/python3
#
# Author: Tom N4LSJ -- EXPERIMENTAL CODE ONLY FOR TINKERING
#                   -- USE AT YOUR OWN RISK ONLY
#                   -- AUTHOR ASSUMES NO LIABILITY
#
# INSTRUCTIONS:
# 
#    By using this program, you agree it is at your own risk
#
#    This program works robustly by, for each operation, trying
#    to use a network service first, and if not present, trying
#    a second network service, and if that one is not present,
#    then trying direct serial.  
#
#    If you use Hamlib, then rigctld_host and rigctld_port need
#    to be set, and this is the preferred method as it will allow
#    your other apps using hamlib to access your radio at the
#    same time.  rigctld_host is an IP or host name, and 
#    rigctld_port is a port number.
#
#    serport is the device name for your serial port.  The
#    downside to serial port is that other "cat" programs
#    may not be able to share nicely.
#
#    baud is whatever baud rate you're using on the serial
#    port specified above.  Most folks will use 19200 but
#    those who "Unlink from Remote" and set their baud rates
#    to something different will have to match that setting
#
#    If you're not using the network items, leave the defaults
#    there so that it will immediately 
#
#
# dbg(argy) prints argy if True
# rlinput(prompt, prefill) prompts and uses prefill on enter
# g2ll (grid) grid to lon/lat
# gdist(lat1, lon1, lat2, lon2) distance between two lat lon points
# distance(mygrid, othergrid) distance between two grid
# hovertxt(txt): text for widget called hlabel
# hover(widg,txt): setup for hovertxt
# startclock(*args): runs putdate() over and over
# numonly(val): returns true if input is numeric and "." only
# alnumslashonly(val): returns true if alphanumeric and slash only
# cwonly(val): returns true if chars are members of the cw data set


from math import radians, degrees, sin, cos, asin, acos, sqrt
from textwrap import wrap
import readline

global cw

def dbg(argy):
    if False:
        print("*** DEBUG: "+str(argy))


def rlinput(prompt, prefill=''):
   readline.set_startup_hook(lambda: readline.insert_text(prefill))
   try:
      return input(prompt)  # or raw_input in Python 2
   finally:
      readline.set_startup_hook()

def g2ll(grid):
    # g2ll means "grid to longitude / latitude"
    # may not be exact but good enough to get rough distance
    letters='abcdefghijklmnopqrstuvwxyz'
    offset = 9

    if len(grid)<6:
        grid=grid+'AA'

    # have to test whole string
    if (grid.upper()[0] not in letters.upper()):
        return None
    if (grid.upper()[1] not in letters.upper()):
        return None
    if (grid.upper()[2] not in '0123456789'):
        return None
    if (grid.upper()[3] not in '0123456789'):
        return None
    if (grid.upper()[4] not in letters.upper()):
        return None
    if (grid.upper()[5] not in letters.upper()):
        return None

    lat_hsd=(letters.upper().index(grid.upper()[1]) - offset) * 10
    lat_msd=(int(grid.upper()[3]) * 1)
    if (grid[5] == ''):
        grid[5] = 'A'
    lat_lsd=(letters.upper().index(grid.upper()[5]) * 0.041666)

    lon_hsd=(letters.upper().index(grid.upper()[0]) - offset) * 20
    lon_msd=(int(grid.upper()[2])  * 2)
    if (grid[4] == ''):
        grid[4] = 'A'
    lon_lsd=(letters.upper().index(grid.upper()[4]) * 0.08333)

    return [ (lat_hsd + lat_msd + lat_lsd) , (lon_hsd + lon_msd + lon_lsd) ]


def gdist(lat1, lon1, lat2, lon2):
   lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
   # 6371 for km, 3948.756 for mi
   return 3958.756 * (
     acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2))
   )

def distance(mygrid, othergrid):
    myll = g2ll(mygrid)
    otherll = g2ll(othergrid)

    if myll == None or otherll == None:
        return 9999999

    return (gdist(*myll, *otherll))




def hovertxt(txt):
        hlabel.config(text=txt)

def hover(widg,txt):
        widg.bind("<Enter>",lambda evt, tt=txt: hovertxt(tt))
        widg.bind("<Leave>",lambda evt, tt="": hovertxt(tt))

def startclock(*args):
        global clock_id
        putdate()
        clock_id=root.after(500,startclock,'')

def numonly(val):
        for ch in val:
                if (not ch in {'1','2','3','4','5','6','7','8','9','0','.'}):
                        return False
        return True

def alnumslashonly(val):
        for ch in val:
                if (not ch in ('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/')):
                        return False
        return True

def cwonly(val):
        global cw
        for ch in val:
                ch=ch.upper()
                if (not ch in cw.keys() and ch != " " and ch != "<" and ch != ">"):
                        print ("BAD CHAR: ["+ch+"]")
                        return False
        return True

cw = {
"A" : ".-", "B" : "-...", "C" : "-.-.", "D" : "-..", "E" : ".", "F" : "..-.",
"G" : "--.", "H" : "....", "I" : "..", "J" : ".---", "K" : "-.-", "L" : ".-..",
"M" : "--", "N" : "-.", "O" : "---", "P" : ".--.", "Q" : "--.-", "R" : ".-.",
"S" : "...", "T" : "-", "U" : "..-", "V" : "...-", "W" : ".--", "X" : "-..-",
"Y" : "-.--", "Z" : "--..", "0" : "-----", "1" : ".----", "2" : "..---",
"3" : "...--", "4" : "....-", "5" : ".....", "6" : "-....", "7" : "--...",
"8" : "---..", "9" : "----.", "." : ".-.-.-", "?" : "..--..", "/" : "-..-.",
"," : "--..--", "!" : "-.-.--", "'" : ".----.", "\"" : ".-..-.", "(" : "-.--.",
")" : "-.--.-", "&" : ".-...", ":" : "---...", ";" : "-.-.-.", "_" : "..--.-",
"=" : "-...-", "+" : ".-.-.", "-" : "-....-", "$" : "...-..-", "@" : ".--.-",
"#" : "...-.-", " ":" "
}

def CwSecs(wpm,strg):
    global cw
    cwstr=""
    t=(1200.0/float(wpm))/1000.0
    #print('dit length is '+str(t))
    ee=0

    for xx in strg:
        if (cwstr != ""):
            cwstr=cwstr+" "
        cwstr=cwstr+cw[xx]

    for dd in cwstr:
        if dd == ".":
            ee=ee+2
        if dd == "-":
            ee=ee+4
        if dd == " ":
            ee=ee+3

    return((ee - 1) * t)

def ForwardBCD_Hex_to_Int(bh):
    # converts '01 23 45' to e.g. 12345
    qq=""   
    for ib in bh.split():
        qq=qq+ib
    iq=int(qq)
    return(iq)

def CI_Hex_to_Pct(strg):
   return int(int(strg.replace(' ',''))*100/255)

def Pct_to_CI_Hex(i):
    inth = int(256 * ( i / 100))
    # special case make 256 = 255
    if inth == 256:
       inth=255
    return " "+Int_to_ForwardBCD_Hex(inth,4)

def Int_to_ForwardBCD_Hex(i,mw):
    # converts int i=255 to (e.g.) '02 55' 
    ic=str(i)
    il=len(ic) % 2
    hd=""   
    if (il == 1):
        ic = "0" + ic
    while len(ic) < mw:
        ic = "00"+ic 
    for hexdig in wrap(ic,2):
        if (hd != ''): hd=hd+" "
        hd=hd+hexdig
    return(hd)

def Ascii_to_Hex(string):
    # converts ascii to hex e.g. 'CQ CQ' is 43 51 20 43 51
    retstr = ''
    for char in string: 
        if len(retstr) > 0: retstr=retstr+' '
        retstr=retstr+'{:02X}'.format(ord(char))
    return(retstr)

def StripCIV(rig_id_hex, ctl_id_hex, hexstr):
    if hexstr.find('FA FD') != -1:
      return 'FA'
    if hexstr.find('FB FD') != -1:
      return 'FB'
    #to = hexstr.find('FE FE '+rig_id_hex+' '+ctl_id_hex)
    #fm = hexstr.find('FE FE '+ctl_id_hex+' '+rig_id_hex)
    #fd = hexstr.find(' FD')
    #cmd=hexstr[ hexstr.find('FE FE '+rig_id_hex+' '+ctl_id_hex) +12: hexstr.find(' FD') ]
    return(hexstr[ hexstr.find('FE FE '+ctl_id_hex+' '+rig_id_hex) +len( hexstr[ hexstr.find('FE FE '+rig_id_hex+' '+ctl_id_hex) +12: hexstr.find(' FD') ])+13:-3])

def ByteArray_to_Hex(retbytes):
    # converts bytearray into hex digits e.g. b'\xff\xaa becomes 'FF AA' 
    retstr = ''
    for char in retbytes:
        if len(retstr) > 0: retstr=retstr+' '
        retstr=retstr+'{:02X}'.format(char)
    return(retstr)

def ReverseHex_to_BCD(hex):
    bcdstr=""
    for z in reversed(wrap(hex,2)):
        bcdstr=bcdstr+z
    return(bcdstr)

def Digits_to_ForwardBCD(digits):
    # converts ascii digits to bcd encoded byte array e.g. '121314' becomes b'\x12\x13\x14
    bcdstr = bytearray()
    for hexdig in wrap(digits,2):
        if hexdig!=' ':
            bcdstr.append(int(hexdig,16))
    return(bcdstr)

def Digits_to_ReverseBCD(digits):
    # converts ascii digits to bcd encoded byte array e.g. '121314' becomes b'\x14\x13\x12
    bcdstr = bytearray()
    for hexdig in reversed(wrap(digits,2)):
        if hexdig!=' ':
            bcdstr.append(int(hexdig,16))
    return(bcdstr)

def ReverseBCD_to_AsciiDigits(retbytes):
    # converts Reverse BCD to ascii digits b'\x14\x13\x12 becomes '121314'
    retstr = ''
    for char in reversed(retbytes):
        retstr=retstr+str((char >> 4))
        retstr=retstr+str((char & 0xF))
    return(retstr)

def ForwardBCD_to_AsciiDigits(retbytes):
    # converts Reverse BCD to ascii digits b'\x12\x13\x14 becomes '121314'
    retstr = ''
    for char in (retbytes):
        #retstr=retstr+str((char & 0xF))
        retstr=retstr+str((char >> 4))
        retstr=retstr+str((char & 0xF))
    return(retstr)

def ByteArray_to_HexDigits(retbytes):
    # converts Byte Array to ascii Hex digits b'\x14\x13\x12 becomes '14 13 12'
    retstr = ''
    for char in (retbytes):
        if (len(retstr) > 0):
           retstr=retstr+' '
        retstr=retstr+str((char >> 4))
        retstr=retstr+str((char & 0xF))
    return(retstr)

def KS_to_WPM(ks):
    # takes e.g. '02 55' and converts it to int, then applies the "CW Speed" formula to get int wpm
    global debuglevel
    qq=""
    #ks=GET('KEYSPEED')
    iq=ForwardBCD_Hex_to_Int(ks)
    wpm = int(round((( iq - 1) / (250 / 42)) + 6))
    return(wpm)

def WPM_to_KS(wpm):
    iwpm = round((wpm - 6) * 250 / 42 + 1)
    return(Int_to_ForwardBCD_Hex(iwpm,4))

global serport
global baud
global rigctld_host
global rigctld_port
global rigctld_use
global xml_key_type
global rig_id_hex
global ctl_id_hex
global BUTTONS
global SLIDERS
global METERS
global LON
global LOFF
global SEMI
global FULL
global SK
global FAKEBUG
global PADDLEKEYER
global BLACK
global GREEN

# **************************************************************
# CHANGE THESE VARS TO MATCH YOUR SET UP
# **************************************************************
#
# RIGCTLD IS THE BEST METHOD AND IS SHAREABLE WITH OTHER HAM
# APPS THAT USE RIGCTLD AT THE SAME TIME
#
rigctld_host='localhost'
rigctld_port=4532
rigctld_use=False

# CI-V
rig_id_hex='94'
ctl_id_hex='E0'

# SERIAL IS THE 2ND BEST METHOD BUT IT IS NOT SHAREABLE
# 

#portlist=serial.tools.list_ports.comports()
#for pp in portlist:
#	pd = pp.device
#	print (pd)
#	exit(1)

serport='/dev/ttyUSB0'
baud=115200


# **************************************************************
# END OF USER VAR SECTION
# **************************************************************

BLACK='#000000'
GREEN='#00ff00'

LON={}
LOFF={}
SEMI={}
FULL={}
SK={}
FAKEBUG={}
PADDLEKEYER={}

LON['00']=BLACK
LON['01']=GREEN

LOFF['00']=GREEN
LOFF['01']=BLACK
LOFF['02']=BLACK

SEMI['00']=BLACK
SEMI['01']=GREEN
SEMI['02']=BLACK

FULL['00']=BLACK
FULL['01']=BLACK
FULL['02']=GREEN

SK['00']=GREEN
SK['01']=BLACK
SK['02']=BLACK

FAKEBUG['00']=BLACK
FAKEBUG['01']=GREEN
FAKEBUG['02']=BLACK

PADDLEKEYER['00']=BLACK
PADDLEKEYER['01']=BLACK
PADDLEKEYER['02']=GREEN

BUTTONS=1
SLIDERS=2
METERS=4

import serial.tools.list_ports
from time import sleep
from tkinter import *
import xmlrpc.client
import serial
import socket
import sys

xml_key_type=2

def CwSecs(wpm,strg):
    global cw
    cwstr=""
    t=(1200.0/float(wpm))/1000.0
    #print('dit length is '+str(t))
    ee=0

    for xx in strg:
        if (cwstr != ""):
            cwstr=cwstr+" "
        cwstr=cwstr+cw[xx]

    for dd in cwstr:
        if dd == ".":
            ee=ee+2
        if dd == "-":
            ee=ee+4
        if dd == " ":
            ee=ee+3

    return((ee - 1) * t)

def SockOpen(rh, rp):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addr = (rigctld_host, rigctld_port)
        s.connect(addr)
        return(s)
        

def SerOpen():
#	portlist=serial.tools.list_ports.comports()
#	for pp in portlist:
#		pd = pp.device
#		print (pd)
        global serport

        ser=serial.Serial()
        ser.port=serport
        ser.baudrate=baud
        ser.timeout=1
        ser.parity=serial.PARITY_NONE
        ser.bytesize=serial.EIGHTBITS
        ser.stopbits=serial.STOPBITS_ONE
        ser.setDTR(False)
        ser.setRTS(False)
        ser.open()
        ser.setDTR(False)
        ser.setRTS(False)
        return(ser)

def SockSend(sock,*args):
    b=bytearray()
    for arg in args:
        b.extend(map(ord,arg))
    sock.sendall(b)

def SockRecv(sock):
    b=bytearray()
    amount_received=0
    while True:
        data=sock.recv(1)
        if (data == b'\n'):
            break
        b.extend(data)
    return(b)


def SerSend(ser,*args):
    ba=bytearray()
    for arg in args:
        for aa in arg.split():
            ba.append(int(aa[1:3],16))
    ser.write(bytes(ba))
    ser.flush()

def SerReceive(ser,*args):
    global rig_id_hex
    global ctl_id_hex
    rig_id=int(rig_id_hex,16);
    ctl_id=int(ctl_id_hex,16);
    send_preamble   =bytes([int('FE',16),int('FE',16),rig_id,ctl_id])
    receive_preamble=bytes([int('FE',16),int('FE',16),ctl_id,rig_id])
    suffix=bytes([int('FD',16)])
    rxbytes=bytearray()
    rr=0
    counter=0
    while True:
        input=ser.read()
        if input != b'': 
            rxbytes.append(int.from_bytes(input,byteorder='big'))   
        if receive_preamble in rxbytes: 
            rr=1;
        if input == suffix and rr == 1: 
            break
        if input == b'':
            counter=counter+1;
            if counter > 4: break
    return(rxbytes)

#def ByteArray_to_Hex(retbytes):
#    # converts bytearray into hex digits e.g. b'\xff\xaa becomes 'FF AA'
#    retstr = ''
#    for char in retbytes:
#        if len(retstr) > 0: retstr=retstr+' '
#        retstr=retstr+'{:02X}'.format(char)
#    return(retstr)

#def ForwardBCD_Hex_to_Int(bh):
#    # converts '01 23 45' to e.g. 12345
#    qq=""
#    for ib in bh.split():
#        qq=qq+ib
#    iq=int(qq)
#    return(iq)

def GetWPM(ksb):
    global debuglevel
    iq=ForwardBCD_Hex_to_Int(ByteArray_to_Hex(ksb))
    wpm = int(round((( iq - 1) / (250 / 42)) + 6))
    return(wpm)

#def get_next_or_prev_keytype(keytype, key_type_byte):
#    return('PSBPS'[key_type_byte+'V N'.index(keytype)])

def hamlibify(strg):
    return("w "+strg.replace(' ','').replace('x','\\0x')+"\n")

def hamlib_rigctld_switcher(key_switcher,cw_announce,cw_an,key_query,rigctld_host,rigctld_port,keytype):
    print ("in hamlib_rigctld_switcher")
    h_key_switcher=hamlibify(key_switcher)
    h_cw_announce=hamlibify(cw_announce)
    h_key_query=hamlibify(key_query)

    s=SockOpen(rigctld_host, rigctld_port)
    print ("after sockopen")

    if (keytype in 'SBPVN'):
        md="RPRT -999"
        while "RPRT -" in str(md):
            SockSend(s, "m\n")
            md=SockRecv(s).decode()
            if "RPRT -" not in str(md):
           	    wid=SockRecv(s).decode()
    
    
        if (str(md) != 'CW'):
            SockSend(s,"M CW 0\n")
            dummy=SockRecv(s).decode()
    
        SockSend(s,"l KEYSPD\n")
        key_speed=SockRecv(s).decode()
    
        SockSend(s,"u SBKIN\n")
        break_in=SockRecv(s).decode()
        print("Break In is "+str(break_in))
    
        SockSend(s,"U SBKIN 0\n")
        dummy=SockRecv(s)
    
        SockSend(s,h_cw_announce)
        dummy=SockRecv(s)
    
        sleep(CwSecs(key_speed,cw_an))
    
        if (str(break_in) == "0"):
            SockSend(s,"U FBKIN 0\n")
            SockSend(s,"U SBKIN 0\n")
    
        if (str(break_in) == "1"):
            SockSend(s,"U SBKIN 1\n")
    
        if (str(break_in) == "2"):
            SockSend(s,"U FBKIN 1\n")
    
        dummy=SockRecv(s)

    SockSend(s,h_key_switcher)
    print ("h key switcher is " + str(h_key_switcher))
    dummy=SockRecv(s)

    s.close()
    print("switched via hamlib rigctld")
    return dummy

def serial_switcher(key_query,keytype,key_speed_query,break_in_query,pfx,break_in_sub,suf,cw_announce,cw_an,key_switcher,mode_query,mode_set_cw):
    print ("in serial switcher")
    ser=SerOpen()

    if (keytype in 'tog_key_sk tog_key_fakebug tog_key_paddle'):
        SerSend(ser,mode_query)
        print("ser mode query sent")
        md=SerReceive(ser)
        print(str(md[-3]))
    
        if(str(md[-3]) != "3"):
            SerSend(ser,mode_set_cw)
            guzuta=SerReceive(ser)
    
        if (keytype in 'NV'):
            SerSend(ser,key_query)
            key_type=SerReceive(ser)
            key_type_byte=key_type[-2]
            setkey(get_next_or_prev_keytype(keytype,key_type_byte))
            return
    
    
        SerSend(ser,key_speed_query)
        key_speed=SerReceive(ser)
        key_speed_bytes=key_speed[-3:-1]
        wpm=GetWPM(key_speed_bytes)
    
        SerSend(ser,break_in_query)
        break_in=SerReceive(ser)
        break_in_byte=break_in[-2]
    
        SerSend(ser,pfx+break_in_sub+" x00"+suf)
        dummy=SerReceive(ser)
    
        SerSend(ser,cw_announce)
        dummy=SerReceive(ser)
    
        sleep(CwSecs(wpm,cw_an))
    
        bib=" x0"+str(break_in_byte)
        SerSend(ser,pfx+break_in_sub+bib+suf)
        dummy=SerReceive(ser)

    SerSend(ser,key_switcher)
    dummy=SerReceive(ser)

    ser.close()
    print("switched via serial")
    return dummy

def ErrHan(er):
    print (type(er))
    print (er.args)
    print (er)

def Quitter(*args):
    root.destroy()

def getslider(event,op):
   thing=(op+str(event.widget.get()).replace(' ',''))
   print(thing)
   setkey(op+str(event.widget.get()).replace(' ',''))

def setkey(keytype):
    global baud
    global host
    global xml_key_type
    global rigctld_use
    global BUTTONS
    global SLIDERS
    global METERS

    if (keytype == 'tog_key_sk'):
        ks_c="00"
        cw_an="S"
        xml_key_type=0
    if (keytype == 'tog_key_fakebug'):
        ks_c="01"
        cw_an="B"
        xml_key_type=1
    if (keytype == 'tog_key_paddle'):
        ks_c="02"
        cw_an="P"
        xml_key_type=2
    if (keytype not in 'tog_key_sk tog_key_fakebug tog_key_paddle'):
        ks_c="na"
        cw_an="E"  # just gets ignored

    powerpfx = "xfe "*150
    pfx="xfe xfe x94 xe0 "
    rpfx="xfe xfe x0 x94 "
    suf=" xfd"
    key_speed_query=    pfx+"x14 x0c"+suf
    key_query=          pfx+"x1a x05 x01 x64"+suf
    key_switcher=       pfx+"x1a x05 x01 x64 x"+ks_c+suf
    cw_announce=        pfx+"x17 x"+'{:02X}'.format(ord(cw_an))+suf
    break_in_sub=       "x16 x47"
    break_in_query=     pfx+break_in_sub+suf
    mode_query=         pfx+"x04"+suf
    mode_set_cw=        pfx+"x06 x03"+suf

    if (keytype == 'query_key_type'):
        key_switcher = pfx + ' x1a x05 x01 x64 ' + suf

    # POWER
    if (keytype == 'tog_pwr_off'):
        key_switcher = pfx + ' x18 x00 ' + suf
    if (keytype == 'tog_pwr_on'):
        key_switcher = powerpfx + pfx + ' x18 x01 ' + suf

    # NR
    if (keytype == 'query_tog_nr'):
        key_switcher = pfx + ' x16 x40 ' + suf
    if (keytype == 'tog_nr_off'):
        key_switcher = pfx + ' x16 x40 x00 ' + suf
    if (keytype == 'tog_nr_on'):
        key_switcher = pfx + ' x16 x40 x01 ' + suf

    # NB
    if (keytype == 'query_tog_nb'):
        key_switcher = pfx + ' x16 x22 ' + suf
    if (keytype == 'tog_nb_off'):
        key_switcher = pfx + ' x16 x22 x00 ' + suf
    if (keytype == 'tog_nb_on'):
        key_switcher = pfx + ' x16 x22 x01 ' + suf
        
    # BKIN
    if (keytype == 'query_tog_bkin'):
        key_switcher = pfx + ' x16 x47 ' + suf
    if (keytype == 'tog_bkin_off'):
        key_switcher = pfx + ' x16 x47 x00 ' + suf
    if (keytype == 'tog_bkin_semi'):
        key_switcher = pfx + ' x16 x47 x01 ' + suf
    if (keytype == 'tog_bkin_full'):
        key_switcher = pfx + ' x16 x47 x02 ' + suf

    if (keytype == 'query_level_af'):
        key_switcher = pfx + ' x14 x01 ' + suf
    if (keytype[0:8] == 'level_af'):
        iis=int(keytype.replace('level_af',''))
        pci=Pct_to_CI_Hex(iis).replace(' ',' x')
        key_switcher = pfx + ' x14 x01 ' + pci + suf

    if (keytype == 'query_level_rf'):
        key_switcher = pfx + ' x14 x02 ' + suf
    if (keytype[0:8] == 'level_rf'):
        iis=int(keytype.replace('level_rf',''))
        pci=Pct_to_CI_Hex(iis).replace(' ',' x')
        key_switcher = pfx + ' x14 x02 ' + pci + suf

    if (keytype == 'query_level_sql'):
        key_switcher = pfx + ' x14 x03 ' + suf
    if (keytype[0:9] == 'level_sql'):
        iis=int(keytype.replace('level_sql',''))
        pci=Pct_to_CI_Hex(iis).replace(' ',' x')
        key_switcher = pfx + ' x14 x03 ' + pci + suf

    if (keytype == 'query_level_pwr'):
        key_switcher = pfx + ' x14 x0a ' + suf
    if (keytype[0:9] == 'level_pwr'):
        iis=int(keytype.replace('level_pwr',''))
        pci=Pct_to_CI_Hex(iis).replace(' ',' x')
        key_switcher = pfx + ' x14 x0a ' + pci + suf

    if (keytype == 'query_level_nr'):
        key_switcher = pfx + ' x14 x06 ' + suf
    if (keytype[0:8] == 'level_nr'):
        iis=int(keytype.replace('level_nr',''))
        pci=Pct_to_CI_Hex(iis).replace(' ',' x')
        key_switcher = pfx + ' x14 x06 ' + pci + suf

    if (keytype == 'query_level_if_inner'):
        key_switcher = pfx + ' x14 x07 ' + suf
    if (keytype[0:14] == 'level_if_inner'):
        iis=int(keytype.replace('level_if_inner',''))
        pci=Pct_to_CI_Hex(iis).replace(' ',' x')
        key_switcher = pfx + ' x14 x07 ' + pci + suf

    if (keytype == 'query_level_if_outer'):
        key_switcher = pfx + ' x14 x08 ' + suf
    if (keytype[0:14] == 'level_if_outer'):
        iis=int(keytype.replace('level_if_outer',''))
        pci=Pct_to_CI_Hex(iis).replace(' ',' x')
        key_switcher = pfx + ' x14 x08 ' + pci + suf

    # determine if hamlib or serial - try hamlib first

    if (keytype != 'tog_pwr_on' and rigctld_use ):
        try:
            rts=hamlib_rigctld_switcher(key_switcher,cw_announce,cw_an,key_query,rigctld_host,rigctld_port,keytype)
            if 'query' not in keytype:
               if keytype[0:4]=='tog_':
                  pollstuff(BUTTONS)
               if keytype[0:6]=='level_':
                  pollstuff(SLIDERS)
            return(rts)

        except ConnectionRefusedError as ex:
            print("did not connect via rigctld... next...")

        except Exception as ex:
            ErrHan(ex)

    try:
        rts=serial_switcher(key_query,keytype,key_speed_query,break_in_query,pfx,break_in_sub,suf,cw_announce,cw_an,key_switcher,mode_query,mode_set_cw)
        if 'query' not in keytype:
           if keytype=='tog_pwr_off':
              exit()
           if keytype=='tog_pwr_on':
              root.after(1000,pollstuff(255))
              return('')
           if keytype[0:4]=='tog_':
              pollstuff(BUTTONS)
           if keytype[0:6]=='level_':
              pollstuff(SLIDERS)

        return(rts)

    except serial.serialutil.SerialException as ex:
        print("did not connect via serial... that's the last try!")
        
    except Exception as ex:
        ErrHan(ex)
        print(sys.exc_info())

def poweron():
    setkey('tog_pwr_on')

def get_0255_bcd_val(setkeyval):
    return CI_Hex_to_Pct(StripCIV(rig_id_hex,ctl_id_hex,ByteArray_to_Hex(setkey(setkeyval))))

def get_FF_bcd_val(setkeyval):
    return StripCIV(rig_id_hex,ctl_id_hex,ByteArray_to_Hex(setkey(setkeyval)))


def pollstuff(items):
    global BUTTONS
    global SLIDERS
    global METERS
    global BLACK 
    global GREEN 
    global LON 
    global LOFF 
    global SEMI 
    global FULL
    global SK
    global FAKEBUG
    global PADDLEKEYER
    global rig_id_hex
    global ctl_id_hex

    print ('items ' + str(items))
    # some dang hard coding here
    if (BUTTONS & items):
       print('doing buttons')
#       print ("KEY TYPE is "+key_tp)

       key_tp=get_FF_bcd_val('query_key_type')
       nr_tog=get_FF_bcd_val('query_tog_nr')
       nb_tog=get_FF_bcd_val('query_tog_nb')
       bkin_tog=get_FF_bcd_val('query_tog_bkin')

       tog_nr_on.configure(fg=LON[nr_tog],activeforeground=LON[nr_tog])
       tog_nr_off.configure(fg=LOFF[nr_tog],activeforeground=LOFF[nr_tog])

       tog_nb_on.configure(fg=LON[nb_tog],activeforeground=LON[nb_tog])
       tog_nb_off.configure(fg=LOFF[nb_tog],activeforeground=LOFF[nb_tog])

       tog_bkin_full.configure(fg=FULL[bkin_tog],activeforeground=FULL[bkin_tog])
       tog_bkin_semi.configure(fg=SEMI[bkin_tog],activeforeground=SEMI[bkin_tog])
       tog_bkin_off.configure(fg=LOFF[bkin_tog],activeforeground=LOFF[bkin_tog])

       tog_key_sk.configure(fg=SK[key_tp],activeforeground=SK[key_tp])
       tog_key_fakebug.configure(fg=FAKEBUG[key_tp],activeforeground=FAKEBUG[key_tp])
       tog_key_paddlekeyer.configure(fg=PADDLEKEYER[key_tp],activeforeground=PADDLEKEYER[key_tp])

    if (SLIDERS & items):
       print('doing sliders')
       level_af.set(get_0255_bcd_val('query_level_af'))
       level_rf.set(get_0255_bcd_val('query_level_rf'))
       level_sql.set(get_0255_bcd_val('query_level_sql'))
       level_pwr.set(get_0255_bcd_val('query_level_pwr'))
       level_nr.set(get_0255_bcd_val('query_level_nr'))
       level_if_inner.set(get_0255_bcd_val('query_level_if_inner'))
       level_if_outer.set(get_0255_bcd_val('query_level_if_outer'))


root=Tk()

tog_key_sk          = Button(root, text="Straight",   justify="center", width=6, command=lambda: setkey('tog_key_sk'))
tog_key_fakebug     = Button(root, text="Bug",        justify="center", width=6, command=lambda: setkey('tog_key_fakebug'))
tog_key_paddlekeyer = Button(root, text="Paddle",     justify="center", width=6, command=lambda: setkey('tog_key_paddle'))

cmd_quit          = Button(root, text="Quit",       justify="center", width=6, command=exit)

tog_bkin_full       = Button(root, text="BK-In Full", justify="center", width=6, command=lambda: setkey('tog_bkin_full'))
tog_bkin_semi       = Button(root, text="BK-In Semi", justify="center", width=6, command=lambda: setkey('tog_bkin_semi'))
tog_bkin_off        = Button(root, text="BK-In Off",  justify="center", width=6, command=lambda: setkey('tog_bkin_off'))

tog_nb_on           = Button(root, text="NB On",      justify="center", width=6, command=lambda: setkey('tog_nb_on'))
tog_nb_off          = Button(root, text="NB Off",     justify="center", width=6, command=lambda: setkey('tog_nb_off'))

tog_nr_on           = Button(root, text="NR On",      justify="center", width=6, command=lambda: setkey('tog_nr_on'))
tog_nr_off          = Button(root, text="NR Off",     justify="center", width=6, command=lambda: setkey('tog_nr_off'))

tog_pwr_on          = Button(root, text="Power On",   justify="center", width=6, command=lambda: setkey('tog_pwr_on'))
tog_pwr_off         = Button(root, text="Power Off",  justify="center", width=6, command=lambda: setkey('tog_pwr_off'))

level_af          = Scale(root,from_=100,to=0,orient=VERTICAL)
level_rf          = Scale(root,from_=100,to=0,orient=VERTICAL)
level_sql         = Scale(root,from_=100,to=0,orient=VERTICAL)
level_pwr         = Scale(root,from_=100,to=0,orient=VERTICAL)
level_nr          = Scale(root,from_=100,to=0,orient=VERTICAL)
level_if_inner    = Scale(root,from_=100,to=0,orient=VERTICAL)
level_if_outer    = Scale(root,from_=100,to=0,orient=VERTICAL)

label_af          = Label(root,text="Vol")
label_rf          = Label(root,text="RF")
label_sql         = Label(root,text="Sql")
label_pwr         = Label(root,text="Pwr")
label_nr          = Label(root,text="NR")
label_if_inner    = Label(root,text="IF Inner")
label_if_outer    = Label(root,text="IF Outer")

cc=1
tog_key_sk.grid(row=1,column=cc)

cc=cc+1
tog_key_fakebug.grid(row=1,column=cc)
cmd_quit.grid(row=2,column=cc)

cc=cc+1
tog_key_paddlekeyer.grid(row=1,column=cc)

cc=cc+1
tog_bkin_full.grid(row=1,column=cc)
tog_bkin_semi.grid(row=2,column=cc)
tog_bkin_off.grid (row=3,column=cc)

cc=cc+1
level_af.grid(row=2,rowspan=3,column=cc)
label_af.grid(row=1,column=cc)
level_af.bind("<ButtonRelease-1>",lambda event, aa='level_af': getslider(event,aa))

cc=cc+1
level_rf.grid(row=2,rowspan=3,column=cc)
label_rf.grid(row=1,column=cc)
level_rf.bind("<ButtonRelease-1>",lambda event, aa='level_rf': getslider(event,aa))

cc=cc+1
level_sql.grid(row=2,rowspan=3,column=cc)
label_sql.grid(row=1,column=cc)
level_sql.bind("<ButtonRelease-1>",lambda event, aa='level_sql': getslider(event,aa))

cc=cc+1
level_pwr.grid(row=2,rowspan=3,column=cc)
label_pwr.grid(row=1,column=cc)
level_pwr.bind("<ButtonRelease-1>",lambda event, aa='level_pwr': getslider(event,aa))

cc=cc+1
level_nr.grid(row=2,rowspan=3,column=cc)
label_nr.grid(row=1,column=cc)
level_nr.bind("<ButtonRelease-1>",lambda event, aa='level_nr': getslider(event,aa))

cc=cc+1
level_if_inner.grid(row=2,rowspan=3,column=cc)
label_if_inner.grid(row=1,column=cc)
level_if_inner.bind("<ButtonRelease-1>",lambda event, aa='level_if_inner': getslider(event,aa))

cc=cc+1
level_if_outer.grid(row=2,rowspan=3,column=cc)
label_if_outer.grid(row=1,column=cc)
level_if_outer.bind("<ButtonRelease-1>",lambda event, aa='level_if_outer': getslider(event,aa))

cc=cc+1
tog_nb_on.grid(row=1,column=cc)
tog_nb_off.grid(row=2,column=cc)

cc=cc+1
tog_nr_on.grid(row=1,column=cc)
tog_nr_off.grid(row=2,column=cc)

cc=cc+1
tog_pwr_on.grid(row=1,column=cc)
tog_pwr_off.grid(row=2,column=cc)


root.bind("<Escape>",Quitter)
root.bind("<Control-w>",Quitter)
root.protocol("WM_DELETE_WINDOW", Quitter)
root.title("ICOM IC-7300 Key Switcheroonie")
# pollstuff()
root.after(200,poweron)
#root.after(2000,pollstuff)
root.mainloop()

