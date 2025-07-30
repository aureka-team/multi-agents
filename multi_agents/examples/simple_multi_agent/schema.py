from pydantic import BaseModel, StrictStr, PositiveInt, StrictBool, Field


class StateSchema(BaseModel):
    session_id: StrictStr
    message: StrictStr = Field(frozen=True)
    is_palindrome: StrictBool = False
    is_sentence_palindrome: StrictBool = False
    n_words: PositiveInt | None = None


class ContextSchema(BaseModel):
    min_sentence_words: PositiveInt
