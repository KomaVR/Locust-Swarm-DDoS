# Locust-Swarm-DDoS

Locust-Swarm-DDoS is an automated, distributed HTTP stress testing system using Discord, GitHub Actions, and Locust. You can trigger high-scale, controlled load tests via Discord slash commands that deploy workers using GitHub's free CI infrastructure — no servers required.

## Features

- Slash command support via Discord (`/stress`)
- Distributed Locust setup (master + multiple workers)
- No infrastructure required — runs fully on GitHub Actions
- Customizable user behavior through Locust tasks
- Secure API and token handling via GitHub Secrets

## Project Structure

```

Locust-Swarm-DDoS/
├── bot.py                     # Discord bot that triggers GitHub Actions
├── stress_test.py            # Locust scenarios
├── requirements.txt          # Python dependencies
└── .github/
└── workflows/
├── load-test.yml     # Workflow to deploy the distributed test
└── run-bot.yml       # Workflow to run the Discord bot

```

## Setup Instructions

### 1. Fork the Repo

Start by forking this repo to your own GitHub account.

### 2. Add GitHub Secrets

Navigate to **Settings > Secrets and variables > Actions** and add the following:

| Name            | Description                                                      |
|-----------------|------------------------------------------------------------------|
| DISCORD_TOKEN   | Your Discord bot token                                           |
| PAT_TOKEN       | GitHub Personal Access Token (with `repo` and `workflow` scopes) |
| REPO_OWNER      | Your GitHub username                                             |
| REPO_NAME       | Repository name (e.g. `Locust-Swarm-DDoS`)                       |

## Usage

Once the bot is running, use the following slash command in Discord:

```

/stress
url: [https://target.site]
users: 200
spawn_rate: 20
workers: 5
run_time: 2m
```

This will trigger:
- A GitHub Actions workflow
- A Locust master + 5 workers
- A headless test on the specified target

## Load Scenarios

The `stress_test.py` file defines the behavior of virtual users:

- `GET /search?q=`: Sends randomized queries to a search endpoint
- `POST /api/process`: Sends large randomized JSON payloads

You can modify or extend these to fit your application's endpoints.

## Run Locally (Optional)

To run the Discord bot locally:

```

pip install -r requirements.txt
python bot.py

```

To run Locust locally:

```

locust -f stress_test.py

```

## Disclaimer

This tool is for educational and authorized testing purposes only. You must have explicit permission to test any targets. Misuse of this tool can be illegal and unethical.

## License

MIT License
