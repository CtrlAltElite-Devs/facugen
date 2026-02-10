from typing import TypedDict, Literal


Label = Literal["positive", "neutral", "negative"]
LangType = Literal[
    "english",
    "tagalog",
    "cebuano",
    "taglish",
    "ceb_eng_mix",
]


class Sample(TypedDict):
    text: str
    label: Label
    lang_type: LangType
