mport random
import re
from datetime import datetime

BOT_NAME = "CodBot"

# Each rule: (list of regex patterns, list of possible responses).
# Rules are checked in order, so more specific rules come first.
RULES = [
    # Goodbyes (checked first so "bye" is never treated as small talk)
    (
        [r"\b(bye|goodbye|see you|exit|quit)\b"],
        ["Goodbye! Keep coding!", "See you later! Happy learning!", "Bye! Come back soon."],
    ),
    # Greetings
    (
        [r"\b(hi|hello|hey|hola|namaste)\b", r"good (morning|afternoon|evening)"],
        ["Hello! How can I help you today?", "Hi there! What can I do for you?", "Hey! Nice to see you."],
    ),
    # How are you
    (
        [r"how are you", r"how('s| is) it going", r"what'?s up"],
        ["I'm doing great, thanks for asking! How about you?", "All good here! How can I help?"],
    ),
    # Bot's name / identity
    (
        [r"your name", r"who are you", r"what are you"],
        [f"I'm {BOT_NAME}, a rule-based chatbot built for the CodSoft AI internship."],
    ),
    # Capabilities
    (
        [r"what can you do", r"\bhelp\b", r"your (features|abilities)"],
        [
            "I can chat, tell you the time or date, explain AI basics, "
            "share a joke, and tell you about the CodSoft internship. Try asking!"
        ],
    ),
    # Time
    (
        [r"\btime\b"],
        ["__TIME__"],
    ),
    # Date
    (
        [r"\b(date|today|day is it)\b"],
        ["__DATE__"],
    ),
    # CodSoft info
    (
        [r"\bcodsoft\b", r"internship"],
        [
            "CodSoft is a tech education platform offering virtual internships. "
            "For the AI internship you complete at least 3 tasks and share them on GitHub and LinkedIn."
        ],
    ),
    # AI basics
    (
        [r"what is (ai|artificial intelligence)"],
        [
            "Artificial Intelligence is the field of building machines that can perform tasks "
            "that normally need human intelligence, like learning, reasoning and understanding language."
        ],
    ),
    (
        [r"what is (ml|machine learning)"],
        ["Machine Learning is a part of AI where computers learn patterns from data instead of being explicitly programmed."],
    ),
    (
        [r"what is (nlp|natural language processing)"],
        ["NLP (Natural Language Processing) helps computers understand, interpret and generate human language."],
    ),
    # Programming
    (
        [r"\bpython\b"],
        ["Python is a beginner-friendly language and the most popular choice for AI and data science."],
    ),
    # Jokes
    (
        [r"\bjoke\b", r"make me laugh"],
        [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "Why did the developer go broke? Because he used up all his cache.",
            "There are 10 types of people: those who understand binary and those who don't.",
        ],
    ),
    # Thanks
    (
        [r"\b(thanks|thank you|thx)\b"],
        ["You're welcome!", "Happy to help!", "Anytime!"],
    ),
    # Positive / negative feelings
    (
        [r"\b(good|great|fine|awesome|happy)\b"],
        ["Glad to hear that!", "That's wonderful!"],
    ),
    (
        [r"\b(sad|bad|tired|angry|stressed)\b"],
        ["I'm sorry to hear that. Take a short break, you've got this!"],
    ),
]

FALLBACKS = [
    "Sorry, I didn't understand that. Could you rephrase it?",
    "Hmm, I'm not sure about that. Type 'help' to see what I can do.",
    "I'm a simple bot and I don't know that one yet. Try asking something else!",
]


def get_response(user_input: str) -> str:
    """Return a response by matching the input against the rules."""
    text = user_input.lower().strip()

    if not text:
        return "Please type something so I can respond."

    for patterns, responses in RULES:
        for pattern in patterns:
            if re.search(pattern, text):
                reply = random.choice(responses)
                if reply == "__TIME__":
                    return f"The current time is {datetime.now().strftime('%I:%M %p')}."
                if reply == "__DATE__":
                    return f"Today's date is {datetime.now().strftime('%A, %d %B %Y')}."
                return reply

    return random.choice(FALLBACKS)


def is_goodbye(user_input: str) -> bool:
    return bool(re.search(r"\b(bye|goodbye|exit|quit)\b", user_input.lower()))


def main():
    print("=" * 50)
    print(f"  {BOT_NAME} - Rule-Based Chatbot (CodSoft Task 1)")
    print("  Type 'bye' to exit. Type 'help' for ideas.")
    print("=" * 50)

    while True:
        user_input = input("You: ")
        print(f"{BOT_NAME}: {get_response(user_input)}")
        if is_goodbye(user_input):
            break


if __name__ == "__main__":
    main()
