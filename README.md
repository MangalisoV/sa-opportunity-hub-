# SA Opportunity Hub

An independent directory of South African jobs, bursaries, tenders, internships and learnerships.

Official source links are provided. Automated imports require configuration of approved RSS or Atom feeds.

## Hosting
Enable GitHub Pages under Settings > Pages, Deploy from a branch, main / (root).

## Automatic updates
The GitHub Actions workflow runs daily. Set the Actions repository variable `OFFICIAL_FEEDS_JSON` to an array of permitted feed configurations (URL, category, organization). No official feeds are preconfigured, so no automatic listings will appear until verified feeds are added.

Always verify opportunities and deadlines with the original publisher.
