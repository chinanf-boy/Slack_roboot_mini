import os
import time
from slackclient import SlackClient

# starterbot 的 ID 作为一个环境变量
BOT_ID = os.environ.get("BOT_ID")
# 常量
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"
# 实例化 Slack 和 Twilio 客户端
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command with numbers, delimited by spaces."
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!" + command

    # 返回信息
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # 返回 @ 之后的文本，删除空格
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                    output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 3  # 1 从 firehose 读取延迟 1 秒
    if slack_client.rtm_connect():
        print("Mini connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            
            if command and channel:
                print('command:', command, 'channel:', channel)
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
