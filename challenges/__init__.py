from challenges.api_challenges import API_CHALLENGES
from challenges.automation_challenges import AUTOMATION_CHALLENGES
from challenges.async_challenges import ASYNC_CHALLENGES
from challenges.langchain_challenges import LANGCHAIN_CHALLENGES

ALL_CHALLENGES = (
    API_CHALLENGES
    + AUTOMATION_CHALLENGES
    + ASYNC_CHALLENGES
    + LANGCHAIN_CHALLENGES
)


def get_all_challenges():
    return ALL_CHALLENGES


def get_by_category(category: str):
    return [c for c in ALL_CHALLENGES if c["category"] == category]


def get_by_id(challenge_id: str):
    for c in ALL_CHALLENGES:
        if c["id"] == challenge_id:
            return c
    return None
