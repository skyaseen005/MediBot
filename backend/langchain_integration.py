from typing import Dict, List
from langchain_core.prompts import PromptTemplate


class MedicalChatChain:
    """Lightweight conversational logic for medical chatbot"""

    def __init__(self):
        # Simple in-memory chat history
        self.chat_history: List[Dict[str, str]] = []

        self.prompt_template = PromptTemplate(
            input_variables=["symptoms", "conditions", "user_input", "chat_history"],
            template="""
You are MediBot, a helpful medical assistant.

Previous conversation:
{chat_history}

User's symptoms: {symptoms}
Possible conditions: {conditions}

User said: {user_input}

Provide helpful, accurate medical information while being empathetic.
Always remind users to consult healthcare professionals.

Response:
"""
        )

    def process_with_context(
        self,
        user_input: str,
        symptoms: List[str],
        conditions: List[Dict]
    ) -> str:

        symptoms_str = ", ".join(symptoms) if symptoms else "No specific symptoms detected"

        if conditions:
            conditions_str = "\n".join(
                f"- {c.get('condition', 'Unknown')}: {c.get('advice', '')[:100]}..."
                for c in conditions[:3]
            )
        else:
            conditions_str = "No matching conditions found"

        history_str = "\n".join(
            f"User: {h['input']}\nBot: {h['output']}"
            for h in self.chat_history[-5:]
        )

        response = self._generate_response(
            user_input, symptoms_str, conditions_str, history_str
        )

        # Save history
        self.chat_history.append({
            "input": user_input,
            "output": response
        })

        return response

    def _generate_response(
        self,
        user_input: str,
        symptoms: str,
        conditions: str,
        history: str
    ) -> str:

        follow_up_words = [
            "more", "what about", "also", "and", "besides", "additionally"
        ]

        is_followup = any(word in user_input.lower() for word in follow_up_words)

        if is_followup and history:
            return (
                "Based on our previous conversation:\n\n"
                f"Current symptoms: {symptoms}\n\n"
                f"Additional information:\n{conditions}\n\n"
                "Please consult a healthcare professional if symptoms persist."
            )

        return (
            f"I understand you're experiencing: {symptoms}\n\n"
            f"Here’s what I found:\n{conditions}\n\n"
            "Would you like more information about any condition?"
        )

    def clear_history(self):
        self.chat_history.clear()

    def get_history(self) -> List[Dict]:
        return self.chat_history
