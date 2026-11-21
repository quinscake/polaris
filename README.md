# Polaris

A one-file project tracker for projects, research and classes. Every day you write one line about what moved, and Polaris turns those lines into a timeline, a week view and gentle reminders.

## What's in it

- **Week** (the home screen): five days that roll with you, from 2 days back to 2 days ahead. Each day shows what you logged and what's due. Tap **+ Log** on a day to add something for it. The toolbar shows how many days in a row you've logged something and how many updates you made this week.
- **Timeline**: every project as a line, with a dot for each update, a ◆ for each milestone, a flag for the final deadline and an ✕ when it ends. Ended projects sink to the bottom and leave the board a week later.
- **Table**: all projects and updates, searchable and editable.
- **Areas**: Research, Class, Project and Personal by default. Rename them or add your own in **Table → Edit areas**, and filter the Timeline by area.
- **Milestones**: several dated checkpoints per project (assignments, exams, submissions). Each one gets a reminder 3 days before. The **final deadline** is separate: once that day is over, the project ends itself.
- **Reminders** (the yellow bars): milestones and deadlines coming up, projects that have gone quiet for 5+ days, and a recap of last week from Monday to Wednesday. Each one can be dismissed.

The whole app is `index.html`: HTML, CSS and JavaScript in one file. There's no build step, nothing to install, and no server of your own. The only outside things it loads are fonts from Google Fonts (Unbounded, Geist and Geist Mono). Without internet it falls back to system fonts.

---

## Three ways to run it

| Where | How | Where your data is saved |
|---|---|---|
| **Your computer** | Double-click `index.html`. It opens in your browser. | In that browser, unless you turn on GitHub sync |
| **Your own website** (GitHub Pages) | Upload this folder to a GitHub repository and switch on Pages (steps below) | GitHub sync, so every device sees the same board |
| **Inside Claude** | Your existing Polaris link on claude.ai | Inside the Claude page itself |

The three copies don't share data with each other automatically. Pick one as your home. To move a board from one to another, use **Backup → Copy backup** in the old one and **Backup → Restore** in the new one.

---

## Recommended setup: your own website + data saved in GitHub

You'll make **two repositories**:

- **`polaris`** (public) holds the app. GitHub Pages turns it into a website. Free Pages sites must be public, but that's fine: the app has no data in it.
- **`polaris-data`** (private) holds `data.json`, your actual board. Only you, and anything you give a token to, can read it.

### 1. Create the data repository

1. On github.com click **+ → New repository**.
2. Name it `polaris-data`, choose **Private**, tick **Add a README file**, and click **Create repository**.
3. Click **Add file → Upload files** and upload `data.json` from the `polaris-data` folder in this download. That's your current board. Click **Commit changes**.

### 2. Create an access token for Polaris

1. Open <https://github.com/settings/personal-access-tokens/new> (Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token).
2. **Token name:** `Polaris`. **Expiration:** up to you (a year is fine; GitHub emails you before it expires).
3. **Repository access:** *Only select repositories* → `polaris-data`.
4. **Permissions → Repository permissions → Contents:** *Read and write*.
5. Click **Generate token** and copy it (it starts with `github_pat_`). You only see it once, so keep it in a password manager.

### 3. Put the app online

1. Create another repository called `polaris`, this time **Public**.
2. **Add file → Upload files**: upload `index.html` and this `README.md`. Commit.
3. Go to **Settings → Pages**. Under *Build and deployment*, set **Source** to *Deploy from a branch*, pick **main** and **/ (root)**, then **Save**.
4. After about a minute your tracker is live at:
   **`https://YOUR-USERNAME.github.io/polaris/`**

Bookmark it on your PC. On your phone, open it and choose **Add to Home Screen** (iPhone: Share button → Add to Home Screen; Android: ⋮ menu → Add to Home screen). It gets the Polaris star icon and opens full screen like an app.

On iPhone, the home-screen app keeps its own storage, separate from Safari, so do step 4 below once inside the home-screen app too.

### 4. Connect Polaris to your data

1. Open your Polaris website and click **GitHub sync** (top right; on a phone it's in the **⋯** menu).
2. **Data repository:** `YOUR-USERNAME/polaris-data`. **Branch:** `main`. **File:** `data.json`.
3. Paste your token and click **Connect**. Your board loads, and the top right says *Saved to GitHub*.

Do step 4 once on each device or browser you use. From then on, every change is saved to GitHub within a couple of seconds as a commit, so `polaris-data` keeps the full history of everything you've done. When you switch back to the tab, Polaris checks GitHub for changes you made on another device.

Anyone who finds your website address only sees an empty board. Your data loads only with your token.

---

## Giving Claude access

1. On claude.ai go to **Settings → Connectors**, connect **GitHub**, and allow the Claude GitHub app to access `polaris` and `polaris-data`.
2. In any chat, ask Claude to open `YOUR-USERNAME/polaris` (and `polaris-data` if it should see your board).

Claude can then change the app and push the new version, and your website updates by itself a minute later. It can also read `data.json`, for example to summarize your week or check upcoming deadlines.

---

## Running it only on your computer

Double-click `index.html`. That's all. Your board is saved in that browser. Use **Backup** now and then, or turn on GitHub sync (steps 1, 2 and 4 above; step 3 isn't needed), which works from a file on your computer too.

To keep the source code in sync with GitHub on your computer, you can also clone the repository:

```
git clone https://github.com/YOUR-USERNAME/polaris.git
```

and open `polaris/index.html`.

---

## On a phone

The layout switches automatically on screens narrower than 640px:

- The **Week** tab lists today first, then the next two days, then the two days before.
- On the **Timeline**, each project's name sits above its line, so the line uses the full width, and it starts on the one-week range.
- The update box is a bar at the bottom of the screen, like a chat app. It always logs for today. To add an update for an earlier day, tap **+ Log** on that day in the Week tab, or tap that day on the project's line.
- Tap an update to read, edit or add more. Pop-ups slide up from the bottom.
- The **Table** tab shows projects and updates as cards.
- **GitHub sync** and **Backup** are in the **⋯** menu at the top right.

---

## How the data is stored

`data.json` is plain JSON:

```json
{
  "v": 2,
  "rev": 12,
  "title": "Polaris",
  "areas": [ { "id": "research", "name": "Research" } ],
  "projects": [
    { "id": "mwq3y07bbxii4o", "name": "ESL Grant", "color": 0,
      "start": "2026-11-16", "ended": null, "deadline": "2026-11-30", "endedBy": null,
      "area": "research",
      "milestones": [ { "id": "m1", "title": "Budget section", "date": "2026-11-22", "done": false } ] }
  ],
  "updates": [
    { "id": "mwq3y8k24hf5h9", "projectId": "mwq3y07bbxii4o", "date": "2026-11-17", "text": "Something" }
  ]
}
```

- `rev` goes up by one with every change. When two copies differ, the higher `rev` wins.
- `ended` is the end date (`null` while active). `endedBy` is `"deadline"` when the project ended itself.
- Dates are `YYYY-MM-DD` in your local time.

Don't edit `data.json` by hand while Polaris is open: the next save from the app replaces it.

## Settings you can change in the code

Near the top of the `<script>` in `index.html`:

| Setting | Default | What it does |
|---|---|---|
| `KEEP_DAYS` | `7` | Days an ended project stays on the board |
| `DUE_SOON` | `3` | Days before a deadline or milestone when the reminder appears |
| `DRIFT_DAYS` | `5` | Days without an update before a project counts as quiet |
| `FUTURE` | `{7:3, 14:4, 30:7}` | Days shown after today on the Timeline, for each zoom level |

## Security notes

- The token is stored in your browser (localStorage) on each device where you connect. Use a fine-grained token limited to `polaris-data` only, as above.
- You can revoke the token any time at <https://github.com/settings/personal-access-tokens>. Polaris then falls back to saving in the browser until you connect a new one.
- On a shared or public computer, click **GitHub sync → Disconnect** when you're done.
