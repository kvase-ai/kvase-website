# kvase.ai

A small static landing page for Kvase, currently building in stealth. HTML and
CSS, with no client-side JavaScript or analytics.

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

The canonical domain is `kvase.ai`, with Cloudflare as authoritative DNS and
OnlyDomains remaining the registrar. To connect it:

1. Add `kvase.ai` to Cloudflare DNS. Review the imported records against the
   existing OnlyDomains zone before switching nameservers; preserve mail
   (including MX and any supporting A/TXT records) and unrelated subdomains.
2. Replace the old website records in the Cloudflare zone with these
   **DNS-only** records:

   | Type  | Name | Value              |
   | ----- | ---- | ------------------ |
   | A     | @    | 185.199.108.153    |
   | A     | @    | 185.199.109.153    |
   | A     | @    | 185.199.110.153    |
   | A     | @    | 185.199.111.153    |
   | CNAME | www  | kvase-ai.github.io |

3. Remove the old apex A/AAAA records and any conflicting `www` records from
   the Cloudflare zone. Confirm the old zone's DNSSEC/DS status before changing
   nameservers.
4. Set **Settings → Pages → Custom domain** to `kvase.ai`. At OnlyDomains,
   replace its three nameservers with the **two nameservers assigned to this
   exact Cloudflare zone**. Wait for Cloudflare to show the zone as active and
   verify that public DNS returns the GitHub Pages records.
5. Once GitHub provisions the certificate, enable **Enforce HTTPS** in Pages
   settings.

For the Actions publishing source, GitHub stores the custom domain in Pages
settings; a `CNAME` file is not used. See the
[GitHub custom domain documentation](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site).
Cloudflare's [full DNS setup](https://developers.cloudflare.com/dns/zone-setups/full-setup/setup/)
and [OnlyDomains delegation steps](https://support.onlydomains.com/hc/en-gb/articles/4406251623057-How-do-I-change-my-Name-Servers-delegate)
cover the nameserver handoff.

## Assets and claims

The cost and performance promise follows the September 2026 founder discussion
and pitch deck. The page says **up to 80%** because actual savings depend on
the workload. The black, off-white and lime identity follows the logo
variants shared by the team. The mark is a vector rendering of the three-arm
symbol used in the macOS app; the small menu illustration follows the app
screenshot while omitting personal account and development-server details.
`social.png` is the 1200 × 630 sharing image and should be updated when the
headline changes.

Keep private notes, decks, customer information and credentials out of this
public repository.
