# Commands Reference

Type in `{p}help` in discord to get a list of commands. Nonetheless, here is a list of commands that are currently available on the selfbot. Commands are grouped categorically.

### Key  
`{p}` - To be repalced with your prefix    
`[ ]` - Optional Parameters     
`< >` - Mandatory Parameters    

**Do not include these in your command**

# Information

| Command Name | Description | Usage |
| ------------- | ------------- | ------------- |
| about  | See information about the selfbot | `{p}about` |
| avatar  | Returns someone's avatar url | `{p}avatar [user]` |
| roleinfo | Shows information about a role | `{p}roleinfo <role name>` |
| serverinfo | See information about the server | `{p}serverinfo [server id]` |
| serverlogo | Return the server's icon url | `{p}serverlogo` |
| userinfo | Get information about a member of a server | `{p}userinfo [user]` |
| emojis | Lists all emojis in a server | `{p}emojis` |

# Moderation
| Command Name | Description | Usage |
| ------------- | ------------- | ------------- |
| addrole |  Add a role to someone else. | `{p}addrole <user> <rolename>` |
| removerole | Remove a role from someone else. | `{p}removerole <user> <rolename>` |
| clean | Clean a number of your own messages | `{p}clean [number=10]` |
| purge | Clean a number of any messages. | `{p}purge <number>` |
| kick | Kick someone from the server. | `{p}kick <user> [reason]` |
| ban  |  Ban someone from the server. | `{p}ban <user> [reason]` |
| unban | Unban someone from the server. | `{p}unban <user>` |
| baninfo | Check the reason of a ban from the audit logs. | `{p}baninfo <username>` |
| bans | See a list of banned users in the guild. | `{p}bans` |

# Miscellaneous
| Command Name | Description | Usage |
| ------------- | ------------- | ------------- |
| algebra | Solve algabraic equations | `{p}algebra <equation>` |
| animate | Animate a text file on discord! | `{p}animate <file.txt>` |
| annoy | Want to annoy a member with mentions? | `{p}annoy [user] [num]` |
| bf | Evaluate 'brainfuck' code (a retarded language). | `{p}bf <code>` |
| calc | Basic Calculator [+ , - , / , x] | `{p}calc [operator] [numbers...]` |
| dcolor | Shows the dominant color of an image | `{p}dcolor <imageurl>` | 
| 8ball | Ask questions to the 8ball | `{p}8ball <question>` |
| emoji | Use emojis without nitro! | `{p}emoji <emojiname>` |
| lenny | Lenny and tableflip group commands | `{p}lenny [face]` |
| react | React to a message with reactions | `{p}react <index> [emojis...]` |
| color | Enter a color and you will see it! | `{p}color <color>` |
| tinyurl | Shorten long urls quickly | `{p}tinyurl <url>` |
| urban | Searches up something in Urban Dictionary | `{p}urban <word>` |
| virus | Destroy someone's device with this command! | `{p}virus [user] [virus]` |

# Utility
| Command Name | Description | Usage |
| ------------- | ------------- | ------------- |
| py | Quick command to edit into a codeblock. | `{p}py <code>` |
| charinfo | Shows you information about characters. | `{p}charinfo [chars...` |
| copy | Copy someones message by ID | `{p}copy <id> [channel]`
| embed | Send complex rich embeds with this command! | `Read support server pins` |
| google | Searches google and gives you top result. | `{p}google <searchterms>` |
| help |  Shows the bot's help message. | `{p}help [command/cog]` |
| logout | Shuts down the selfbot | `{p}logout` |
| presence | Change your Discord status! | `{p}presence <status> [message]` |
| quote | Quote someone's message by ID | `{p}quote <message_id> [channel]` |
| translate | Translate text using google translate! | `{p}translate <language> <text...>`
| wiki | Addictive wikipedia results | `{p}wiki <search_terms...>` |

# Developer
| Command Name | Description | Usage |
| ------------- | ------------- | ------------- |
| rtfm | Gives you a documentation link for a discord.py entity | `{p}rtfm <entity>` |
| source | See the source code for any command. | `{p}source <command>` |
| eval | Execute python code on discord! | `{p}eval <code>` |

!> Warning! The `eval` command is extremely dangerous. Never use it unless you know exactly what you are doing. Improper use of this command can lead to leaked tokens or API abuse which in turn can get your account terminated.
