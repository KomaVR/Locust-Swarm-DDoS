import os
import discord
from discord import app_commands
from discord.ext import commands
from github import Github
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
PAT_TOKEN     = os.environ["PAT_TOKEN"]
REPO_OWNER    = os.environ["REPO_OWNER"]
REPO_NAME     = os.environ["REPO_NAME"]
WORKFLOW_FILE = os.environ["WORKFLOW_FILE"]
REF           = os.environ.get("REF", "main")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

gh = Github(PAT_TOKEN)
repo = gh.get_repo(f"{REPO_OWNER}/{REPO_NAME}")

async def dispatch_locust_workflow(url: str, users: int, spawn_rate: int, workers: int, run_time: str):
    workflow = repo.get_workflow(WORKFLOW_FILE)
    workflow.create_dispatch(
        ref=REF,
        inputs={
            "HOST": url,
            "USERS": str(users),
            "SPAWN_RATE": str(spawn_rate),
            "WORKERS": str(workers),
            "RUN_TIME": run_time
        }
    )

@bot.tree.command(name="stress", description="Kick off a distributed Locust stress test")
@app_commands.describe(
    url="The target URL to test",
    users="Total number of virtual users",
    spawn_rate="Spawn rate (users per second)",
    workers="Number of worker processes",
    run_time="Duration (e.g. 5m, 1h)"
)
async def stress(interaction: discord.Interaction, url: str, users: int, spawn_rate: int, workers: int, run_time: str):
    await interaction.response.defer(thinking=True)
    try:
        await dispatch_locust_workflow(url, users, spawn_rate, workers, run_time)
        await interaction.followup.send(
            f"🚀 Stress test requested!\n"
            f"• Target: `{url}`\n"
            f"• Users: `{users}` @ `{spawn_rate}` u/s\n"
            f"• Workers: `{workers}`\n"
            f"• Duration: `{run_time}`\n"
            f"Watch the GitHub Actions workflow for progress."
        )
    except Exception as e:
        await interaction.followup.send(f"❌ Failed to dispatch workflow: `{e}`", ephemeral=True)

bot.run(DISCORD_TOKEN)
