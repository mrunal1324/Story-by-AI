import time
import re
import requests

def extract_genre_from_prompt(prompt):
    prompt_lower = prompt.lower()
    if any(word in prompt_lower for word in ["romance", "love", "relationship", "couple"]):
        return "romance"
    elif any(word in prompt_lower for word in ["space", "alien", "galaxy", "future", "robot", "sci-fi", "science fiction"]):
        return "sci-fi"
    elif any(word in prompt_lower for word in ["magic", "dragon", "wizard", "elf", "kingdom", "fantasy", "mythical"]):
        return "fantasy"
    elif any(word in prompt_lower for word in ["murder", "detective", "crime", "mystery", "clue", "investigation"]):
        return "mystery"
    elif any(word in prompt_lower for word in ["history", "historical", "century", "ancient", "medieval", "renaissance"]):
        return "historical"
    elif any(word in prompt_lower for word in ["horror", "scary", "ghost", "monster", "fear", "terror"]):
        return "horror"
    return "general"

def generate_story(prompt, length="Medium", creativity=0.85, use_ai=True):
    start_time = time.time()
    genre = extract_genre_from_prompt(prompt)
    print(f"Detected genre: {genre}")

    prompt_template = f"""Write a short, creative story titled: "{prompt}"

Story:"""


    try:
        if use_ai:
            response = requests.post(
                'http://localhost:11434/api/generate',
                json={
                    "model": "phi",
                    'prompt': prompt_template,
                    "num_predict": 250,  # or even 200 for Short
                    "stream": False
                }
            )
            story_text = response.json()['response']
            story_text = re.sub(r'[^.!?]*$', '', story_text).strip()
            print(f"Story generation took {time.time() - start_time:.2f} seconds")
            return story_text
    except Exception as e:
        print(f"Ollama failed, using fallback. Error: {e}")

    return generate_fallback_story(prompt, genre)

def generate_fallback_story(prompt, genre="general"):
    """
    Generate a high-quality fallback story based on genre.
    
    Args:
        prompt (str): The user's story prompt
        genre (str): The detected genre
        
    Returns:
        str: A manually crafted story based on the genre
    """
    if genre == "romance":
        return """In a bustling city, two strangers crossed paths in an unexpected way. Their eyes met, and something sparked between them - a connection neither could explain.

As days turned into weeks, they found themselves drawn to each other, sharing stories, dreams, and eventually, their deepest fears. Their relationship blossomed despite the obstacles life threw their way.

Through misunderstandings and reconciliations, they discovered that love wasn't just about the perfect moments, but about choosing each other every day. In the end, they realized that some connections are simply meant to be, transcending all logic and reason."""

    elif genre == "sci-fi":
        return """In the distant future, humanity had spread across the stars, establishing colonies on countless worlds. On a remote outpost at the edge of known space, a discovery was made that would change everything.

A researcher uncovered an ancient alien artifact, dormant for millennia but still pulsing with mysterious energy. As the team began to study it, strange phenomena occurred - equipment malfunctioned, and team members reported vivid dreams of distant worlds.

When they finally activated the device, it revealed a startling truth: humanity was not alone in the universe, and an ancient race had left this beacon as both a warning and an invitation. The future of human civilization now hung in the balance of what they would do next."""

    elif genre == "fantasy":
        return """In a realm where magic flowed through every living thing, a young apprentice discovered an ancient tome hidden beneath the floorboards of the wizard's library. The book, bound in dragon hide and inscribed with forgotten runes, called to them with an irresistible whisper.

Against their master's warnings, they began to decipher the spells within - magic that had been forbidden for centuries. With each incantation mastered, they grew more powerful, but also awakened forces long dormant.

As shadows gathered and ancient enemies stirred, the apprentice realized too late the responsibility that came with such power. Now, they alone held the knowledge that could either save their world or plunge it into darkness."""

    elif genre == "mystery":
        return """The small coastal town had always kept its secrets well, but when three people vanished without a trace during the autumn festival, those secrets began to surface.

A detective arrived from the city, methodically piecing together clues that locals seemed eager to overlook. Strange symbols found at each disappearance site, whispered conversations that stopped when strangers approached, and a pattern that seemed to repeat every fifty years.

As the investigation deepened, the detective uncovered a pact made generations ago - one that demanded sacrifice in exchange for prosperity. Now, with time running out before another victim was taken, they raced to break a cycle that had held the town captive for centuries."""

    elif genre == "historical":
        return """Florence, 1478. The city was alive with the spirit of the Renaissance, as artists and thinkers breathed new life into the ancient wisdom of Greece and Rome. Among them was a young apprentice to the great Verrocchio, whose talent had begun to outshine even his master's.

The apprentice found himself drawn into the dangerous politics of the Medici family, who ruled Florence with wealth and cunning. When he discovered a hidden message in a commissioned painting - a warning of conspiracy against Lorenzo de' Medici - he was faced with a terrible choice.

To reveal what he knew would place him in the path of powerful enemies, yet to remain silent might doom the patron who had supported artists throughout the city. As the Pazzi conspiracy unfolded around him, the young artist's decisions would not only determine his own fate but influence the course of Florence itself."""

    elif genre == "horror":
        return """The old house at the end of Willow Street had stood empty for decades. Local children dared each other to touch its rusted gate, but none ventured inside. When a young couple purchased it for a surprisingly low price, the neighbors watched with quiet concern but said nothing of its history.

As renovation began, strange occurrences plagued the couple - tools disappeared, rooms grew inexplicably cold, and whispers seemed to echo through empty hallways. In the basement, behind a crumbling wall, they discovered a small door sealed with unusual symbols.

Curiosity overcame caution, and they broke the seal. That night, the lights in the old house blazed until dawn, but when morning came, the couple was nowhere to be found. Only a journal remained, its final entry a frantic warning: "It was never the house that was haunted."""

    else:  # General fiction
        return """The letter arrived on an ordinary Tuesday, its handwriting familiar yet from a past almost forgotten. As they turned the envelope over in their hands, memories flooded back - of summers long ago, of promises made in youth, and of paths that had diverged.

Inside was an invitation, simple but life-changing: a chance to return to the place where everything had begun, to reunite with those who had once known them best. The decision to go wasn't easy, but something pulled them back - perhaps curiosity, perhaps nostalgia, or perhaps the feeling that something had been left unfinished.

The journey back revealed how much had changed, both in the landscape of their hometown and within themselves. Yet in reconnecting with old friends and confronting long-buried truths, they discovered that some bonds transcend time and distance, and that it's never too late to find closure or to begin again."""