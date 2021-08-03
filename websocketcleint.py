
from websocket import create_connection

import pygame,base64,cv2,threading,json,asyncio,websockets,random
import numpy as np


def connect(url,port):
    ws = create_connection("ws://"+str(url)+":"+str(port))
    ws.send("Hello, World")
    result = ws.recv()
    ws.close()
    im_bytes = base64.b64decode(result.decode("utf-8"))
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    return img

def main():
    
    while True:

        img=connect("8.tcp.ngrok.io",17451)
        # if img!=None:
        cv2.imshow("img",img)
        if cv2.waitKey(25) & 0xFF==ord("q"):
                cv2.destroyAllWindows()
                print("bitti")
                break


if __name__ == '__main__':
    main()
    