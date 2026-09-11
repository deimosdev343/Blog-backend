from config import TORMENT_NEXUS_KEY
from openai import OpenAI
from dto.suggest_text_dto import transfromTextInput, SuggestTextInput, ExpandSuggestInput
client = OpenAI(api_key=TORMENT_NEXUS_KEY)
from services.language_processing.language_processing import detect_tone
import yake


ACTION_RULES ={ 
  "improve":"""
    Rewrite the passage so it reads better: tighter phrasing, stronger verbs,
    less hedging, smoother rhythm. Keep every fact, claim and opinion the
    writer made. Do not add new ideas or examples of your own.
  """,
  "shorten":"""
      Cut the passage down while keeping every idea it contains. Remove filler,
    redundancy and throat-clearing rather than content. Aim for roughly
    {short_target} words; never exceed {word_count} words.
  """,
  "expand": """
    Develop the passage further. Keep the writer's existing sentences intact in
    substance and add supporting detail, a concrete example, or the reasoning
    behind a claim. Aim for roughly {long_target} words. Do not introduce facts,
    statistics, names or dates that could be wrong — stay at the level of
    reasoning and illustration.
  """,
  "grammar": """
    Fix only what is incorrect: spelling, grammar, punctuation, verb agreement
    and obvious typos. This is a correction pass, not a rewrite. Preserve the
    writer's word choice, sentence structure, voice and any deliberate
    informality. If a sentence is already correct, return it unchanged.
  """,
  "tone": """
    Rewrite the passage in a {tone} register. Keep the same meaning, the same
    facts and roughly the same length. Change diction and sentence shape, not
    substance.
  """,
}

TONE_GUIDES = {
    "professional": "measured and precise, no slang, no exclamation marks",
    "casual": "relaxed and conversational, contractions welcome, like talking to a friend",
    "confident": "direct and declarative, no hedging words like 'maybe', 'I think', 'sort of'",
    "plain": "simple and concrete, short sentences, no jargon or abstraction",
}

TEMPERATURES = {
    "improve": 0.5,
    "shorten": 0.3,
    "expand": 0.7,
    "grammar": 0.1,
    "tone": 0.6,
}


def extract_keywords(text):
    kw_extractor = yake.KeywordExtractor(top=5)
    keywords = kw_extractor.extract_keywords(text)
    return [kw for kw, score in keywords]


def transform_selection(data: transfromTextInput):
  selection = data.text.strip()
  context = data.context[-2500:]
  word_count = len(selection.split())
  if(data.action == "tone"):
    tone_line = f"traget register {data.tone} - {TONE_GUIDES[data.tone]}."
  else:
    try:
      detected = detect_tone(context) if len(context.split()) > 30 else None
    except Exception:
      detected = None
    tone_line = (
      f"The surrounding post reads as: {detected}. Match it."
      if detected
      else "Match the voice of the surrounding post."
    )
    keywords_str = ", ".join(extract_keywords(context)) if context.strip() else ""
     
    rule = ACTION_RULES[data.action].format(
        word_count=word_count,
        short_target=max(5, int(word_count * 0.6)),
        long_target=int(word_count * 1.8),
        tone=data.tone,
    )
  
