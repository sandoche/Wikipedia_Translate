import pymongo
from config import DB_USER, DB_PASS, MONGO_PORT
from datetime import datetime

CON = pymongo.Connection(port=MONGO_PORT)
db = CON["wiki_translate"]
db.authenticate(DB_USER, DB_PASS)

def fetch_cache_dict_translation(query, lang):
	'''
	Checks if provided query is in the db cache.

	Args:
		query: query that was issued for translation 
		lang: language code for which the translation is being 
                      asked for 
	Returns:
		Translated text if one is found or None if not found.
	'''
	trans = db.dict_trans.find_one({"query":query, "lang":lang})
	if trans:
		hits = int(trans["hits"])
		hits += 1
		db.dict_trans.update({"_id":trans["_id"]}, 
                        {"$set": {"hits": hits, "updated":datetime.now()}})
		return trans["text"]
	else:
		return None


def insert_dict_translation(query,lang,text):
	'''
	Inserts into db cache the provided dictionary mapping.

	Args:
		query: query that was issued for translation
		lang: language code for which the translation is being 
                      asked for
		text: translated text 
	'''
	db.dict_trans.insert({"query":query, "lang":lang, 
            "text":text, "hits":1, "updated":datetime.now(), 
            "updated":datetime.now()})


def insert_wiki_translation(title, langs):
	'''
	Inserts into db cache the provided wiki property.

	Args:
		title: Wikipedia valid article title
		langs: list of dicts in form:
			lang: language
			text: appropriate translation
			lang_code: corresponding langauge code
			url: corresponding wikipedia url page in the language

	'''
        db.wiki_trans.insert({"hits":1, "title":title, "langs": langs, 
            "created":datetime.now(), "updated":datetime.now()})


def fetch_cache_wiki_translation(title):
	trans = db.wiki_trans.find_one({"title":title})
	if trans:
		hits = int(trans["hits"])
		hits += 1
		db.wiki_trans.update({"_id":trans["_id"]}, 
                        {"$set": {"hits": hits, "updated":datetime.now()}})
		return trans["langs"]
	else:
		return None
