#!/usr/bin/python
#Configuration du sql connect 
import MySQLdb
import fileinput
import os

print("Configuration de wp-config.php")

userSQL = raw_input("User DB : ")
pwdSQL = raw_input("Pwd DB : ")
nameSQL = raw_input("Name DB : ")
hostSQL = raw_input("Host DB : (Default localhost) (y/n)")
if hostSQL == 'y':
	hostSQL = 'localhost'
elif hostSQL == 'n' : 
	hostSQL = raw_input("Host DB :")

print("Le nouveau host est : "+hostSQL)

print("Modification du wp-config-db.php")

with open('wp-config.php') as fin, open('wp-config2.php', 'w') as fout:
    for i, name in enumerate(fin, 1):
        if i == 23: 
            name = "define('DB_NAME', '"+nameSQL+"');\n"
            os.remove("wp-config.php")
        fout.write(name)
with open('wp-config2.php') as fin, open('wp-config3.php', 'w') as fout:
    for i, name in enumerate(fin, 1):
        if i == 26: 
            name = "define('DB_USER', '"+userSQL+"');\n"
            os.remove("wp-config2.php")
        fout.write(name)
with open('wp-config3.php') as fin, open('wp-config4.php', 'w') as fout:
    for i, name in enumerate(fin, 1):
        if i == 29: 
            name = "define('DB_PASSWORD', '"+pwdSQL+"');\n"
            os.remove("wp-config3.php")
        fout.write(name)
with open('wp-config4.php') as fin, open('wp-config5.php', 'w') as fout:
    for i, name in enumerate(fin, 1):
        if i == 32: 
            name = "define('DB_HOST', '"+hostSQL+"');\n"
            os.remove("wp-config4.php")
            os.rename("wp-config5.php","wp-config.php")
        fout.write(name)

print("Configuration des URLs en db")

oldUrl = raw_input("Ancienne URL ? ")
newUrl = raw_input("Nouvelle URL ? ")
validate = raw_input("De l'url : "+oldUrl+" => vers cette nouvelle url : "+newUrl+" , ok ? (y/n)")
if validate == 'y' :
	print("Vous avez valide la configuration")
	print("Changement URL principale")
	db = MySQLdb.connect(host=hostSQL,
                     user=userSQL,
                     passwd=pwdSQL,
                     db=nameSQL)
	cur = db.cursor()
	reqUrl = ("UPDATE wp_options SET option_value = REPLACE(option_value, '"+oldUrl+"', '"+newUrl+"') WHERE option_name = 'home' OR option_name = 'siteurl';")
	if cur.execute(reqUrl):
		print("Url principale OK, changement des GUID en cours")
		reqGuid = ("UPDATE wp_posts SET guid = REPLACE(guid, '"+oldUrl+"', '"+newUrl+"');")
		if cur.execute(reqGuid):
			print("Guid OK, changement des urls des contenus (Images, Liens, Documents)")
			reqContent = ("UPDATE wp_posts SET post_content = REPLACE(post_content, '"+oldUrl+"', '"+newUrl+"');")
			if cur.execute(reqContent):
				reqMetaPost = ("UPDATE wp_postmeta SET meta_value = REPLACE(meta_value, '"+oldUrl+"','"+newUrl+"');")
				if cur.execute(reqMetaPost):
					print("Votre DB a ete mise a jour")
				else:
					print("Erreur DB")
			else:
				print("Erreur CONTENT")
		else:
			print("Erreur GUID")
	else:
		print("Erreur URL")
else :
	print("Reload la charge")