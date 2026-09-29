# kvase.ai

A small static landing page for Kvase, currently building in stealth. HTML, CSS
and SVG, with a self-hosted font and no client-side JavaScript or analytics.

## Local development

Requires Node.js 22.22.1+ (Node 24 recommended) and Python 3 for the preview server.

```sh
npm ci
npm run dev
```

Open <http://127.0.0.1:8080>. Edit `site/index.html`, `site/styles.css` and
`site/assets/`. The contact link currently goes to `simen@eide.ai`.

```sh
npm run format
npm run check
```

`npm ci` enables the repository's Git hooks. The pre-commit hook formats staged
files with lint-staged (preserving unstaged edits) and validates the HTML. The
pre-push hook scans Git history with Gitleaks. Install
[Gitleaks](https://github.com/gitleaks/gitleaks#installing) and put it on your
`PATH` before pushing. CI repeats formatting, HTML validation and secret checks;
its Gitleaks download is version-pinned and checksum-verified.

## Deployment

GitHub Actions checks pull requests and deploys `site/` to GitHub Pages on pushes
to `main`. No build step or deployment secrets are needed. Only `site/` is
published. Set **Settings → Pages → Build and deployment → Source** to
**GitHub Actions**.

The canonical domain is `kvase.ai`. To connect it:

1. Set **Settings → Pages → Custom domain** to `kvase.ai`.
2. At the DNS provider, replace the apex (`@`) A record with these four records:

   | Type  | Name | Value              |
   | ----- | ---- | ------------------ |
   | A     | @    | 185.199.108.153    |
   | A     | @    | 185.199.109.153    |
   | A     | @    | 185.199.110.153    |
   | A     | @    | 185.199.111.153    |
   | CNAME | www  | kvase-ai.github.io |

3. Remove conflicting apex or `www` A/AAAA/CNAME records, if present. Preserve
   email (MX/TXT) and other subdomain records.
4. Once DNS is verified and GitHub provisions the certificate, enable **Enforce
   HTTPS** in Pages settings.

For the Actions publishing source, GitHub stores the custom domain in Pages
settings; a `CNAME` file is not used. See the
[GitHub custom domain documentation](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site).

## Assets

The wordmark and token illustration are original SVGs. `social.png` is the
1200 × 630 sharing image and should be updated when the headline or art changes.
Instrument Sans is distributed under the SIL Open Font License, included at
`site/assets/OFL.txt`.

Keep private notes, decks, customer information and credentials out of this
public repository.
