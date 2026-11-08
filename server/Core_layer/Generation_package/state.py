from typing import Any, Optional, TypedDict


class DialogueState(TypedDict, total=False):
    text: str
    user: str
    chat_id: Optional[str]
    pltype: str
    platform: str
    message: Any
    commands: Any
    route: str
    rag_context: Optional[str]
    answer: str
    history: list
    is_image: bool
    gradius_chat_id: str
    gradius_user_id: str
    existing_ad_count: int
    stream_id: str
    should_persist: bool
    message_id: Optional[str]
    update_message_id: Optional[str]
    skip_ads: bool
