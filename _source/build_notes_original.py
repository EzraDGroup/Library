import json,os,re,shutil
R='/home/claude/library'
def convert(html):
    m=re.match(r'\s*<title>(.*?)</title>',html,re.S); title=m.group(1); body=html[m.end():]
    links=''.join(re.findall(r'<link[^>]*>\n?',body)); body=re.sub(r'<link[^>]*>\n?','',body)
    # downloads: plain link
    s=body.index('async function download(id){'); e=body.index('function shareLinkMsg(')
    body=body[:s]+'''function download(id){
  const it=ITEMS.find(i=>i.id===id); if(!it) return;
  const a=document.createElement('a'); a.href=it.file; a.download=it.dl; a.rel='noopener';
  document.body.appendChild(a); a.click(); a.remove();
}
'''+body[e:]
    body=re.sub(r"let downloads=null;\n\(async\(\)=>\{[^\n]*\}\)\(\);\n",'',body)
    body=re.sub(r"const PAGE_URL='[^']*';","const PAGE_URL=location.origin+location.pathname;",body)
    head=f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<title>{title}</title>\n{links}<style>html,body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>\n</head>\n<body>\n'
    return head+body+'\n</body>\n</html>\n'
def build(src_dir,template_html,catalog,dest):
    os.makedirs(dest,exist_ok=True)
    for d in ['files','thumbs','pages']:
        os.makedirs(f'{dest}/{d}',exist_ok=True)
    for i in catalog:
        for p in [i['file'],i['thumb']]+i['pages']:
            shutil.copy(f'{src_dir}/{p}',f'{dest}/{p}')
    html=convert(template_html.replace('__CATALOG__',json.dumps(catalog,ensure_ascii=False)))
    assert 'downloads.save' not in html and 'window.open' not in html
    open(f'{dest}/index.html','w').write(html)
# church: restore full page lists
c=json.load(open('catalog.json'))
for i in c:
    if i.get('preview_only'):
        i['pages']=sorted('pages/'+x for x in os.listdir('site/pages') if x.startswith(i['id']+'-'))
        i.pop('preview_only')
        assert len(i['pages'])==i['n'],(i['id'],len(i['pages']))
build('site',open('site/template.html').read(),c,R)
# political
pol=json.load(open('polcatalog.json'))
p=open('polsite/index.html').read()
p=re.sub(r'const ITEMS=.*?;\n','const ITEMS=__CATALOG__;\n',p,count=1,flags=re.S)
build('polsite',p,pol,R+'/political')
d=json.load(open('devcatalog.json'))
build('devsite',open('devsite/template.html').read(),d,R+'/growth')
open(R+'/.nojekyll','w').write('')
print('ok')
