#coding:utf-8
from bs4 import BeautifulSoup 
import codecs
import re
import sys
import os
from subprocess import Popen, PIPE

def input(chemin):
	a = codecs.open(chemin, "r", "utf-8")
	html_doc=a.read()
	a.close()
	soup = BeautifulSoup(html_doc, 'html.parser')

	return soup

toto = "../projets_zhu_2017/projet_canard2/rsc/canard_lichao_corpus_corrige_GL.xml"
soup = input(toto)

sequence = soup.find_all(u"séquence_figée")
chemin_corpus = sys.argv[1]

w = codecs.open("output.txt", "w", "utf-8")
for exp in sequence :
	expression = u"%s"%exp.text
	len_expression = len(expression)
	mots_origine = re.split(" |,", expression)
	w.write(expression+"\n")
	expression = re.sub("'", "\\'", expression)
	expression = expression[:8]
	w.write(" "+expression+"\n")
	commande = u"grep -r -E -h -o '"+expression+".{30}' "+ chemin_corpus

	#os.system(commande.encode("utf-8"))
	exp_formate = expression+".{30}"
	p1 = Popen(["grep", "-r", "-E" ,"-h" ,"-o", exp_formate, chemin_corpus], stdout=PIPE)

	resultats = p1.communicate(str.encode("utf-8"))[0]
	liste_resultats = resultats.splitlines()
	print("NB résultats avant filtrage: "+str(len(liste_resultats)))
	liste_resultats_filtree = []
	for resultat in liste_resultats:
		mots_resultat = re.split(" |,", resultat[:len_expression])
		cpt = 0
		for i, mot in enumerate(mots_resultat):
			if i>=len(mots_origine):
				continue
			if mot==mots_origine[i]:
				cpt+=1
		if cpt>=2:
			liste_resultats_filtree.append(resultat)
	print("  NB résultats après filtrage: "+str(len(liste_resultats_filtree)))
				
	liste_resultats = [u"  "+resultat.decode("utf-8")+u"\n" for resultat in liste_resultats_filtree]
	liste_resultats = sorted(liste_resultats)
	w.write(u"".join(liste_resultats))
		#w.write("  "+resultat.decode("utf-8")+"\n")
	#print(p1.communicate()[1])
w.close()

