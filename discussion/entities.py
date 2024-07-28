from dataclasses import dataclass
from typing import List


@dataclass
class TagCreateServiceEntity:
    name: str

@dataclass
class DiscussionCreateServiceEntity:
    description: str
    image: str
    tags: List[TagCreateServiceEntity]