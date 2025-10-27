from pydantic import BaseModel, Field

class BasePromptModel(BaseModel):
    """Base model for prompt templates."""
    user_messages: str = Field(..., description="The user's input to be included in the prompt.")
    system_messages: str | None = Field("", description="Optional administrative messages to guide the model's response.")
    
    def template(self) -> list[dict[str, str]]:
        """Return the prompt template string."""
        return [
            {"role": "user", "content": self.user_messages},
            {"role": "system", "content": self.system_messages or ""}
        ]