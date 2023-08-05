from setuptools import setup
setup(
    name='twincharm',
    packages=['twincharm.client.udp','twincharm.server.udp','twincharm.response'
    ],
    author='Adam Jenča',
    author_email='jenca.a@gjh.sk',
    version='1.0.1',
    url='https://github.com/jenca-adam',
    description='Simple socket server and client creator',
    long_description='''Simple socket server and client creator.
    Only UDP support for now.
    Example code:
    Server:
    from twincharm.server.udp import Server
    server=Server(('127.0.0.1',8391))#make new server listening on port 8391
    @server.function
    def hello(request,addr):
    return b'Hello world'#if request is 'hello' return response 'Hello world'
    server.run()
    Client:
    from twincharm.client.udp import Client
    client=Client()#create new client object
    client.pair(('127.0.0.1',8391))#pair with server
    client.hello()#should return b'Hello world'
        ''',
 
   ) 
