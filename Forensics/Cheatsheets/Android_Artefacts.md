## Android Artefacts


**1.Applications**
 - */data/system/packages.list*
 - */data/system/package-usage.list*

**2.Wifi**
 - */data/misc/wifi/wpa_supplicant.conf*

**3.Contacts & Calls**
 - */data/data/com.android.providers.contacts/files*
	 - *photos*
	 - *profile*
 - */data/data/com.android.providers.contacts/databases/contacts2.db*
	- *raw_contacts*
	- *accounts*
	- *data*
	- *contacts*
	- *calls*
	- *deleted_contacts*
	- *groups*

**4.SMS/MMS**
 - */data/data/com.android.providers.telephony/app_parts*
 - */data/data/com.android.providers.telephony/databases/telephony.db*
	 - *siminfo*
 - */data/data/com.android.providers.telephony/databases/mmssms.db*
	 - *part*
	 - *sms*
	 - *pdu*

**5.User Dictionary**
 - */data/data/com.android.providers.userdictionary/databases/user_dict.db*
	 - *words*

**6.Gmail**
 - */data/data/com.google.android.gm/databases/mailstore.username@gmail.com.db*
	 - *conversations*
 - */data/data/com.google.android.gm/databases/suggestions.db*
 - /data/data/com.google.android.gm/shared_prefs/
	 - *Gmail.xml*
	 - *MailAppProvider.xml*
	 - *UnifiedEmail.xml*

**7.Chrome**
 - *data/data/com.android.chrome/app_chrome/Default/*
	- *Sync Data/SyncData.sqlite3*
	- *Bookmarks*
	- *Cookies*
	- *Google Profile Picture.png*
	- *History*
	- *Login Data*
	- *Preferences*
	- *Top Sites*
	- *Web Data*
 - *data/data/com.android.chrome/app_ChromeDocumentActivity*

**8.Google Maps**
 - */data/data/com.google.android.apps.maps/cache/http/*
 - */data/data/com.google.android.apps.maps/databases/gmm_myplaces.db*
 - */data/data/com.google.android.apps.maps/databases/gmm_storage.db*

**9.Facebook Analysis**
 - */data/data/com.facebook.katana/files/video-cache/*
 - */data/data/com.facebook.katana/cache/images/*
 - */data/data/com.facebook.katana/databases/bookmarks_db2*
 - */data/data/com.facebook.katana/databases/contacts_db2*
 - */data/data/com.facebook.katana/databases/nearbytiles_db*
 - */data/data/com.facebook.katana/databases/newsfeed_db*
 - */data/data/com.facebook.katana/databases/notifications_db*
 - */data/data/com.facebook.katana/databases/prefs_db*
 - */data/data/com.facebook.katana/databases/threads_db2*

**10.Facebook Messenger Analysis**
 - */data/data/com.facebook.orca/cache/*
	 - *audio*
	 - *fb_temp*
	 - *image*
 - */data/sdcard/com.facebook.orca/*
 - */data/data/com.facebook.orca/files/rti.mqtt.analytics.xml*
 - */data/data/com.facebook.orca/databases/*
	 - *call_log.sqlite*
	 - *contacts_db2*
	 - *prefs_db*
	 - *threads_db2*

**11.Skype Analysis**
 - */data/data/com.skype.raider/cache/skype-4228/DbTemp*
 - */sdcard/Android/data/com.skype.raider/cache/*
 - */data/data/com.skype.raider/files/*
	 - *shared.xml*
	 - *username/thumbnails/*
	 - *username/main.db*
	 - *username/chatsync (video message recovery)*

**12.Snap Chat Analysis**
 - */sdcard/Android/data/com.snapchat.android/cache/my_media/*
 - */data/data/com.snapchat.android/*
	 - */cache/stories/received/thumbnail/*
	 - */shared_prefs/com.snapchat.android_preferences.xml*
	 - */databases/tcspahn.db*

**13.Viber Analysis**
 - */data/data/com.viber.voip*
	 - */files/preferences/*
		 - *activated_sim_serial*
		 - *display_name*
		 - *reg_viber_phone_num*
	- */sdcard/viber/media/*
		- */User Photos/*
		- */Viber Images/*
		- */Viber Videos/*
	- */databases/*
		- *viber_data*
		- *viber_message*
		
**14.Tango Analysis**
 - */data/data/com.sgiggle.production/files/*
	 - *tc.db*
	 - *userinfo.xml.db*
 - */sdcard/Android/data/com.sgiggle.production/files/storage/appdata/*
	 - *TCStorageManagerMediaCache_v2/*
	 - *conv_msg_tab_snapshots/*
 - *Tango Decryption*
	 - *base64*
	 - 
*tcdb.py*
```
import sqlite3
import base64
conn = sqlite3.connect('tc.db')
c = conn.cursor()
c.execute('SELECT msg_id, payload FROM messages')
message_tuples = c.fetchall()
with open('tcdb_out.txt', 'w') as f:
for message_id, message in message_tuples:
f.write(str(message_id) + '\x09')
f.write(str(base64.b64decode(message)) + '\r\n')
```
*userinfo.xml.db.py*
```import sqlite3
import base64
conn = sqlite3.connect('userinfo.xml.db')
c = conn.cursor()
c.execute('SELECT key, value FROM profiles')
key_tuples = c.fetchall()
with open('userinfo_out.txt', 'w') as f:
for key, value in key_tuples:
if value == None:
value = 'Tm9uZQ=='
f.write(str(base64.b64decode(key)) + '\x09')
f.write(str(base64.b64decode(value)) + '\r\n')
```
**15.WhatsApp Analysis**
 - */data/data/com.whatsapp/*
	 - *files/*
		 - *Avatars/*
		 - *me*
		 - *me.jpg*
	 - *shared_prefs/*
		 - *RegisteredPhone.xml*
		 - *VerifySMS.xml*
	 - */databases/*
		 - *msgstore.db*
		 - *wa.db*
	 - */sdcard/WhatsApp/*
		 - *media/*
		 - *databases.*

Decrypting msgstore.db
 - https://forum.xda-developers.com/android/apps-games/how-to-decode-whatsapp-crypt8-db-files-t2975313
 - https://forum.xda-developers.com/showthread.php?t=1583021

**16.Kik**
 - */data/data/kik.android*
	 - *cache/*
		 - *chatPicsBig/*
		 - *contentpics/*
		 - *profPics/*
	 - */files/staging/thumbs*
	 - */shared_prefs/KikPreferences.xml*
	 - */sdcard/Kik/*
	 - */databases/kikDatabase.db*



**17.WeChat**
 - */data/data/com.tencent.mm/*
	 - */files/host/*.getdns2*
	 - */shared_prefs/*
		 - *com.tencent.mm_preferences.xml*
		 - *system_config_prefs.xml*
	 - */sdcard/tencent/MicroMsg/*
		 - *diskcache/*
		 - *WeChat/*
	 - */sdcard/tencent/MicroMsg/\*/*
		 - *image2/*
		 - *video/*
		 - *voice2/*
	 - */MicroMsg/*
		 - *CompatibleInfo.cfg*
		 - *\*/EnMicroMsg.db*
		 

WeChat Message Decrypting  
 - https://articles.forensicfocus.com/2014/10/01/decrypt-wechat-enmicromsgdb-database/
 - https://gist.github.com/fauzimd/8cb0ca85ecaa923df828/download
 
---

**Tools**
 - Linux Time Converter
	 - https://www.epochconverter.com/
 - Webkit Time Converter
	 - https://www.epochconverter.com/webkit
 - SQLite Browser
 - XML Viewer
---
**Referneces**
 - https://www.packtpub.com/networking-and-servers/learning-android-forensics-second-edition
