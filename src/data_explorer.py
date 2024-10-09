import json
import sys
import os

class JSONFileConverterError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class JSONFileConverter:
    @staticmethod
    def get_dict_of_json_file(filename:str)-> dict[str]:
        messages= None
        try:
            with open(filename,"r",encoding="utf-8") as file:
                try:
                    messages = json.load(file)
                except json.decoder.JSONDecodeError:
                    print(f"File '{filename}' is not valid JSON")
                    raise JSONFileConverterError(f"File '{filename}' is not valid JSON")
        except FileNotFoundError:
            raise JSONFileConverterError(f"File Not Found. {filename}")
        return messages


class DiscordMessagesInfo:
    CHANNEL_FILENAME = "channel.json"
    MESSAGES_FILENAME= "messages.json"
    SERVER_AUDITLOG_FILENAME= "audit-log.json"
    SERVER_GUILDINFO_FILENAME= "guild.json"
    CHANNEL_ID_KEY= "id"
    CHANNEL_TYPE_KEY="type"
    CHANNEL_RECIPIENTS_KEY= "recipients"
    CHANNEL_TYPE_DM_VALUE= "DM"
    CHANNEL_TYPE_GUILD_VALUE= "GUILD_TEXT"
    CHANNEL_TYPE_THREAD_VALUE= "PUBLIC_THREAD"
    MESSAGES_ID_KEY= "ID"
    MESSAGES_TIMESTAMP_KEY= "Timestamp"
    MESSAGES_CONTENTS_KEY= "Contents"
    MESSAGES_ATTACHMENTS_KEY= "Attachments"


    def get_channel_and_message_ids(directory:str):
        for folder in os.walk(directory):
            channel = None
            messages = None
            message_ids = []
            path,subfolders,files = folder

            for file in files:
                message_ids = []
                if DiscordMessagesInfo.CHANNEL_FILENAME in files and DiscordMessagesInfo.MESSAGES_FILENAME in files:
                    try:
                        channel= JSONFileConverter.get_dict_of_json_file(f"{path}{os.sep}{DiscordMessagesInfo.CHANNEL_FILENAME}")
                        messages= JSONFileConverter.get_dict_of_json_file(f"{path}{os.sep}{DiscordMessagesInfo.MESSAGES_FILENAME}")
                    except JSONFileConverterError:
                        print(f"{path}{os.sep}{file}  failed to convert")

                        if messages:
                            for message in messages:
                                message_ids.append(message[DiscordMessagesInfo.MESSAGES_ID_KEY])
                            
                            with open(f"{path}{os.sep}{channel[DiscordMessagesInfo.CHANNEL_ID_KEY]}_channel_and_message_ids.txt","w") as file:
                                file.write(f"{channel[DiscordMessagesInfo.CHANNEL_ID_KEY]}:\n")
                                [file.write(f"{message}, ") for message in message_ids]
                else:
                    continue


def main():
    #try:
    #    argv_1 = sys.argv[1]
    #except:
    #    print("Not enough arguments. Usage: python get_messageIDs.py <filename>")
    #    sys.exit()
    DiscordMessagesInfo.get_channel_and_message_ids("./")
            

if __name__ == "__main__":
    main()


