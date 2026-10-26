# content/photos.json: the image library for the blog

One JSON object per image. The owner adds real photos and their entries; the content agent only references ids, keeps `usedIn` current, and may add generated entries through `tools/generate_image.py` (files under `public/img/blog/ai/`). Nothing else writes this file.

| Field | Type | Meaning |
|---|---|---|
| `id` | string | Unique id used in `heroPhoto` and `{{photo id="..."}}`. Kebab-case, no spaces. |
| `file` | string | Path under `public/`, starting with `/`. Real photos: `/img/p/...` (already on the site) or `/img/blog/...`. Generated: `/img/blog/ai/...`. |
| `shows` | string | What is actually visible, in plain words. The agent matches slots against this. |
| `room` | bath \| shower \| kitchen \| tile \| other | Where the photo was taken. |
| `city` | string or null | City of the project, only if the client consented to naming it. |
| `materials` | list of strings | Materials visible (for example "12x24 porcelain tile", "quartz"). |
| `stage` | before \| during \| after \| detail \| before-after | before-after = a composite image; never used as a hero. |
| `pairWith` | id or null | The matching before/after photo, if any. |
| `orientation` | landscape \| portrait \| square | From the pixel size. |
| `width`, `height` | integers | Pixel size, read from the file. |
| `date` | YYYY-MM or null | When the photo was taken. |
| `clientConsent` | boolean | Must be `true` for the photo to appear in any article. Generated images set `true` (no client involved). |
| `heroOk` | boolean | May be used as a post's hero image. |
| `source` | photo \| ai | Real photograph or generated illustration. |
| `altDefault` | string | One factual sentence used as alt text when a block gives none. No keyword stuffing. |
| `usedIn` | list of slugs | Posts that use this image. Maintained by the agent; checked by the validator (max uses, unique hero). |

Extra fields on `source: "ai"` entries, written by `tools/generate_image.py`:

| Field | Meaning |
|---|---|
| `prompt` | The full prompt used, so the image can be regenerated with one change. |
| `model` | The image model, from `content/config.yaml`. |
| `generatedOn` | YYYY-MM-DD. |
| `iptcWritten` | `true` when ExifTool was available and the IPTC `DigitalSourceType` tag was written. |

Rules the validator enforces: a real photo appears in at most `images.max_uses_per_photo` posts; a hero photo is the hero of one post only; generated images live only under `/img/blog/ai/`, never in project stories, never in before/after pairs, and never carry captions or alt text that claim the room is ours. No visible AI label is printed (owner decision 2026-10-24); `source: "ai"` and the IPTC tag stay.

Adding a real photo (owner): resize to 1600 px on the long side, save as WebP without EXIF/GPS, name it `<city>-<room>-<yyyy-mm>-<stage>-<nn>.webp` under `public/img/blog/`, then add an entry here with `clientConsent` set truthfully.
