'''import http.client

conn = http.client.HTTPConnection("ifconfig.me")
conn.request("GET", "/ip")
a = conn.getresponse().read()'''

info = {
    'addr': '127.0.0.1', # a,
    'port': 8022,
    'users': 5
}
# print(a)