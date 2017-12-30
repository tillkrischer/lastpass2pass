from subprocess import Popen, PIPE
from urllib.parse import urlparse

f = open("lastpass.csv", "r")

data = {}

for line in f:
    url,username,password,extra,name,grouping,fav = line.split(',')
    o = urlparse(url)
    urlstring = "{}://{}".format(o.scheme, o.netloc)
    domain = o.netloc
    if not domain:
        domain = "(nodomain)"
    if not domain in data:
        data[domain] = {}
        data[domain]["entry"] = ""
        if username:
            data[domain]["name"] = username
        elif name:
            data[domain]["name"] = name
        else:
            data[domain]["name"] = domain

    entry = []
    entry.append(password)
    entry.append("\n")
    entry.append("---")
    entry.append("\n")
    if name:
        entry.append(name)
        entry.append("\n")
    if username:
        entry.append("username: {}".format(username))
        entry.append("\n")
    if o.netloc:
        entry.append("url: {}".format(urlstring))
        entry.append("\n")
    entry.append("\n")
    entry.append("\n")
    
    data[domain]["entry"] += "".join(entry)


for key in data:
    filename = "{}/{}".format(key, data[key]["name"])
#    print("filename: {}".format(filename))
#    print(data[key]["entry"])

    p = Popen(['pass', 'insert', '-m', filename], stdin=PIPE, stdout=PIPE)
    p.communicate(bytes(data[key]["entry"], 'utf-8'))
    p.stdin.close()
