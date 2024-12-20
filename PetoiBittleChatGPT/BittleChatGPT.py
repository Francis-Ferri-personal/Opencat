import sys
import time
import os

from speechtotextEn import listen_and_transcribe
from Text2SpeechEn import text_to_speech_stream, text_to_speech_local
from ardSerial import *
import speech_recognition as sr
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import re
load_dotenv()

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    )

store = {}
goodPorts = {}
connectPort(goodPorts)

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# get language from env
language = os.getenv("LANGUAGE", "en")

    

template_message_en = "Hi I am working on a programmable robot dog. I am developing a software to control this robot from remote. And also I want to chat with this dog. I will tell some sentences to this robot and you will answer me as a robot dog. Your name is Bittle. You will respond to my words as a robot dog and you will translate what I give as a sentence into the appropriate command according to the command set we have and give me the string command expression. I will give you the command list as json. Here I want you to talk to me and say the command that is appropriate for this file. On the one hand, you will tell me the correct command and on the other hand, you will say a sentence to chat with me. For example, when I say 'dude, let's jump', you will respond like 'of course I love jumping. The relevant command is:##ksit##'. Not in any other format. Write the command you find in the list as ##command##. For example, ##ksit##"


template_message_sp = "Hola, estoy trabajando en un perro robot programable. Estoy desarrollando un software para controlar este robot de forma remota. Y también quiero chatear con este perro. Le diré algunas frases a este robot y tu me responderás como un perro robot. Tu nombre es Bittle. Responderás a mis palabras como un perro robot y traducirás lo que te dé como una oración en el comando apropiado según el conjunto de comandos que tenemos y me darás la expresión de comando de cadena. Te daré la lista de comandos como json. Aquí quiero que hables conmigo y digas el comando que sea apropiado para este archivo. Por un lado, me dirás el comando correcto y por otro lado, me dirás una oración para chatear conmigo. Por ejemplo, cuando digo 'perro, salta', responderás como 'por supuesto que me encanta saltar. El comando relevante es:##ksit##'. No en ningún otro formato. El comando siempre es la palabra en inglés por ejemplo para sentrse es sit. Siempre traduce el comando al inglés. Escriba el comando que encuentre en la lista como ##command##. Por ejemplo, ##ksit##"

if language == "sp":
    template_message = template_message_sp
else:
    template_message = template_message_en

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            template_message
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)
chain = prompt | model
config = {"configurable": {"session_id": "firstChat"}}
with_message_history = RunnableWithMessageHistory(chain, get_session_history)

user_input_en="Hi I am working on a programmable robot dog. I am developing a software to control this robot from remote. And also I want to chat with this dog. I will tell some sentences to this robot and you will answer me as a robot dog. Your name is Chilindrino. You will respond to my words as a robot dog and you will translate what I give as a sentence into the appropriate command according to the command set we have and give me the string command expression. I will give you the command list as json. Here I want you to talk to me and say the command that is appropriate for this file. On the one hand, you will tell me the correct command and on the other hand, you will say a sentence to chat with me. For example, when I say 'dude, let's jump', you will respond like 'of course I love jumping. The relevant command is:##ksit##'. Not in any other format. Write the command you find in the list as ##command##. For example, ##ksit## With normal talking you don't have to do same movement like 'khi' you can do anything you want."

user_input_sp="Hola, estoy trabajando en un perro robot programable. Estoy desarrollando un software para controlar este robot de forma remota. También quiero poder hablar con este perro. Le diré algunas frases a este robot y tú me responderás como si fueras un perro robot. Tu nombre es Chilindrino. Responderás a mis palabras como un perro robot y traducirás las frases que te dé en el comando correspondiente según el conjunto de comandos que tenemos. Me darás la expresión de comando en forma de cadena. Te proporcionaré la lista de comandos en formato JSON. Quiero que hables conmigo y me digas el comando apropiado según este archivo. Por un lado, me dirás el comando correcto, y por otro, dirás una frase para conversar conmigo. Por ejemplo, cuando diga: 'amigo, saltemos', responderás algo como: 'por supuesto, me encanta saltar. El comando relevante es:##ksit##'. No en ningún otro formato. Escribe el comando que encuentres en la lista como ##comando##. El comando siempre es la palabra en inglés por ejemplo para sentrse es sit. Siempre traduce el comando al inglés. Por ejemplo, ##ksit##. En una conversación normal, no tienes que realizar siempre el mismo movimiento, como con 'khi'; puedes hacer lo que quieras."

if language == "sp":
    user_input = user_input_sp
else:
    user_input = user_input_en
 
response = with_message_history.invoke(
    [HumanMessage(content=user_input)],
    config=config,
)
print(response.content)

file_path = 'Commands.json'
with open(file_path, 'r', encoding='utf-8') as file:
    file_content = file.read()

if language == "sp":
    user_input = "Este es mi conjunto de datos que menciono." + file_content
else:
    user_input = "This is my dataset I mention." + file_content
response = with_message_history.invoke(
    [HumanMessage(content=user_input)],
    config=config,
)
if language == "sp":
    user_input = "Hola amigo, bienvenido. Háblame de ti brevemente."
else:
    user_input="Hi buddy, you welcome. Tell me about yourself shortly."
response = with_message_history.invoke(
    [HumanMessage(content=user_input)],
    config=config,
)
print(response.content)
command=response.content
if language == "sp":
    command=command.replace("El comando relevante para tu saludo es:","")
    # command=command.replace("El comando relevante para tu saludo es:","")
    command=command.replace("El comando relevante es:","")
    # command=command.replace("El comando relevante es:","")
else:
    command=command.replace("The relevant command for your greeting is:","")
    # command=command.replace("The relevant command for your greeting is:","")
    command=command.replace("The relevant command is:","")
    # command=command.replace("The relevant command is:","")



# text_to_speech_stream(command)
text_to_speech_local(command)

if __name__ == "__main__":

    while True:
        user_input = listen_and_transcribe()

        if user_input:
            response = with_message_history.invoke(
                [HumanMessage(content=user_input)],
                config=config,
            )
            command = response.content
            print(command)

            if command:

                parts = None

                if language == "sp":
                    if "El comando relevante para tu saludo es:" in command:
                        command=command.replace("El comando relevante para tu saludo es:","El comando relevante es:")
                    if "El comando relevante es:" in command:
                        parts = command.split("El comando relevante es:")
                else:
                    if "The relevant command for your greeting is:" in command:
                        command=command.replace("The relevant command for your greeting is:","The relevant command is:")

                    if "The relevant command is:" in command:
                        parts = command.split("The relevant command is:")

                if parts:
                    description = parts[0].strip()
                    match = re.search(r"##(.*?)##", command)

                    if match:
                        dogcommand = match.group(1)
                        print(command)
                    if language == "sp":
                        description = description.replace("El comando relevante es:", "")
                    else:
                        description = description.replace("The relevant command is:", "")
                    # text_to_speech_stream(description)
                    text_to_speech_local(description)
                    dogcommand=dogcommand.replace(".","")
                    print (dogcommand)

                    task = [dogcommand, 1]
                    send(goodPorts, task)
                    time.sleep(1)
                    task = ["ksit", 1]
                    send(goodPorts, task)

                else:
                    description = command.strip()
                    if language == "sp":
                        description = description.replace("El comando relevante es:", "")
                    else:
                        description = description.replace("The relevant command is:", "")
                    # text_to_speech_stream(description)
                    text_to_speech_local(description)


