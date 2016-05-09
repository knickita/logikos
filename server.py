#!/usr/bin/python
import random
import database
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

PORT_NUMBER = 8080

def generate_hash():
    out=""
    for i in range(10):
        out+=chr(random.randint(98,122))
    return out

def newHash():
    new_hash=generate_hash()
    while new_hash in database.hashes.keys():
        new_hash=generate_hash()

    database.hashes[new_hash]=None
    return new_hash


def change(user,title,new_value):
    if title[:6]=="titolo":
        line_number=int(title[6:])
        if database.get_lavoro(line_number).responsabile==user:
            if not database.exist_event(user,new_value):
                database.get_lavoro(line_number).titolo=new_value
        return "$(\"#"+title+"\").val(\""+database.get_lavoro(line_number).titolo+"\");"
    elif title[:12]=="responsabile":
        line_number=int(title[12:])
        return "$(\"#"+title+"\").val(\""+database.get_lavoro(line_number).responsabile+"\");"
    elif title[:6]=="inizio":
        line_number=int(title[6:])
        if database.get_lavoro(line_number).responsabile==user:
            database.get_lavoro(line_number).inizio=new_value
        return "$(\"#"+title+"\").val(\""+database.get_lavoro(line_number).inizio+"\");"
    elif title[:4]=="fine":
        line_number=int(title[4:])
        if database.get_lavoro(line_number).responsabile==user:
            database.get_lavoro(line_number).fine=new_value
        return "$(\"#"+title+"\").val(\""+database.get_lavoro(line_number).fine+"\");"
    elif title[:9]=="personale":
        line_number=int(title[9:])
        return "$(\"#"+title+"\").val(\""+database.get_lavoro(line_number).personale_to_str()+"\");"

    return ""


class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path[:7]=="/random":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            data_query = self.path[8:].split("&")
            data={}
            for d in data_query:
                c=d.split("=")
                data[c[0]]=c[1]
            if data["contest"]=="login":
                if data["user"] in database.users.keys():
                    if data["value"]==database.users[data["user"]]:
                        for key in database.hashes.keys():
                            if database.hashes[key]==data["user"]:
                                del database.hashes[key]
                        hash_id=newHash()
                        database.hashes[hash_id]=data["user"]
                        self.wfile.write("user_hash=\""+hash_id+"\";")
                        self.wfile.write("document.cookie = \"username="+data["user"]+"\";")
                        self.wfile.write("document.cookie = \"hash="+hash_id+"\";")
                        self.wfile.write("window.location=\"global.html\";")
                        return                    

                self.wfile.write("alert(\"nome utente o password errati\")")
            elif data["hash"] in database.hashes.keys():
                if data["user"]==database.hashes[data["hash"]]:
                    if data["contest"]=="global":
                        if data["action"]=="update":
                            self.wfile.write("$(\"#table1\").empty();")
                            self.wfile.write("$(\"#table1\").append(\""+database.get_global_to_html()+"\");")
                            return
                        elif data["action"]=="remove":
                            if database.get_lavoro(int(data["line"])).responsabile==data["user"]:
                                database.elimina_lavoro(int(data["line"]))
                                #update
                                self.wfile.write("$(\"#table1\").empty();")
                                self.wfile.write("$(\"#table1\").append(\""+database.get_global_to_html()+"\");")
                            return
                        elif data["action"]=="change":
                            response=change(data["user"],data["id"],data["value"])
                            self.wfile.write(response)
                        elif data["action"]=="aggiungi_tecnico":
                            if database.get_lavoro(int(data["line"])).responsabile==data["user"]:
                                if not data["value"] in database.get_lavoro(int(data["line"])).personale:
                                    database.get_lavoro(int(data["line"])).personale.append(data["value"])
                            self.wfile.write("$(\"#personale"+data["line"]+"\").val(\""+database.get_lavoro(int(data["line"])).personale_to_str()+"\");")
                        elif data["action"]=="new_event":
                            if database.exist_event(data["user"],data["value"]):
                                self.wfile.write("alert(\"Esiste un altro evento di "+data["user"]+" chiamato: "+data["value"]+"\");")
                            else:
                                database.lavori.append(database.Lavoro(data["value"],data["user"],"today","today",[]))
                                self.wfile.write("location.reload();")
                    elif data["contest"]=="tecnici":
                        if data["action"]=="update":
                            self.wfile.write("$(\"#table1\").empty();")
                            self.wfile.write("$(\"#table1\").append(\""+database.get_schermata_tecnici_to_html()+"\");")
                            return
        elif self.path=="/":
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            in_file=open("index.html","r")
            data = in_file.read()
            in_file.close()
            # Send the html message
            self.wfile.write(data)
        else:
            test=self.path.split(".")[-1]
            try:
                self.send_response(200)
                if test=="css":
                    self.send_header('Content-type','text/css')
                elif test=="png":
                    self.send_header('Content-type','image/png')
                else:
                    self.send_header('Content-type','text/html')
                
                self.end_headers()
                if test=="png":
                    in_file=open(self.path[1:],"rb")
                else:
                    in_file=open(self.path[1:],"r")
                data = in_file.read()
                in_file.close()
                # Send the html message
                self.wfile.write(data)
            except:
                self.wfile.write("file not found")


try:
    #Create a web server and define the handler to manage the
    #incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ' , PORT_NUMBER
    
    #Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()