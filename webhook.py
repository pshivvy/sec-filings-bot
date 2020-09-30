from discord_webhook import DiscordWebhook, DiscordEmbed

# will be used to make function to embed messages.

def send_data(hookrl: str, title: str, type: str, datetime: str, filingUrl: str):
    webhook = DiscordWebhook(url=hookrl)

    # create embed object for webhook
    embed = DiscordEmbed(title=title, description=filingUrl, color=00000)
    embed.set_footer(text='Filed on: ' + datetime)
    # add embed object to webhook
    webhook.add_embed(embed)

    webhook.execute()