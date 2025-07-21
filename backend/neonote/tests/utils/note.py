import random
from sqlmodel import Session, select, desc
from neonote.repository.note_repository import _NoteRepository
from neonote.service.note_service import _NoteService
from neonote.models import Note, NoteCreate, User


def create_test_note(session: Session) -> Note:
    user = session.exec(select(User).order_by(desc(User.id)).limit(1)).one()
    service = _NoteService(user, _NoteRepository(session))
    todo = NoteCreate(
        title="test todo",
        content="test todo content",
    )
    service.create_note(todo)
    todo.title = "test 2 todo"
    created_todo = service.create_note(todo)
    return created_todo


def generate_random_paragraph(num_sentences=5, min_length=8, max_length=15):
    """
    Generates a random paragraph

    Args:
        num_sentences (int): Number of sentences in the paragraph
        longitud_min (int): Minimum length of words per sentence
        longitud_max (int): Maximum length of words per sentence

    Returns:
        str: Generated paragraph
    """

    subjects = [
        "The cat",
        "A dog",
        "The student",
        "My friend",
        "The teacher",
        "A bird",
        "The computer",
        "This book",
        "The weather",
        "A child",
        "The scientist",
        "The artist",
        "A musician",
        "The doctor",
        "The engineer",
        "A writer",
    ]

    verbs = [
        "runs",
        "walks",
        "jumps",
        "flies",
        "thinks",
        "works",
        "studies",
        "creates",
        "discovers",
        "explores",
        "builds",
        "writes",
        "reads",
        "sings",
        "dances",
        "teaches",
        "learns",
        "travels",
        "speaks",
        "listens",
    ]

    objects = [
        "quickly",
        "slowly",
        "carefully",
        "happily",
        "quietly",
        "loudly",
        "peacefully",
        "through the park",
        "in the garden",
        "at home",
        "in the library",
        "near the river",
        "under the tree",
        "on the mountain",
        "by the ocean",
        "in the city",
        "every day",
        "with enthusiasm",
        "with patience",
        "with dedication",
    ]

    adjectives = [
        "beautiful",
        "interesting",
        "complex",
        "simple",
        "amazing",
        "wonderful",
        "challenging",
        "exciting",
        "peaceful",
        "mysterious",
        "colorful",
        "bright",
        "ancient",
        "modern",
        "creative",
        "innovative",
        "traditional",
        "unique",
    ]

    nouns = [
        "story",
        "adventure",
        "journey",
        "experience",
        "moment",
        "opportunity",
        "challenge",
        "discovery",
        "solution",
        "problem",
        "idea",
        "concept",
        "project",
        "dream",
        "goal",
        "vision",
        "plan",
        "method",
        "approach",
    ]

    connectors = [
        "However",
        "Furthermore",
        "Moreover",
        "Additionally",
        "Nevertheless",
        "Consequently",
        "Therefore",
        "Meanwhile",
        "Subsequently",
        "In contrast",
        "For instance",
        "As a result",
        "On the other hand",
        "In addition",
    ]

    sentences = []

    for i in range(num_sentences):
        length = random.randint(min_length, max_length)

        # Basic sentence structure
        if i == 0:
            # First sentence without connector
            sentence = f"{random.choice(subjects)} {random.choice(verbs)}"
        else:
            # The following sentences can have a connector
            if random.random() < 0.3:  # 30% probability of using connector
                sentence = f"{random.choice(connectors)}, {random.choice(subjects).lower()} {random.choice(verbs)}"
            else:
                sentence = f"{random.choice(subjects)} {random.choice(verbs)}"

        # Add additional words until the desired length is reached
        current_words = len(sentence.split())
        while current_words < length:
            item = random.choice(
                [
                    random.choice(adjectives),
                    random.choice(objects),
                    random.choice(nouns),
                    f"a {random.choice(adjectives)} {random.choice(nouns)}",
                ]
            )
            sentence += f" {item}"
            current_words = len(sentence.split())

        # Ensure that the sentence ends with a period
        if not sentence.endswith("."):
            sentence += "."

        sentences.append(sentence)

    return " ".join(sentences)


def generate_random_paragraphs(
    num_paragraphs=3, sentences_per_paragraph=5, min_lenght=8, max_length=15
):
    paragraphs = []
    for _ in range(num_paragraphs):
        paragraph = generate_random_paragraph(
            sentences_per_paragraph, min_lenght, max_length
        )
        paragraphs.append(paragraph)

    return "\n\n".join(paragraphs)


def create_note_batch(
    service: _NoteService, archive: bool = False, trash: bool = False
) -> list[Note]:
    notes = []
    for i in range(10):
        notes.append(
            service.create_note(
                NoteCreate(
                    title=f"Note {i}",
                    content=generate_random_paragraphs(),
                ),
                archive=archive,
                trash=trash,
            )
        )
    return notes
