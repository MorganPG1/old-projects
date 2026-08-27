import linkboy
import logging
linkboy.l = logging.getLogger()
logging.basicConfig(filename='myapp.log', level=logging.INFO)

l1 = linkboy.LinkDevice()
l2 = linkboy.LinkDevice()

link = linkboy.Link(l1, l2)

for i in range(0,256):
    link.SendByte(l1, i)
    link.SendByte(l2, i)
    for i in range(0,8):
        link.step()
