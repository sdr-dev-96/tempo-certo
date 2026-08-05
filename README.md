# Tempo Certo

Sends a daily Telegram notification (6:00 AM on weekdays, 7:30 AM on weekends) with:
- whether to close/reopen the shutters and windows, and when — covers both
  hot weather (close before peak heat, reopen once it cools down) and
  cold + windy weather (keep windows closed to avoid drafts/heat loss)
- a clothing suggestion based on the day's weather (temperature, rain, wind, UV)

Built on the free [Open-Meteo](https://open-meteo.com/) API (no API key required).

## 1. Installation

```bash
git clone <this repo> tempo-certo   # or just copy the files
cd tempo-certo
python3 -m venv venv
source venv/bin/activate
pip install .
cp .env.example .env
```

## 2. Configuration

Non-secret settings live in `config.py` — open it and adjust:

- `HOT_THRESHOLD_C`, `INDOOR_COMFORT_TEMP_C`: shutter close/reopen thresholds (hot weather)
- `SUN_EXPOSURE_START_HOUR` / `END_HOUR`: the window when direct sun hits your home
- `COLD_THRESHOLD_C`, `WINDY_THRESHOLD_KMH`: thresholds for the cold + windy window-closing advice
- `NOTIFY_METHOD`: `"telegram"` (recommended), `"ntfy"`, or `"email"`
- `FALLBACK_NOTIFY_METHODS`: methods to try, in order, if `NOTIFY_METHOD` fails to
  send (e.g. `["ntfy"]`); empty by default

Secrets and environment-specific values live in `.env` (gitignored — never
committed). Copy `.env.example` to `.env` and fill in the values below;
`config.py` loads them automatically via `python-dotenv`.

- `LATITUDE` / `LONGITUDE`: your coordinates (find them at latlong.net)
- `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID`: see Option A below
- `NTFY_TOPIC`: see Option B below
- `SMTP_HOST` / `SMTP_PORT` / `SMTP_USER` / `SMTP_PASSWORD` / `SMTP_FROM` / `SMTP_TO`: see Option C below
- `DRY_RUN`: `1` to test without sending a notification, `0` by default (see below)

### Option A — Telegram (recommended)

1. Open Telegram, search for **@BotFather**, send `/newbot` and follow the steps.
   You'll get a bot token that looks like `123456789:ABCDefGhIJKlmNoPQRsTUVwxyZ`.
2. Set that value as `TELEGRAM_BOT_TOKEN` in `.env`.
3. Send any message to your new bot (search for it by the username you gave it).
4. Open this URL in a browser, replacing `<TOKEN>` with your bot token:
   `https://api.telegram.org/bot<TOKEN>/getUpdates`
5. Look for `"chat":{"id": 123456789, ...}` in the response and copy that number
   into `TELEGRAM_CHAT_ID` in `.env`.

### Option B — ntfy.sh (no account needed)

1. Pick a unique, hard-to-guess topic name, e.g. `tempo-certo-a8f3k2`
2. Set it as `NTFY_TOPIC` in `.env`, and set `NOTIFY_METHOD = "ntfy"` in `config.py`
3. Install the **ntfy** app on your phone (iOS/Android) and subscribe to that topic
   (or simply open `https://ntfy.sh/<your-topic>` in a browser)

### Option C — Email (SMTP)

Fill in the `SMTP_*` fields in `.env` and set `NOTIFY_METHOD = "email"` in `config.py`.
For Gmail, you'll need to generate an "app password" (not your regular password):
https://myaccount.google.com/apppasswords

## 3. Manual test

```bash
python -m tempo_certo
```

You should see the message printed in the terminal AND receive the notification.

## 4. Test sans envoi (dry-run)

Pour tester le script sans déclencher de vraie notification (utile pour
vérifier la config ou le contenu du message), lance :

```bash
DRY_RUN=1 python -m tempo_certo
```

Le message est toujours affiché dans le terminal, mais `notify()` n'est pas
appelée. Fonctionne aussi avec `DRY_RUN=1` mis directement dans `.env`.

## 5. Automation with cron

Edit your crontab:

```bash
crontab -e
```

Add (adjust paths to your setup):

```cron
# Tempo Certo — 6:00 AM on weekdays (Monday to Friday)
0 6 * * 1-5 cd /path/to/tempo-certo && venv/bin/python -m tempo_certo >> logs.txt 2>&1

# Tempo Certo — 7:30 AM on weekends (Saturday, Sunday)
30 7 * * 6,0 cd /path/to/tempo-certo && venv/bin/python -m tempo_certo >> logs.txt 2>&1
```

Make sure cron runs in the expected timezone (`TZ=Europe/Paris` can be added at
the top of your crontab if your server is in a different timezone):

```cron
TZ=Europe/Paris
0 6 * * 1-5 cd /path/to/tempo-certo && venv/bin/python -m tempo_certo >> logs.txt 2>&1
30 7 * * 6,0 cd /path/to/tempo-certo && venv/bin/python -m tempo_certo >> logs.txt 2>&1
```

> ⚠️ **Mise à jour d'un déploiement existant** : ce projet est passé d'un
> script plat (`tempo_certo.py`) à un package (`tempo_certo/`), lancé via
> `python -m tempo_certo`. Après avoir mis à jour le repo sur le VPS,
> pense à :
> 1. relancer `pip install .` dans le venv (remplace `requirements.txt`) ;
> 2. **modifier la ligne de cron existante** pour utiliser
>    `venv/bin/python -m tempo_certo` au lieu de
>    `venv/bin/python3 tempo_certo.py`.

## 6. Rotation des logs

`logs.txt` grossit indéfiniment si rien ne le nettoie. Installe la config
logrotate fournie (adapte d'abord le chemin de `logs.txt` dans le fichier à
ton installation réelle) :

```bash
sudo cp tempo-certo-logrotate.conf /etc/logrotate.d/tempo-certo
```

## 7. Ideas for future evolution

- Factor in rain forecast for the next few hours (not just daily max)
- Specific heatwave / weather alert notifications
- History of recommendations (SQLite) to fine-tune thresholds over time
- Lightweight web UI (Flask) to tweak config without touching the code
- Multi-user / multi-home support (several configs, several Telegram chats)
- Home Assistant integration to auto-close motorized shutters

## Project files

```
tempo-certo/
├── tempo_certo/            # the package — run with `python -m tempo_certo`
│   ├── __init__.py
│   ├── __main__.py         # entry point (weather fetch, windows/clothing logic, notification)
│   ├── config.py           # non-secret configuration (thresholds, notification)
│   ├── i18n.py               # fr/en strings for the notification message
│   ├── weather_api.py       # Open-Meteo fetch + parsing
│   ├── windows_advice.py    # shutters/windows logic
│   ├── clothing_advice.py   # outfit logic
│   ├── message_builder.py   # assembles the final notification text
│   ├── notifiers.py         # Telegram / ntfy / email sending
│   └── log_setup.py         # daily log file + stdout logging
├── tests/                   # unit tests (pure logic, no network calls)
├── .env                     # secrets and environment-specific values (coordinates, bot tokens, passwords, chat IDs); gitignored, create it from `.env.example`
├── .env.example             # template for `.env`, safe to commit
├── tempo-certo-logrotate.conf  # logrotate config for `logs.txt`
├── pyproject.toml           # project metadata + dependencies (`requests`, `python-dotenv`)
└── README.md                # this file
```

Run the test suite with:

```bash
pip install pytest
pytest
```
