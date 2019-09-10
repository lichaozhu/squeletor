import sys, json, re, os

liste_kw = [["numérique"], ["digital", "digitaux"]]
stats = {formes[0]:[0, 0, 0] for formes in liste_kw}
has_all = 0

main_dir = "data_sub_corpus_lemonde"
sub_corpus_name = "%s/%s"%(main_dir, "_".join(stats.keys()))
sub_corpus_name = re.sub("é", "e", sub_corpus_name)#for Antconc

for annee in range(1987, 2006):
  dossier = "%s/%i"%(sub_corpus_name, annee)
  try:
    os.makedirs(dossier)
  except:
    pass

for json_path in sys.argv[1:]:
  f = open(json_path)
  dic = json.load(f)
  f.close()
  has_num = 0
  has_dig = 0
  for ID, infos in dic.items():
    ID = re.sub("\n", "", ID)
    titre = infos["Titre"]
    texte = infos["Texte"]
    date = infos["Date"]
    if type(texte) is not str:
      try:
        texte =" [Categorie=%s]"%infos["Categorie"]
      except:
        texte =" [Categorie=autres]"
    if type(titre) is not str:
      titre = "__"
    toto = titre+texte
    toto = toto.lower()
    nb=0
    for formes in liste_kw:
      lemme = formes[0]
      num = []
      for forme_kw in formes:
        num+= re.findall(forme_kw, toto)
      if len(num)>0:
        nb+=1
        stats[lemme][0]+=1
        if len(num)==1:
          stats[lemme][1]+=1
        stats[lemme][2]+=len(num)
        
    if nb>0:
      filename = "%s__%s"%(date, ID)
      chaine = titre +"----\n" + texte
      w = open("%s/%s/%s.txt"%(sub_corpus_name, date[:4], filename), "w")
      w.write(chaine)
      w.close()
    if nb == len(liste_kw):
      has_all +=1
print("has_all : %i"%has_all)
for kw in stats:
  support = stats[kw][0]
  hapax = stats[kw][1]
  effectif = stats[kw][2]
  print("%s : %i textes dont %i hapax pour %i occurences"%(kw, support, hapax, effectif)) 
