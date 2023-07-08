# proof of concept
import sys

# import logging
import subprocess
import os
from slack_notifications import Slack

SUCCESS = "{} has pushed on the dashboard repo succesfully"
FAILED = (
    "{} does not implement the naming convention\n please rename the branch correctly"
)
CHAN = "#photon-repo"
BOT = "PTBOT"


def analyze(msg: str, tokens: list[str] = ["EM", "dev"]) -> bool:
    if msg in tokens:
        return True
    return False


if __name__ == "__main__":
    slack = Slack(os.environ["STK"])
    current_branch_name = subprocess.getoutput("git branch --show-current")
    commit_msg = subprocess.getoutput("git log -1 --pretty=%B")

    if not analyze(current_branch_name):
        slack.send_notify(CHAN, username=BOT, text=FAILED.format(current_branch_name))
        sys.exit(1)
    else:
        slack.send_notify(CHAN, username=BOT, text=SUCCESS.format(current_branch_name))
