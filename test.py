# speed test.py
# Mark Lowerison.  Downloads a 100m file every 15 mins for 2 d and logs the mb/s to slack.


import requests
import sys
import time
import os
from subprocess import call
from slackclient import SlackClient

# Slack Notifier Stuff
bot_slack_token = "xoxb-412355015472-535475665268-qkFNYWekgkx5b0IO62tofYaO"

slack = SlackClient(bot_slack_token)
thread = slack.api_call(
    "chat.postMessage", channel="CFCCHRH0F", text=f"Starting Speed Test at Jers."
)


def downloadFile(url, directory):
    localFilename = url.split("/")[-1]
    with open(directory + "/" + localFilename, "wb") as f:
        start = time.clock()
        r = requests.get(url, stream=True)
        total_length = r.headers.get("content-length")
        dl = 0
        if total_length is None:  # no content length header
            f.write(r.content)
        else:
            for chunk in r.iter_content(1024):
                dl += len(chunk)
                f.write(chunk)
                done = int(50) * dl / int(total_length)
    return time.clock() - start


def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = "http://speedtest.wdc01.softlayer.com/downloads/test10.zip"
    directory = "."

    time_elapsed = downloadFile(url, directory)
    call(f"rm -f test100.zip", shell=True)
    speed = 11.5 / time_elapsed

    slack.api_call(
        "chat.postMessage",
        channel="CFCCHRH0F",
        thread_ts=thread["ts"],
        text=f"{speed}",
    )


if __name__ == "__main__":
    for i in range(1, 200):
        main()
        time.sleep(60*15)
