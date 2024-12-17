"""
cmd_table_[xx] : dict{ str:str }
    Key represents the result of speech recognition(voice command).
    Value represents the corresponding Petoi command.
"""


# ===================================== Spanish(es-es) ====================================
cmd_table_es = {
    'mentir': 'knd',
    'sentarse': 'ksit',
    'por favor, siéntate': 'ksit',
    'ponerse de pie': 'kbalance',
    'levantarse': 'kbalance',
    'caminar hacia adelante': 'kwkF',
    'correr hacia adelante': 'ktrF',
    'verificar estado': 'c',
    'descansar': 'rest',
    'agacharse': 'd',
    'detenerse': 'd',
}


def build_dict_es(cmd_table):
    """Esto es para Español.

    Construye una lista personalizada de palabras de cmd_table para que el modelo de vosk elija al reconocer.

    Parámetros
    ----------
    cmd_table : dict{ str:str }
        Descripción como se indica arriba.

    Devuelve
    -------
    d : str
        La forma en cadena de una lista personalizada de palabras.
    """

    d = []
    keys = cmd_table.keys()
    for k in keys:
        d += k.split(' ')
    d = list(set(d))
    d = [" ".join(d), "[unk]"]
    d = str(d).replace("'", "\"")
    print(d)
    return d
# ===================================== Spanish(es-es) ====================================


# ===================================== English(en-us) ====================================
cmd_table_en = {
    'lies': 'knd',
    'sit down': 'ksit',
    'please sit': 'ksit',
    'stand up': 'kbalance',
    'get up': 'kbalance',
    'walk forward': 'kwkF',
    'run forward': 'ktrF',
    'check status': 'c',
    'rest': 'rest',
    'get down': 'd',
    'stop': 'd',
}


def build_dict_en(cmd_table):
    """This is for English.

    Build a custom list of words from cmd_table for vosk model to choose from when recognizing.

    Parameters
    ----------
    cmd_table : dict{ str:str }
        Description as above.

    Returns
    -------
    d : str
        The str form of a custom list of words.
    """

    # return '["get status down please walk sit forward check rest stand up run stop", "[unk]"]'
    # print("[\"get status down please walk sit forward check rest stand up run stop\", \"[unk]\"]")
    d = []
    keys = cmd_table.keys()
    for k in keys:
        d += k.split(' ')
    d = list(set(d))
    d = [" ".join(d), "[unk]"]
    d = str(d).replace("'", "\"")
    print(d)
    return d
# ===================================== English(en-us) ====================================



def text2cmd(text, cmd_table):
    """Convert the result of speech recognition into Petoi command.

    Parameters
    ----------
    text : str
        The result from vosk model after speech recognition.

    cmd_table : dict{ str:str }
        Description as above.

    Returns
    -------
    An str. The corresponding Petoi command.
    """

    return cmd_table.get(text, '')
