import random
import os
import datetime
class Lavoro():
	id_count=0
	def __init__(self,titolo,responsabile,inizio,fine,personale):
		self.titolo=titolo
		self.responsabile=responsabile

		self.inizio=inizio
		self.fine=fine
		if inizio=="today":
			self.inizio=str(datetime.datetime.now()).split(" ")[0]
		if fine=="today":
			self.fine=str(datetime.datetime.now()).split(" ")[0]

		self.personale=personale
		self.id=Lavoro.id_count
		Lavoro.id_count+=1

	def __cmp__(self, other):
		if self.inizio.__gt__(other.inizio):
			return 1
		elif self.inizio.__lt__(other.inizio):
			return -1
		else:
			return 0

	def to_html(self):
		out = "<td><input id=titolo"+str(self.id)+" type=text onchange=my_change('titolo"+str(self.id)+"') value="+self.titolo+"></td>"
		out	+="<td><input id=responsabile"+str(self.id)+" type=text onchange=my_change('responsabile"+str(self.id)+"') value="+self.responsabile+"></td>"
		out	+="<td><input id=inizio"+str(self.id)+" type=date onchange=my_change('inizio"+str(self.id)+"') value="+self.inizio+"></td>"
		out	+="<td><input id=fine"+str(self.id)+" type=date onchange=my_change('fine"+str(self.id)+"') value="+self.fine+"></td>"
		out	+="<td><input id=personale"+str(self.id)+" type=text name=personale[] onchange=my_change('personale"+str(self.id)+"') value="
		out +=self.personale_to_str()+"></td>"
		return out

	def nel_giorno(self,giorno):
		t_in=self.inizio.split("-")
		inizio = datetime.date(int(t_in[0]),int(t_in[1]),int(t_in[2]))
		t_in=self.fine.split("-")
		fine = datetime.date(int(t_in[0]),int(t_in[1]),int(t_in[2]))
		giorno=str(giorno).split(" ")[0]
		t_in=giorno.split("-")
		giorno = datetime.date(int(t_in[0]),int(t_in[1]),int(t_in[2]))
		if giorno.__ge__(inizio) and fine.__ge__(giorno):
			return True
		return False

	def personale_to_str(self):
		out=""
		for p in self.personale:
			out += p+","
		out=out[:-1]
		return out

users={}
f = open(os.path.join("db","users.txt"))
data = f.read().split()
f.close()
for d in data:
	c=d.split(",")
	users[c[0]]=c[1]

hashes={}

lavori=[]
lavori.append(Lavoro("prova","random","2016-03-08","2016-03-09",["nick","fede"]))
for i in range(100):
	lavori.append(Lavoro("prova","microfase","2016-03-08","2016-03-09",["nick","fede"]))

tecnici=[]
f = open(os.path.join("db","tecnici.txt"))
data = f.read().split()
f.close()
for d in data:
	tecnici.append(d)



def get_global_to_html():
	out=""
	ordinati=sorted(lavori)
	for lavoro in ordinati:
		out+="<tr> "
		out+="<td id=remove onclick=my_remove("+str(lavoro.id)+")>-</td>"
		out+=lavoro.to_html()
		out+="<td>"+get_tecnici_to_html(lavoro.id)+"</td>"
		out+="</tr>"

	return out

def get_lavoro(i):
	for lavoro in lavori:
		if lavoro.id==i:
			return lavoro
	return None

def get_tecnici_to_html(i):
	out="<select class=aggiungi_tecnico id=aggiungi_tecnico"+str(i)+" onchange=aggiungi_tecnico("+str(i)+")>"
	for tecnico in tecnici:
		out+="<option value="+tecnico+">"+tecnico+"</option>"
	out+="<option selected=selected value=aggiungi></option>"
	out+="</select>"
	return out	

def get_lavora_il_giorno(tecnico,giorno):
	out=0
	for lavoro in lavori:
		if lavoro.nel_giorno(giorno):
			if tecnico in lavoro.personale:
				out+=1
	return out

def get_schermata_tecnici_to_html():
	actual=datetime.datetime.now()
	timeframe=[]
	out="<tr><td></td>"
	for t in tecnici:
		out+="<td>"+t+"</td>"
	out+="</tr>"
	for i in range(90):
		out+="<tr> "
		out+="<td>"+str(actual).split(" ")[0]+"</td>"
		for t in tecnici:
			out+="<td>"
			out+=str( get_lavora_il_giorno(t,actual))
			out+="</td>"
		out+="</tr>"
		actual = actual+datetime.timedelta(days=1)
	return out

def exist_event(user,name):
	for lavoro in lavori:
		if lavoro.titolo==name and lavoro.responsabile==user:
			return True
	return False

def elimina_lavoro(i):
	for x in range(len(lavori)):
		if lavori[x].id==i:
			del lavori[x]
			return