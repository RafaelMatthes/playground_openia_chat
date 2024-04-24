from dataclasses import dataclass
from typing import Optional, List


@dataclass
class FilterResult:
    filtered: bool
    severity: str


@dataclass
class PromptFilterResult:
    detected: Optional[bool]
    filtered: bool


@dataclass
class DataItem:
    b64_json: Optional[str]
    revised_prompt: str
    url: str
    content_filter_results: dict[str, FilterResult]
    prompt_filter_results: dict[str, PromptFilterResult]


@dataclass
class ImageOutput:
    created: int
    data: List[DataItem]

    @classmethod
    def from_json(cls, json_data: dict):
        created = json_data.get("created")
        data = []
        if "data" in json_data:
            data = [DataItem(
                b64_json=item.get("b64_json"),
                revised_prompt=item["revised_prompt"],
                url=item["url"],
                content_filter_results={
                    key: FilterResult(**value) for key, value in item["content_filter_results"].items()
                },
                prompt_filter_results={
                    key: PromptFilterResult(**value) for key, value in item["prompt_filter_results"].items()
                }
            ) for item in json_data["data"]]
        return cls(created=created, data=data)


