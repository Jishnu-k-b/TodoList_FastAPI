from pydantic import BaseModel, Field


class Todo(BaseModel):
    task_title: str = Field(default=None)
    task_description: str = Field(default=None)

    class Config:
        scheme_extra = {
            "task": {
                "task_title": "The title",
                "task_description": "The description",
            }
        }
