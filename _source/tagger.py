import json, re, sys
from collections import Counter

# tag -> regex (case-insensitive) matched against card text
THEMES = {
 'baptism': r'\bbaptis|\bbaptiz', 'covenant': r'\bcovenant', 'gospel': r'\bgospel',
 'grace': r'\bgrace\b', 'faith': r'\bfaith\b', 'salvation': r'\bsalvation|\bsaved\b|\bsaves\b',
 'justification': r'\bjustif', 'sanctification': r'\bsanctif', 'glorification': r'\bglorif',
 'adoption': r'\badopt', 'atonement': r'\batone', 'election': r'\belect(ion|ed)\b|\bchosen\b|predestin',
 'repentance': r'\brepent', 'forgiveness': r'\bforgiv', 'resurrection': r'\bresurrect|\braised\b|\brisen\b',
 'the cross': r'\bcross\b|crucif', 'holy spirit': r'holy spirit|\bspirit of god', 'prayer': r'\bpray',
 'worship': r'\bworship', 'church': r'\bchurch', 'marriage': r'\bmarriage|\bmarried|\bhusband|\bwife\b|\bwives\b',
 'family': r'\bfamily|\bfamilies|\bhousehold', 'children': r'\bchild|\bparent', 'love': r'\blove\b|\bloving\b',
 'kingdom of god': r'kingdom', 'great commission': r'great commission|disciple (all )?the nations|make disciples',
 'nations': r'\bnations\b', 'government': r'\bgovern|\bcivil\b|\bmagistrat|\bcaesar|\bruler',
 "god's law": r"\blaw\b|commandment", 'theonomy': r'theonom', 'conscience': r'\bconscience',
 'apologetics': r'apologetic|\bobjection|\bworldview', 'creation': r'\bcreation|\bcreated\b|\bcreator',
 'evolution': r'\bevolution', 'sin': r'\bsin\b|\bsins\b|\bsinful|\bsinner', 'idolatry': r'\bidol',
 'suffering': r'\bsuffer|\btrial', 'hope': r'\bhope', 'eschatology': r'eschatolog|end times|millenni|second coming|return of christ',
 'heaven': r'\bheaven', 'judgment': r'\bjudg', 'discipleship': r'\bdisciple', 'evangelism': r'evangel|\bwitness',
 'leadership': r'\blead(er|ership)', 'humility': r'\bhumil|\bhumble', 'pride': r'\bpride\b|\bproud',
 'wisdom': r'\bwis(dom|e)\b', 'truth': r'\btruth', 'culture': r'\bcultur|\bsecular',
 'sanctity of life': r'\babortion|\bunborn|sanctity of (human )?life|conception to natural death', 'sexuality': r'\bsexual',
 'gender': r'\bgender|\bmasculin|\bfemin|\bmanhood|\bwomanhood', 'communication': r'\bcommunicat|\blisten|\bconversation|\bspeak',
 'unity': r'\bunity|\bunited|\bdivision', 'spiritual gifts': r'spiritual gifts|gifts of the (holy )?spirit|\btongues|\bprophecy',
 'armor of god': r'armou?r of god|\bshield of faith|\bbreastplate', 'spiritual warfare': r'\bbattle|\bwarfare|\benemy|\bsatan|\bdevil',
 'bible study': r'\bscripture|bible study|\bread(ing)? the bible', 'interpretation': r'hermeneut|interpret|exegesis|\bcontext\b',
 "christ's lordship": r'\blord(ship)? of all|\bking jesus|all authority|\breigns?\b|\bthrone', 'trinity': r'\btrinit|\btriune',
 'sovereignty of god': r'\bsovereign', 'easter': r'\beaster', "lord's supper": r"lord'?s supper|communion|\bthe table\b",
 'giving': r'\bgenerous|\bgiving\b|\bcollection|\btithe|\boffering', 'obedience': r'\bobe(y|di)',
 'holiness': r'\bholiness|\bholy living|\bblameless|\bpurity', 'identity': r'\bidentity|\bin christ\b|\bimage[- ]bearer|image of god',
 'purpose': r'\bpurpose|\bcalling\b|\bvocation', 'deacons': r'\bdeacon', 'shepherding': r'\bshepherd|\bpastoral care|\bcare for',
 'promises of god': r'\bpromise', 'peace': r'\bpeace', 'jesus christ': r'\bjesus|\bchrist\b|\bmessiah',
 'doctrines of grace': r'total depravity|unconditional election|limited atonement|irresistible grace|perseverance of the saints|\btulip\b|calvinis',
 'westminster': r'westminster', 'catechism': r'catechism', 'heresy': r'\bheres|false teach|\bheretic',
 'discernment': r'\bdiscern', 'patience': r'\bpatien', 'courage': r'\bcourage', 'honor': r'\bhonou?r\b',
 'work': r'\blaz(y|iness)|\bdiligen|\bwork ethic|\bsluggard', 'mind': r'\bthoughts?\b|\bmind\b',
}
BOOKS = ['Genesis','Exodus','Leviticus','Numbers','Deuteronomy','Joshua','Judges','Ruth','1 Samuel','2 Samuel','1 Kings','2 Kings',
 '1 Chronicles','2 Chronicles','Ezra','Nehemiah','Esther','Job','Psalms','Proverbs','Ecclesiastes','Song of Songs','Isaiah','Jeremiah',
 'Lamentations','Ezekiel','Daniel','Hosea','Joel','Amos','Obadiah','Jonah','Micah','Nahum','Habakkuk','Zephaniah','Haggai','Zechariah',
 'Malachi','Matthew','Mark','Luke','John','Acts','Romans','1 Corinthians','2 Corinthians','Galatians','Ephesians','Philippians',
 'Colossians','1 Thessalonians','2 Thessalonians','1 Timothy','2 Timothy','Titus','Philemon','Hebrews','James','1 Peter','2 Peter',
 '1 John','2 John','3 John','Jude','Revelation']
ABBR = {'Gen':'Genesis','Ex':'Exodus','Exod':'Exodus','Deut':'Deuteronomy','Ps':'Psalms','Psalm':'Psalms','Prov':'Proverbs','Isa':'Isaiah',
 'Jer':'Jeremiah','Ezek':'Ezekiel','Dan':'Daniel','Zech':'Zechariah','Matt':'Matthew','Mt':'Matthew','Rom':'Romans','Gal':'Galatians',
 'Eph':'Ephesians','Phil':'Philippians','Col':'Colossians','Heb':'Hebrews','Rev':'Revelation','Jas':'James','Lk':'Luke','Jn':'John'}

def book_refs(text):
    out = Counter()
    for b in BOOKS:
        num, _, name = b.partition(' ') if b[0].isdigit() else ('', '', b)
        pat = (rf'\b{num}\s*{name}' if num else rf'(?<![123]\s)(?<![123])\b{name}') + r'\.?\s+\d+[:.]\d+'
        out[b] += len(re.findall(pat, text))
    for a, b in ABBR.items():
        num = ''
        out[b] += len(re.findall(rf'(?<![123]\s)\b{a}\.?\s+\d+[:.]\d+', text))
    for n in '123':
        for a, b in [('Cor', 'Corinthians'), ('Tim', 'Timothy'), ('Pet', 'Peter'), ('Thess', 'Thessalonians'), ('Sam', 'Samuel'), ('Kgs', 'Kings')]:
            out[f'{n} {b}'] += len(re.findall(rf'\b{n}\s*{a}\.?\s+\d+[:.]\d+', text))
    return out

def tag(item, text, max_themes=7, max_books=3):
    head = ' '.join([item['title'], item['sub'], item['series']])
    body = text
    scores = {}
    for t, rx in THEMES.items():
        h = len(re.findall(rx, head, re.I)); n = len(re.findall(rx, body, re.I))
        s = h * 5 + n
        if h or n >= 2: scores[t] = s
    scores.pop('jesus christ', None)
    if 'mind' in scores and not re.search(THEMES['mind'], head, re.I): scores.pop('mind')
    themes = [t for t, _ in sorted(scores.items(), key=lambda kv: -kv[1])][:max_themes]
    hb = book_refs(head); bb = book_refs(body)
    bs = {b: hb[b] * 5 + bb[b] for b in BOOKS if hb[b] or bb[b] >= 2}
    books = [b for b, _ in sorted(bs.items(), key=lambda kv: -kv[1])][:max_books]
    return themes + books

MANUAL = {
 'grappling-with-a-concept': ['critical thinking', 'apologetics', 'communication'],
 'teaching-grid-scenarios': ['critical thinking', 'apologetics', 'communication'],
 'grappling-2-in-1': ['critical thinking', 'apologetics', 'communication'],
 'correcting-graciously': ['correction', 'communication', 'leadership'],
 'glossary-anthropomorphism': ['attributes of god', 'interpretation'],
 'glossary-anthropopathism': ['attributes of god', 'interpretation'],
 'what-if-it-turns-out': ['evangelism', 'outreach', 'relationship with god'],
 'five-aspects-of-man': ['identity', 'gender', 'creation'],
 'glossary-double-imputation': ['justification', 'atonement', 'imputation'],
 'week-7-character': ['narrative', 'interpretation'],
 'week-8-setting': ['narrative', 'interpretation'],
 'evolution-portrait': ['creation', 'science'],
 'gracious-persuasion-3': ['listening', 'apologetics'],
 'gethsemane': ['prayer'],
 'sanctity-of-life': ['abortion'],
 'glossary-glorification': ['salvation', 'resurrection', 'eschatology'],
 'week-4-literary-styles': ['genre', 'interpretation'],
 'week-6-partner-activity': ['narrative', 'plot', 'interpretation'],
 'exegesis-eisegesis-narcigesis': ['exegesis', 'bible study'],
 'children-of-the-covenant-highlights': ['infant baptism', 'circumcision'],
 'pre-sermon-covenant-promise': ['abraham', 'circumcision'],
}

if __name__ == '__main__':
    cat = json.load(open(sys.argv[1])); txtdir = sys.argv[2]
    res = {}
    for i in cat:
        try: text = open(f'{txtdir}/{i["id"]}.txt', errors='ignore').read()
        except FileNotFoundError: text = ''
        res[i['id']] = tag(i, text)
        for t in MANUAL.get(i['id'], []):
            if t not in res[i['id']]: res[i['id']].insert(0, t)
    json.dump(res, open(sys.argv[3], 'w'), indent=0)
    for k, v in res.items(): print(k, '|', ', '.join(v))
