"""
loop dosyası içerisinde raspberry pi programımızın akışı sağlanacaktır..
resimler webSocketsOpencvServer üzerinden akışı sağlanacaktır..
roboSocketCom üzerinden pyserial kütüphanesi sayesinde verilerimizin akışı mikrokontrolcüye gidecektir.
"""
import socket,threading,_thread,asyncio
from webSocketsOpencvServer import WebSocketsOpencvServer
from Adafruit_IO import Client, RequestError, Feed

from pyngrok import ngrok,conf

def log_event_callback(log):
    print(str(log))

async def roboRUN(serverHost,roboOpencvServerPort,loop):
    roboOpencv = WebSocketsOpencvServer(serverHost=serverHost, serverPort=roboOpencvServerPort, camId=0)

    t1 = loop.create_task(roboOpencv.socketRun())


    await t1

def mainLoop():

    ADAFRUIT_IO_KEY = 'your adafruit key'
    ADAFRUIT_IO_USERNAME = 'your adafruit io username'
    aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
    "----------------------------"
    serverHost="0.0.0.0"
    roboOpencvServerPort=5000
    "---------------------------"
    loop = asyncio.get_event_loop()
    # cihazın isimini çekiyoruz
    hostname = socket.gethostname()
    # cihazın ip adresini çekiyoruz
    ip_address = socket.gethostbyname(hostname)
    pyngrok_config = conf.PyngrokConfig(log_event_callback=log_event_callback,
                                    max_logs=10)
    conf.set_default(pyngrok_config)

    ngrok.set_auth_token("1v3LW7Iod4hdphvksXxLYqCL5qf_35sgSpT6RumaGNu8z4cNS")

    # Open a ngrok tunnel to the socket
    public_url = ngrok.connect(roboOpencvServerPort,"tcp").public_url
    # print("ngrok tunnel \"{}\" -> \"tcp://127.0.0.1:{}/\"".format(public_url, roboOpencvServerPort))

    ssh_url, port = public_url.strip("tcp://").split(":")
    print(f" * ngrok tunnel available, access with `ssh root@{ssh_url} -p{port}`")
    "-------------------------"

    try:
        server_url = aio.feeds('server-url')
    except RequestError: # Doesn't exist, create a new feed
        feed = Feed(name="server-url")
        server_url = aio.create_feed(feed)
    
    try:
        server_port = aio.feeds('server-port')
    except RequestError: # Doesn't exist, create a new feed
        feed = Feed(name="server-port")
        server_port = aio.create_feed(feed)
    
    aio.send_data(server_url.key, str(ssh_url))
    aio.send_data(server_port.key, str(port))
    
    # print(ip_address)
    loop.run_until_complete(roboRUN(serverHost, roboOpencvServerPort,loop))
    loop.run_forever()
    # loop.run_until_complete(roboRUN(serverHost, roboServerPort, roboOpencvServerPort))
if __name__ == '__main__':
    mainLoop()
