import ugfx

period = 5 * 1000
needs_icon = True

mod = False

def tick(icon):
  global mod
  try:
    if (mod==False):
      mod = __import__("iloveyou.py")
    if "main" in dir(mod):
      mod.main()
    else:
      mod = False
  except:
    dummy=True
  return False
