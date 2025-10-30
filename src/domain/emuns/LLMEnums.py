from enum import Enum



class IntFloat(Enum):
    SYSTEM = "system: "
    ASSISTANT = "passage: "
    QUERY = "query: "


class EmbedEnums(Enum):
    PROVIDERS_NAMES = ["INTFLOAT", ]
    INTFLOAT = IntFloat


    PROVIDERS = [INTFLOAT, ]



class DefaultEmbedEnums(Enum):
    SYSTEM = "system: "
    ASSISTANT = "assistant: "
    QUERY = "query: "


