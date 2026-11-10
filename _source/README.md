# How this site is maintained

Three pages, built from the catalogs in this folder:

| Page | Catalog | Template | Published at |
|---|---|---|---|
| Learn · Do · Teach | catalog.json | library-template.html | /index.html (files/, thumbs/, pages/) |
| Political Battle Cards | polcatalog.json | political-template-built.html (catalog embedded as `const ITEMS=`) | /political/ |
| Growth & Development | devcatalog.json | growth-template.html (`__DEVURL__` placeholder) | /growth/ |

Each catalog entry: id, topic (section id), series, title, sub, kind, file, dl (download filename),
size, pages (preview images), n (page count), thumb, optional `last_in` (list of section ids where the card shows at the very end, after the subheading groups), optional `also` (list of section ids that show
the card as an "Additional resources" link) and `sub_in` ({section: subheading}), and `tags` (hidden search keywords).

Templates contain `__CATALOG__`, replaced with the JSON catalog. The templates were written for a
Claude artifact; build_notes_original.py converts them to standalone pages (adds the HTML head,
replaces the download code with a plain download link, uses location for share links).

Conventions:
- One card lives in exactly one section; other sections link to it via `also`.
- Sermons are ordered newest first; Sermon Highlights card first, then that Sunday's pre-sermon materials.
- Drop a "-P" suffix from incoming file names (it marks printed copies).
- Long PDFs: page previews rendered with pdftoppm; large image PDFs recompressed.
- Repository name is "Library" (capital L) — URLs are case-sensitive: https://ezradgroup.github.io/Library/
- Tags: every card gets hidden `tags` (themes + main Bible books) that the search box matches. Generate with
  `_source/tagger.py` (keyword vocabulary over the card's text, extracted with pdftotext or tesseract), plus
  hand-picked tags in its MANUAL dict. Review copy of all tags: _source/tags.md. Tag new cards when adding them.
