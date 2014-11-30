import pymongo

CON = pymongo.Connection()
db = CON["wiki_translate"]

def fetch_cache_dict_translation(query, lang):
	trans = db.dict_trans.find_one({"query":query, "lang":lang})
	if trans:
		hits = int(trans["hits"])
		hits += 1
		db.dict_trans.update({"_id":trans["_id"]}, {"$set": {"hits": hits}})
		return trans["text"]
	else:
		return None

def insert_dict_translation(query,lang,text):
	db.dict_trans.insert({"query":query, "lang":lang, "text":text, "hits":1})

def insert_wiki_translation(title, langs):
	lg = ""
	for l in langs:
		lg = "%s,%s" % (lg,l)
	lg = lg[1:]
	db.wiki_trans.insert({"hits":0, "title":title, "langs": langs})

def fetch_cache_wiki_translation(title):
	trans = db.wiki_trans.find_one({"title":title})
	if trans:
		hits = int(trans["hits"])
		hits += 1
		db.wiki_trans.update({"_id":trans["_id"]}, {"$set": {"hits": hits}})
		return trans["langs"]
	else:
		return None