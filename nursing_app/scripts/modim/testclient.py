from ws_client import *

# export MODIM_IP=<modim server IP>

q = ModimWSClient()
q.cconnect()
q.csend("im.logenable(True)")
q.csend("im.setDemoPath('../../demo/sample')")
q.csend("im.execute('welcome')")



