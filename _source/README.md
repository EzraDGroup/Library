# How this site is maintained

Three pages, built from the catalogs in this folder:

| Page | Catalog | Template | Published at |
|---|---|---|---|
| Learn · Do · Teach | catalog.json | library-template.html | /index.html (files/, thumbs/, pages/) |
| Political Battle Cards | polcatalog.json | political-template-built.html (catalog embedded as `const ITEMS=`) | /political/ |
| Growth & Development | devcatalog.json | growth-template.html (`__DEVURL__` placeholder) | /growth/ |

Each catalog entry: id, topic (section id), series, title, sub, kind, file, dl (download filename),
size, pages (preview images), n (page count), thumb, optional `also` (list of section ids that show
the card as an "Additional resources" link) and `sub_in` ({section: subheading}).

Templates contain `__CATALOG__`, replaced with the JSON catalog. The templates were written for a
Claude artifact; build_notes_original.py converts them to standalone pages (adds the HTML head,
replaces the download code with a plain download link, uses location for share links).

Conventions:
- One card lives in exactly one section; other sections link to it via `also`.
- Sermons are ordered newest first; pre-sermon card before highlights for each Sunday.
- Drop a "-P" suffix from incoming file names (it marks printed copies).
- Long PDFs: page previews rendered with pdftoppm; large image PDFs recompressed.
- Repository name is "Library" (capital L) — URLs are case-sensitive: https://ezradgroup.github.io/Library/
