# LWTC Training site

The landing page (`index.html`) lists every training in the `training-assets/` folder.
Nobody edits the landing page to add a training.

## One-time setup (IT)

1. Put everything in this folder in the root of the GitHub repository (branch `main`).
2. In the repository, go to **Settings > Pages** and set **Source** to **GitHub Actions**.
3. Push. The **Publish training site** workflow runs and the site goes live.

## Adding a training (IT)

1. Get the training's HTML file. It must have its details in the `<head>` (see below).
   `training-assets/_template.html` is a starting point.
2. Upload it to the `training-assets/` folder on `main`.
3. Wait 1 to 2 minutes. The workflow rebuilds the list and the training appears on the landing page.

To change or remove a training, edit or delete the file in `training-assets/`.

## What goes in each training's `<head>`

```html
<title>Training title</title>
<meta name="training-date" content="2026-10-15">   <!-- required, YYYY-MM-DD -->
<meta name="description" content="One or two sentences on what participants will do.">
<meta name="training-minutes" content="60">        <!-- optional -->
<meta name="training-audience" content="Faculty and staff">   <!-- optional -->
<meta name="training-title" content="Short title">  <!-- optional, overrides <title> -->
```

If `training-date` is missing, a filename that starts with the date also works
(for example `2026-10-15-assessment-design.html`). A training with no date still
appears, at the bottom, marked "Date not set", and the workflow log shows a warning.

## How the page orders and labels trainings

- Trainings are sorted by training date, newest first.
- The newest training is shown at the top. It is labeled **Upcoming** if its date is after
  the visitor's computer date, and **Current** if it is today or earlier.
- Everything else is under **Earlier trainings**. An older entry that is dated in the
  future also gets an **Upcoming** tag.
- Labels are worked out in the visitor's browser, so they change on their own as dates pass.

## Drafts

Files whose names start with `_` (like `_template.html`) are never listed. Upload a
draft as `_my-draft.html`, review it by its direct address, then rename it to publish.

## Every training should link back

Near the top of each training page:

```html
<a href="../index.html">Back to LWTC Training</a>
```

## Settings

Near the top of the script in `index.html`: `FOLDER` (default `training-assets`) and
`LOGO_BASE` (where the LWTC logo files load from; if they cannot load, a text wordmark shows).

## Troubleshooting

- **A new training does not appear:** open the repository's **Actions** tab and check that the
  latest "Publish training site" run is green. A warning there names any file missing a date.
- **"Trainings could not be loaded":** the page must be opened from its github.io address,
  not from a saved copy. To test on a computer, run `python3 -m http.server` in this folder
  and open `http://localhost:8000`.
- **If the workflow is not set up yet:** the page falls back to asking GitHub for the folder
  listing. GitHub allows only 60 of these requests per hour per IP address, so a whole campus
  loading the page at once can hit the limit. Use the workflow.
