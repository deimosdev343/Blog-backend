import pytest
 
from services.language_processing.language_processing import detect_tone
 
KNOWN_TONES = {"academic", "casual", "technical", "emotional", "neutral", "storytelling"}
 
 
class TestDetectTone:
    def test_empty_text_is_neutral(self):
        assert detect_tone("") == "neutral"
 
    def test_text_with_no_indicators_is_neutral(self):
        assert detect_tone("Zzz qqq xyzzy plugh.") == "neutral"
 
    def test_recognises_academic_writing(self):
        text = (
            "The research demonstrates a significant correlation in the "
            "empirical data."
        )
        assert detect_tone(text) == "academic"
 
    def test_recognises_emotional_writing(self):
        text = "I felt lonely and heartbroken, but I am grateful and hopeful."
        assert detect_tone(text) == "emotional"
 
    def test_is_case_insensitive(self):
        lower = detect_tone("i felt lonely and heartbroken and grateful")
        upper = detect_tone("I FELT LONELY AND HEARTBROKEN AND GRATEFUL")
        assert lower == upper
 
    def test_always_returns_a_known_label(self):
        """The return value is interpolated straight into a prompt, so it
        should never be something the model has to guess at."""
        for text in ["", "Zzz qqq.", "I felt sad.", "The data suggests."]:
            result = detect_tone(text)
            assert detect_tone(text) in KNOWN_TONES
 
    def test_the_stronger_signal_wins(self):
        mostly_emotional = (
            "I felt lonely, heartbroken, anxious and overwhelmed, but the "
            "data helped."
        )
        assert detect_tone(mostly_emotional) == "emotional"
 
    def test_substring_matching_produces_false_positives(self):
        assert detect_tone("Unsaddle the horse.") != "neutral"
 
