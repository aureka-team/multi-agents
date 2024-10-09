from pydantic import BaseModel, StrictStr, PositiveInt, StrictBool, Field


class StateSchema(BaseModel):
    message: StrictStr = Field(frozen=True)
    is_palindrome: StrictBool = False
    is_sentence_palindrome: StrictBool = False
    n_words: PositiveInt | None = None


class ConfigSchema(BaseModel):
    min_sentence_words: PositiveInt
