from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class ConversationTurn:
    turn_id: int
    speaker: str
    text: str


@dataclass
class Conversation:
    turns: List[ConversationTurn] = field(default_factory=list)

    @property
    def turn_count(self) -> int:
        return len(self.turns)

    @property
    def full_text(self) -> str:
        return "\n".join(
            f"{turn.speaker}: {turn.text}"
            for turn in self.turns
        )

    def add_turn(self, speaker: str, text: str):
        turn = ConversationTurn(
            turn_id=len(self.turns) + 1,
            speaker=speaker,
            text=text.strip()
        )

        self.turns.append(turn)

    def get_text_turns(self) -> List[str]:
        """
        Returns only the text of each turn.

        This preserves compatibility with the current
        DistilBERT + BiLSTM training pipeline.
        """
        return [turn.text for turn in self.turns]

    def get_speakers(self) -> List[str]:
        return [turn.speaker for turn in self.turns]

    def truncate(self, max_turns: int) -> "Conversation":
        """
        Return a new conversation containing at most max_turns.
        """
        return Conversation(
            turns=self.turns[:max_turns]
        )

    def to_dict(self) -> Dict:
        return {
            "turn_count": self.turn_count,
            "turns": [
                {
                    "turn_id": turn.turn_id,
                    "speaker": turn.speaker,
                    "text": turn.text
                }
                for turn in self.turns
            ]
        }


def parse_conversation(text: str) -> Conversation:
    """
    Parse a simple conversation transcript.

    Supported examples:

        Person 1: Hello
        Person 2: Hi

        Speaker 1: Hello
        Speaker 2: Hi

        User: Hello
        Scammer: You need to act now

        Victim: I don't understand
        Attacker: Give me your OTP

    If no speaker label is detected, the line is treated
    as an unknown speaker.
    """

    conversation = Conversation()

    lines = text.splitlines()

    known_speakers = {
        "person",
        "speaker",
        "user",
        "assistant",
        "victim",
        "suspect",
        "scammer",
        "attacker",
        "receiver",
        "sender",
        "a",
        "b"
    }

    for line in lines:

        line = line.strip()

        if not line:
            continue

        speaker = "unknown"
        message = line

        if ":" in line:

            possible_speaker, possible_message = line.split(
                ":", 1
            )

            candidate = possible_speaker.strip().lower()

            is_valid_speaker = False

            if candidate in known_speakers:
                is_valid_speaker = True

            else:
                # Handle:
                # Person 1
                # Speaker 2
                # User 1
                # etc.
                words = candidate.split()

                if len(words) == 2:
                    if (
                        words[0] in known_speakers
                        and words[1].isdigit()
                    ):
                        is_valid_speaker = True

            if is_valid_speaker:
                speaker = possible_speaker.strip()
                message = possible_message.strip()

        if message:
            conversation.add_turn(
                speaker=speaker,
                text=message
            )

    return conversation


if __name__ == "__main__":

    sample = """
    Person 1: Hello, I received your message.
    Person 2: Yes, I need your help immediately.
    Person 1: What happened?
    Person 2: Your account has been compromised.
    Person 1: What should I do?
    Person 2: Send me the verification code now.
    """

    conversation = parse_conversation(sample)

    print("Conversation:")
    print(conversation.to_dict())

    print()
    print("Turn count:", conversation.turn_count)

    print()
    print("Text turns:")
    for turn in conversation.get_text_turns():
        print("-", turn)