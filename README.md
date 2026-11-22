# 22 November 2026 — the world in one day

A single front page summing up the news of Sunday 22 November 2026: ten stories across
Europe, the Middle East, Africa, Asia, the Americas, tech and space, drawn as a newspaper
page with the date set in the masthead.

`build_image.py` draws it with Pillow; `entry.png` is the rendered result, and `main.ts`
copies it to `/output/entry.png`.

```
python3 build_image.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## The stories

| Region | Story |
| --- | --- |
| Europe | a cargo ship damaged in the Baltic; a barrage reported over Lviv |
| Middle East | an Iranian claim of strikes on Bahrain, denied; a US F-16 loss claim denied; renewed Hormuz talks |
| Africa | an overloaded boat disaster in Nigeria |
| Asia | a magnitude 7.4 earthquake off Maluku |
| Americas | a capture in Sinaloa |
| Tech | a large AI march in London |
| Space | a Mercury orbit milestone |

## Licence

MIT — see `LICENSE`.