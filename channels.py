
from consts import *

from telethon.sync import TelegramClient
from telethon.tl.functions.channels import CreateChannelRequest, InviteToChannelRequest, EditAdminRequest, GetAdminLogRequest
from telethon.tl.types import ChatAdminRights
from telethon.tl.functions.messages import ExportChatInviteRequest
# from telethon.tl.functions.channels import EditPhotoRequest
from telethon.tl.types import InputChatUploadedPhoto
# from telethon.tl.functions.channels import EditChannelRequest


client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# data = ['Изнасилование в семейном ресторане',
# 'Ryoujoku Famiresu Choukyou Menu', '2010',
# '2', '#Straight #Oral #Big_tits #Anal #Rape #Virgin #Waitresses',
#  '#Есть', 'Субтитры #Русская_Озвучка',
#  'Изнасилование в семейном ресторане ',
#   'Ryojoku Family Restaurant Chokyo Menu - ']



async def create_private_channel(channel_title, channel_description, client):

  try:
    # Create a new private channel
    result = await client(CreateChannelRequest(
      title=channel_title,
      about=channel_description,
      broadcast=True,  # Set to True to make it a broadcast channel
      megagroup=False,  # Set to False for a private channel 2091954420
    ))

    # Get the newly created channel ID
    channel_id = result.chats[0].id

    print("Private channel created successfully!", channel_id)
    return channel_id
  except Exception as e:
    print(f"Error: {e}")


async def add_users_to_channel(channel_id, user_phone_numbers, client):


  try:
    # Get information about the channel
    channel_entity = await client.get_entity(channel_id)

    # Add users to the channel
    await client(InviteToChannelRequest(
    channel=channel_entity,
    users=user_phone_numbers,  # List of phone numbers of users to add
    ))

    print("Users added to the channel successfully!")

  except Exception as e:
    print(f"Error: {e}")


async def get_user_id_by_name_or_number(user_input, client):

  try:
    # Search for the user by first name or phone number
    result = await client.get_entity(user_input)

    return result.id

  except Exception as e:
    print(f"Error: {e}")
    return None


async def promote_to_admin(channel_id, user_input, client):
  user_id = await get_user_id_by_name_or_number(user_input, client)

  try:
    # Get information about the channel
    channel_entity = await client.get_entity(channel_id)

    # Define the admin rights
    admin_rights = ChatAdminRights(
      post_messages=True,
      delete_messages=True,
      ban_users=True,
      invite_users=True,
      pin_messages=True,
      change_info=True,
      add_admins=True,
      anonymous=True,
      post_stories=True,
      edit_stories=True,
      delete_stories=True,
      edit_messages=True,
      manage_call=True,
      manage_topics=True,
      other=True,
      )
    # print(admin_rights)

    # Promote the user to admin
    await client(EditAdminRequest(
      channel=channel_entity,
      user_id=user_id,
      admin_rights=admin_rights,
      rank='',  # Optional: custom admin title
    ))

    print("User promoted to admin successfully!")

  except Exception as e:
    print(f"Error: {e}")


async def generate_invite_link(channel_id, client):
  # Get information about the channel
  channel_entity = await client.get_entity(channel_id)

  # Generate the invite link for the channel
  result = await client(ExportChatInviteRequest(channel_entity))

  # The invite link is available in result.link
  invite_link = result.link
  print("Invite link:", invite_link)
  return invite_link


async def make_channel(data, client):

  channel_id = await create_private_channel(data[0] + " | " +data[1], "", client)

  user_phone_numbers = ['+998333286839',]

  await add_users_to_channel(channel_id, user_phone_numbers, client)
  await promote_to_admin(channel_id, user_phone_numbers[0], client)
  invite_link = await generate_invite_link(channel_id, client)
  return channel_id, invite_link


async def make_channel_and_add_bot(channel_title, descriptions="", bot_url=MAIN_BOT):
    channel_id = await create_private_channel(channel_title, descriptions, client)
    await promote_to_admin(channel_id, bot_url, client)
    return channel_id

def make_private_channel(channel_title, descriptions="", bot_url=MAIN_BOT):
  with client:
    return client.loop.run_until_complete(make_channel_and_add_bot(channel_title, descriptions="", bot_url=MAIN_BOT))
async def main():
    # channel_id = -1001145760050
    # channel_id, invite_link = await make_channel()
    # print(channel_id, invite_link)
    # user_input = 'My33_328 (Humans)'
    # photo_path = IMAGES + 's-ke-ni-totsuida-m-jou-no-nich.jpg'

    i = await make_channel_and_add_bot("TEST2" )
    print(i)
    # a = await add_users_to_channel(channel_id, ['https://t.me/mkclone_bot'], client)
    # a = await promote_to_admin(channel_id, 'https://t.me/sender2chanel_bot', client)
    # a = await get_referral_links(channel_id)
    # print(a)


if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
