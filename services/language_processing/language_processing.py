def detect_tone(text):
    """Detect writing style and emotional tone with comprehensive word lists"""
    tone_indicators = {
        "academic": [
            "furthermore", "moreover", "consequently", "thus", "therefore", "nevertheless",
            "nonetheless", "accordingly", "subsequently", "hence", "thereby", "whereas",
            "notwithstanding", "hereby", "therein", "thereof", "thereto", "wherein",
            "demonstrates", "illustrates", "indicates", "suggests", "reveals", "establishes",
            "determines", "identifies", "examines", "analyzes", "evaluates", "assesses",
            "investigates", "explores", "discusses", "elaborates", "formulates", "hypothesizes",
            "postulates", "theorizes", "conceptualizes", "operationalizes", "validates",
            "evidence", "data", "research", "study", "analysis", "findings", "results",
            "empirical", "theoretical", "methodological", "statistical", "quantitative",
            "qualitative", "systematic", "comprehensive", "rigorous", "substantial",
            "framework", "paradigm", "hypothesis", "methodology", "phenomenon", "variable",
            "correlation", "causation", "implication", "significance", "limitation",
            "contribution", "perspective", "context", "parameter", "constraint",
            "significantly", "notably", "importantly", "interestingly", "remarkably",
            "predominantly", "approximately", "relatively", "comparatively", "particularly",            
        ],
        
        "casual": [
            "like", "just", "well", "so", "okay", "alright", "hey", "oh", "hmm", "uh", "um",
            "basically", "actually", "literally", "seriously", "honestly", "totally",
            "absolutely", "definitely", "probably", "maybe", "perhaps", "kinda", "sorta",
            "don't", "doesn't", "didn't", "isn't", "aren't", "wasn't", "weren't", "won't",
            "wouldn't", "couldn't", "shouldn't", "haven't", "hasn't", "hadn't", "can't",
            "ain't", "gonna", "wanna", "gotta", "lemme", "let's", "y'all", "dunno",
            "you know", "i mean", "you see", "look", "listen", "guess what", "by the way",
            "anyway", "anyways", "alright", "cool", "awesome", "great", "nice", "sweet",
            "fun", "weird", "crazy", "insane", "ridiculous", "hilarious", "sucks",
            "yeah", "yep", "nope", "nah", "uh-huh", "nuh-uh", "duh", "dude", "guys",
            "folks", "peeps", "stuff", "things", "something", "anything", "nothing",
            "super", "uber", "mega", "extra", "hella", "wicked", "mad", "crazy", "insane",
            "literally", "figuratively", "honestly", "truthfully", "frankly", "bluntly"
        ],
        
        "persuasive": [
            "must", "should", "ought", "need to", "have to", "got to", "has to",
            "cannot", "will not", "shall", "would", "could", "may", "might",
            "clearly", "obviously", "undoubtedly", "certainly", "definitely", "absolutely",
            "positively", "surely", "truly", "indeed", "without doubt", "without question",
            "proves", "demonstrates", "shows", "reveals", "confirms", "validates",
            "guarantees", "ensures", "assures", "promises", "delivers",
            "because", "since", "as", "for", "given that", "considering that",
            "due to", "owing to", "thanks to", "as a result of", "in light of",
            "critical", "crucial", "essential", "vital", "necessary", "imperative",
            "paramount", "obligatory", "mandatory", "required", "compulsory",
            "advantage", "benefit", "opportunity", "solution", "improvement", "enhancement",
            "transformation", "breakthrough", "innovation", "revolution", "evolution",
            "remember", "imagine", "consider", "think about", "reflect on", "realize",
            "recognize", "understand", "appreciate", "acknowledge", "admit", "agree",
            "especially", "particularly", "specifically", "notably", "remarkably",
            "extraordinarily", "exceptionally", "uniquely", "distinctly", "decidedly"
        ],
        
        "storytelling": [
            "once", "suddenly", "immediately", "instantly",
            "meanwhile", "in the meantime", "during", "throughout", "as", "while",
            "eventually", "finally", "ultimately", "in the end", "at last", "after all",
            "first", "second", "third", "next", "then", "after", "before", "earlier",
            "later", "subsequently", "previously", "initially", "ultimately",
            "wondered", "realized", "noticed", "observed", "felt", "thought", "remembered",
            "recalled", "imagined", "dreamed", "hoped", "wished", "desired", "longed",
            "dark", "light", "shadow", "silence", "whisper", "echo", "sound", "noise",
            "glance", "stare", "look", "gaze", "sight", "scene", "view", "landscape",
            "happy", "sad", "angry", "afraid", "excited", "nervous", "anxious", "calm",
            "peaceful", "restless", "tired", "energetic", "hopeful", "desperate",
            "then", "now", "later", "soon", "shortly", "presently", "currently",
            "formerly", "historically", "traditionally", "originally",
            "decided", "chose", "opted", "selected", "picked", "determined", "resolved",
            "committed", "pledged", "vowed", "swore", "promised", "agreed",
            "said", "asked", "replied", "answered", "whispered", "shouted", "yelled",
            "screamed", "murmured", "muttered", "exclaimed", "declared", "announced"
        ],
        
        "technical": [
            "algorithm", "data", "analysis", "process", "system", "software", "hardware",
            "interface", "protocol", "framework", "architecture", "component", "module",
            "function", "method", "class", "object", "variable", "parameter", "argument",
            "database", "server", "client", "network", "cloud", "storage", "memory",
            "processor", "bandwidth", "latency", "throughput", "capacity", "performance",
            "execute", "implement", "deploy", "configure", "optimize", "initialize", "terminate",
            "compile", "debug", "test", "validate", "verify", "authenticate", "authorize",
            "encrypt", "decrypt", "compress", "decompress", "parse", "serialize",
            "percentage", "ratio", "proportion", "average", "median", "mean", "mode",
            "standard deviation", "variance", "correlation", "coefficient", "frequency",
            "magnitude", "dimension", "scale", "range", "threshold", "limit", "boundary",
            "efficient", "scalable", "robust", "reliable", "secure", "stable", "compatible",
            "modular", "customizable", "extensible", "maintainable", "documented",
            "asynchronous", "synchronous", "concurrent", "parallel", "distributed",
            "quantify", "measure", "calculate", "compute", "estimate", "approximate",
            "determine", "derive", "extract", "generate", "produce", "transform",
            "firstly", "secondly", "finally", "subsequently", "consequently",
            "additionally", "furthermore", "moreover", "likewise", "similarly",
            "if and only if", "provided that", "assuming that", "given that",
            "under condition", "in case of", "whenever", "wherever", "whereby",
            "input", "output", "throughput", "feed", "feedback", "loop", "iteration",
            "recursion", "optimization", "simulation", "emulation", "virtualization"
        ],
        
        "emotional": [
            "happy", "joyful", "delighted", "pleased", "thrilled", "ecstatic", "elated",
            "excited", "enthusiastic", "passionate", "hopeful", "optimistic", "grateful",
            "thankful", "appreciative", "content", "satisfied", "fulfilled", "peaceful",
            "sad", "unhappy", "depressed", "miserable", "heartbroken", "devastated",
            "angry", "furious", "enraged", "livid", "frustrated", "annoyed", "irritated",
            "anxious", "nervous", "worried", "concerned", "stressed", "overwhelmed",
            "scared", "frightened", "terrified", "horrified", "disgusted", "ashamed",
            "feel", "felt", "sense", "sensed", "experience", "experienced", "suffer",
            "endure", "cherish", "treasure", "value", "despise", "loathe", "adore",
            "deeply", "truly", "honestly", "sincerely", "genuinely", "profoundly",
            "utterly", "completely", "totally", "absolutely", "extremely",
            "understand", "relate", "connect", "empathize", "sympathize", "support",
            "care", "love", "hurt", "pain", "suffering", "struggle", "challenge",
            "lonely", "isolated", "abandoned", "rejected", "accepted", "welcomed",
            "belonging", "appreciated", "valued", "respected", "admired", "loved"
        ]
    }
    
    # Count occurrences for each tone
    detected = {}
    text_lower = text.lower()
    
    for tone, indicators in tone_indicators.items():
        # Count each indicator (avoid double-counting overlapping phrases)
        count = 0
        for indicator in indicators:
            if indicator in text_lower:
                # Weight longer phrases more heavily
                weight = len(indicator.split())  # Number of words in phrase
                count += max(1, weight)  # At least 1 point, more for phrases
        detected[tone] = count
    
    # Return the highest scoring tone, or "neutral" if all are zero
    if any(detected.values()):
        # Add a small threshold - at least 2 points to register
        max_tone = max(detected, key=detected.get)
        if detected[max_tone] >= 1:
            return max_tone
    
    return "neutral"