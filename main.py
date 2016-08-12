from database import *
from filesystem import *
import ugfx
import buttons
import stm
import http_client
import wifi
import ujson
#from imu import IMU
import network
#import micropython
import gc
import socket
import pyb
import http_client

def load_resources_1():
  ugfx.clear(ugfx.BLACK);
  ugfx.set_default_font(ugfx.FONT_SMALL)
  ugfx.text(5, 5, "Connecting...", ugfx.WHITE)
  if (not wifi.nic().is_connected()):
    wifi.connect(True)
  ugfx.clear(ugfx.BLACK);
  ugfx.text(5, 5, "Loading resources... (1/3)", ugfx.WHITE)
  r1 = stm.mem32[0x1FFF7590]
  r2 = stm.mem32[0x1FFF7594]
  r3 = stm.mem32[0x1FFF7598]
  name = database_get("display-name", "UNKN")
  urlparams = "r1="+str(r1)+"&r2="+str(r2)+"&r3="+str(r3)+"&name="+name
  needlist = True
  while(needlist):
    #try:
    ugfx.text(5, 15, "Requesting...", ugfx.WHITE)
    with http_client.post('http://rnpl.us/emf/nyancat.php', urlencoded=urlparams) as resp:
      needlist = False
      ugfx.text(5, 30, "Storing result...", ugfx.WHITE)
      listfile = open("apps/renze~nyancat/list.json",'w')
      listfile.write(resp.text)
      listfile.close()
      #recf = ujson.loads(resp.text)
    #except:
    #  print("Failed")
    ugfx.text(5, 50, "Stage 1 OK", ugfx.WHITE)

  
def load_resources_2():
  ugfx.clear(ugfx.BLACK);
  ugfx.text(5, 5, "Loading resources... (2/3)", ugfx.WHITE)

  s=socket.socket()
  s.connect(socket.getaddrinfo('rnpl.us',80)[0][4])
  s.send("GET /emf/nyanres.php HTTP/1.1\r\nHost:rnpl.us\r\nConnection: close\r\n\r\n")
  buf = s.recv(100)
  outfile = open("apps/renze~nyancat/nyanres",'w')
  h1 = 0
  h2 = 0
  h3 = 0
  h4 = 0
  header = True
  headers = ""

  #while ((len(buf) > 0) and (header)):
  #  while (len(buf) > 0):
  #    if (h1=="\r") and (h2=="\n") and (h3=="\r") and (h4=="\n"):
  #      header = False
  #    else:
  #      h1 = h2
  #      h2 = h3
  #      h3 = h4
  #      h4 = buf
  #      headers = headers+chr(buf[0])
  #      buf = buf[1:]
  #  buf = s.recv(100)
  #ugfx.text(5, 35, "Header found.", ugfx.WHITE)
  #      
  #print("Headers: "+headers)
  buf = s.recv(512)
  ncnt = 0
  while (len(buf) > 0):
    print("Searching: "+str(buf[0]))
    if(buf[0]==10):
      ncnt = ncnt + 1
      print("FOUND "+str(ncnt))
    buf = buf[1:]
    if(ncnt>=5):
      break;
  print("OK")
  print(buf)
  pyb.delay(2000)
  while len(buf) > 0:
    a = outfile.write(buf)
    buf = s.recv(512)
    print("Loading nyanres: "+str(a)+" / "+str(len(buf)))
    pyb.delay(5)
    gc.collect()
  outfile.close()
  s.close()

def unpack_resources():
    ugfx.clear(ugfx.BLACK)
    ugfx.set_default_font(ugfx.FONT_SMALL)
    ugfx.text(5, 5, "Unpacking files...", ugfx.WHITE)
    with open("apps/renze~nyancat/list.json") as f:
      w = json.loads(f.read())
    pack = open("apps/renze~nyancat/nyanres")
    for i in range(0,len(w)):
      fname = w["file"+str(i)]["name"]
      fsize = w["file"+str(i)]["size"]
      print(fname)
      outfile = open(fname, 'w')
      srem = fsize
      ugfx.clear(ugfx.BLACK)
      ugfx.set_default_font(ugfx.FONT_SMALL)
      ugfx.text(5, 5, "Unpacking file "+str(i)+"...", ugfx.WHITE)
      print("Unpacking "+fname+"' ("+str(fsize)+")...")
      while (srem>0):
        srem = srem - outfile.write(pack.read(1))
        print("Remaining: "+str(srem))
    outfile.close()
    pack.close()
    ugfx.clear(ugfx.GREEN)
    ugfx.set_default_font(ugfx.FONT_SMALL)
    ugfx.text(5, 5, "DONE", ugfx.WHITE)
    os.remove("apps/renze~nyancat/nyanres")
    pyb.delay(1000)

if not "nyancat.py" in os.listdir("apps/renze~nyancat"):
  try:
    load_resources_1()
    load_resources_2()
    unpack_resources()
  except:
    try:
      os.remove("apps/renze~nyancat/nyancat.py")
    except:
      print("e_rm")
    ugfx.clear(ugfx.BLACK)
    ugfx.set_default_font(ugfx.FONT_SMALL)
    ugfx.text(5, 5, "Error, please restart (1).", ugfx.WHITE)
    while(True):
      dummy=True

try:
  mod = __import__("apps/renze~nyancat/nyancat.py")
  if "main" in dir(mod):
    print("OK")
    mod.main()
  else:
    ugfx.clear(ugfx.BLACK)
    ugfx.set_default_font(ugfx.FONT_SMALL)
    ugfx.text(5, 5, "Error, please restart (2).", ugfx.WHITE)
    try:
      os.remove("apps/renze~nyancat/nyancat.py")
    except:
      dummy=True
except:
    ugfx.clear(ugfx.BLACK)
    ugfx.set_default_font(ugfx.FONT_SMALL)
    ugfx.text(5, 5, "Error, please restart (3).", ugfx.WHITE)
    try:
      os.remove("apps/renze~nyancat/nyancat.py")
    except:
      dummy=True

while(True):
  dummy=True