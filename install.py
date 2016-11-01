#!/usr/bin/python
#Configuration du sql connect 
import MySQLdb
import fileinput
import os

print("Config of wp-config.php")

userSQL = raw_input("User DB : ")
pwdSQL = raw_input("Pwd DB : ")
nameSQL = raw_input("Name DB : ")
hostSQL = raw_input("Host DB : (Default localhost) (y/n)")
if hostSQL == 'y':
	hostSQL = 'localhost'
elif hostSQL == 'n' : 
	hostSQL = raw_input("Host DB :")

print("New host is : "+hostSQL)

print("Editing of wp-config-db.php")

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

print("Cfg URLS in DB")

oldUrl = raw_input("Old URL ? ")
newUrl = raw_input("New URL ? ")
validate = raw_input("From URL : "+oldUrl+" => To new URL : "+newUrl+" , ok ? (y/n)")
if validate == 'y' :
	print("Check yes for config")
	print("Currently replace url main")
	db = MySQLdb.connect(host=hostSQL,
                     user=userSQL,
                     passwd=pwdSQL,
                     db=nameSQL)
	cur = db.cursor()
	reqUrl = ("UPDATE wp_options SET option_value = REPLACE(option_value, '"+oldUrl+"', '"+newUrl+"') WHERE option_name = 'home' OR option_name = 'siteurl';")
	if cur.execute(reqUrl):
		print("Url main OK, replace GUID ...")
		reqGuid = ("UPDATE wp_posts SET guid = REPLACE(guid, '"+oldUrl+"', '"+newUrl+"');")
		if cur.execute(reqGuid):
			print("Guid OK, repalce urls of medias (Images, Links, Docs)")
			reqContent = ("UPDATE wp_posts SET post_content = REPLACE(post_content, '"+oldUrl+"', '"+newUrl+"');")
			if cur.execute(reqContent):
				reqMetaPost = ("UPDATE wp_postmeta SET meta_value = REPLACE(meta_value, '"+oldUrl+"','"+newUrl+"');")
				if cur.execute(reqMetaPost):
					print("DB is OK")
				else:
					print("Error DB")
			else:
				print("Error CONTENT")
		else:
			print("Error GUID")
	else:
		print("Error URL")
else :
	print("Reload")
