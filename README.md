# SA Opportunity Hub

Free, independent South African opportunity directory: jobs, bursaries, internships, learnerships and government procurement sources.

## Live site
https://mangalisov.github.io/sa-opportunity-hub-/

## Production checklist
- [x] Public GitHub Pages hosting with HTTPS
- [x] Responsive homepage, searchable directory and keyboard-visible focus
- [x] SEO title, description, canonical URL, sitemap.xml, robots.txt
- [x] Original application guides, privacy policy and editorial policy
- [x] Distinction between official directories and published opportunity information
- [x] Scheduled GitHub Actions collector with automated unit tests
- [ ] Individual tender records from a verified, permitted eTender API/feed
- [ ] Further verified first-party opportunity feeds
- [ ] Google Search Console ownership verification (site owner action)
- [ ] Domain and AdSense review (a custom registrable domain may be required)
- [ ] AdSense payment identity / banking details (account holder action, **never commit bank details**)

## Maintaining opportunity data
Data lives in `data/opportunities.json`. Jobs are sourced from the DPSA vacancy circular index, and Funza Lushaka information is checked from its official website. The National Treasury eTender portal is currently a **directory link**, not a live tender import. Verify expiry and closing dates from source pages; an umbrella DPSA circular may contain many advertisements with different deadlines.

The workflow `.github/workflows/update.yml` runs at 05:15 UTC daily and can be started from Actions > Refresh opportunity feeds > Run workflow. It runs `python -m unittest -v test_update.py` before updating data. Optional approved RSS/Atom feeds can be configured using repository Actions variable `OFFICIAL_FEEDS_JSON` with objects containing `url`, `category`, and `organization`; avoid feeds without permission to republish.

## Google setup
1. Add a URL-prefix property for the live address to Google Search Console.
2. Verify site ownership and submit `https://mangalisov.github.io/sa-opportunity-hub-/sitemap.xml`.
3. Register for AdSense without a site while the domain question remains unresolved. Never misrepresent ownership of github.io.
4. Enter personal identity and banking information **inside Google AdSense**, not in this repository, public issues, or chats.
5. Add `ads.txt` and ad scripts **only after** Google supplies a publisher ID and the site is eligible.

## Editorial caution
SA Opportunity Hub is not affiliated with official publishers, doesn't accept applications and cannot guarantee funding or employment. Review publisher pages before applying. Paid advertisements are **not yet enabled**.
