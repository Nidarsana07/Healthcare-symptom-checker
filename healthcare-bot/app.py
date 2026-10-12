import os
import json
import re
from collections import Counter

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --------------------------------------------------
# 1. LOAD SYMPTOM DATASET
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "symptoms.json")

try:
    with open(JSON_PATH, "r", encoding="utf-8") as file:
        DATA = json.load(file)

    if not isinstance(DATA, list):
        raise ValueError("symptoms.json must contain a JSON list.")

    for item in DATA:
        if not isinstance(item, dict):
            raise ValueError("Every dataset entry must be an object.")

        if not all(key in item for key in (
            "condition", "symptoms", "severity", "advice"
        )):
            raise ValueError(
                "Every entry must contain condition, symptoms, "
                "severity and advice."
            )

        if not isinstance(item["symptoms"], list):
            raise ValueError("'symptoms' must be a list.")

except (OSError, json.JSONDecodeError, ValueError) as error:
    raise RuntimeError(
        f"Unable to load the symptom dataset at {JSON_PATH}: {error}"
    ) from error


# --------------------------------------------------
# 2. SYMPTOM ALIASES
# --------------------------------------------------

# Maps common user phrases to equivalent dataset symptoms.
SYMPTOM_ALIASES = {
    "runny nose": [
        "running nose",
        "nose is running",
        "nasal discharge"
    ],
    "chest pain": [
        "pain in my chest",
        "pain in the chest",
        "chest discomfort"
    ],
    "shortness of breath": [
        "difficulty breathing",
        "trouble breathing",
        "breathlessness",
        "cannot breathe",
        "can't breathe",
        "cant breathe"
    ],
    "sore throat": [
        "throat pain",
        "painful throat"
    ],
    "stomach pain": [
        "abdominal pain",
        "pain in my stomach",
        "stomach ache"
    ],
    "headache": [
        "head pain",
        "pain in my head"
    ],
    "high fever": [
        "very high temperature"
    ],
    "dizziness": [
        "feeling dizzy",
        "lightheaded"
    ],
    "vomiting": [
        "throwing up",
        "being sick"
    ],
    "diarrhea": [
        "diarrhoea",
        "loose stools",
        "loose motions"
    ],
    "blurred vision": [
        "blurry vision",
        "vision is blurry"
    ],
    "swelling of face": [
        "face swelling",
        "swollen face"
    ],
    "swelling of tongue": [
        "tongue swelling",
        "swollen tongue"
    ],
    "weakness on one side": [
        "one sided weakness"
    ],
    "slurred speech": [
        "speech is slurred"
    ]
}


# --------------------------------------------------
# 3. EMERGENCY WARNING PHRASES
# --------------------------------------------------

# A basic precautionary keyword screen, not a medical
# triage tool or a clinically validated emergency detector.

EMERGENCY_PHRASES = [
    "chest pain",
    "crushing chest pain",
    "severe chest pain",
    "cannot breathe",
    "can't breathe",
    "cant breathe",
    "severe difficulty breathing",
    "gasping for air",
    "blue lips",
    "unconscious",
    "unresponsive",
    "seizure",
    "face drooping",
    "weakness on one side",
    "slurred speech",
    "sudden confusion",
    "swelling of tongue",
    "swelling of throat",
    "severe allergic reaction",
    "vomiting blood",
    "coughing up blood"
]

NEGATION_WORDS = {
    "no", "not", "never", "without", "denies",
    "don't", "dont", "doesn't", "doesnt",
    "isn't", "isnt", "aren't", "arent",
    "haven't", "havent", "hasn't", "hasnt"
}


# --------------------------------------------------
# 4. TEXT PROCESSING HELPERS
# --------------------------------------------------

def normalize_text(text):
    """Normalize case, punctuation and repeated spaces."""
    text = str(text).lower().replace("’", "'")
    text = re.sub(r"[^a-z0-9'\s-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def phrase_is_present(text, phrase):
    """
    Match complete words and phrases rather than accidental
    substrings. Ignore simple negated mentions.
    """
    phrase = normalize_text(phrase)

    if not phrase:
        return False

    pattern = (
        r"(?<!\w)" + re.escape(phrase) + r"(?!\w)"
    )

    for match in re.finditer(pattern, text):
        preceding_words = text[:match.start()].split()[-3:]

        if any(
            word in NEGATION_WORDS
            for word in preceding_words
        ):
            continue

        return True

    return False


def get_symptom_variants(symptom):
    """Return a dataset symptom and its known alternative phrases."""
    symptom = normalize_text(symptom)
    variants = {symptom}

    for canonical, aliases in SYMPTOM_ALIASES.items():
        names = [canonical] + aliases

        normalized_names = {
            normalize_text(name) for name in names
        }

        if symptom in normalized_names:
            variants.update(normalized_names)

    return variants


def find_emergency_phrases(text):
    """Return emergency phrases found in the user's message."""
    found = []

    for phrase in EMERGENCY_PHRASES:
        if phrase_is_present(text, phrase):
            found.append(phrase)

    return list(dict.fromkeys(found))


# --------------------------------------------------
# 5. MAIN SYMPTOM ANALYSIS ENGINE
# --------------------------------------------------

def analyze(user_input):
    """
    Return ranked possible dataset matches.

    The score represents symptom overlap, not the probability
    of a condition and not a confirmed medical diagnosis.
    """

    # Validate the input.
    if not isinstance(user_input, str) or not user_input.strip():
        return {
            "error": "Please enter your symptoms before sending.",
            "emergency": False,
            "matches": []
        }

    if len(user_input) > 1000:
        return {
            "error": "Please keep your message under 1000 characters.",
            "emergency": False,
            "matches": []
        }

    text = normalize_text(user_input)

    # Check emergency phrases before normal matching.
    emergency_matches = find_emergency_phrases(text)

    if emergency_matches:
        return {
            "emergency": True,
            "emergency_message": (
                "Your message contains a possible emergency warning "
                "sign. If this symptom is happening now, seek urgent "
                "medical help or contact your local emergency service. "
                "Do not rely on this chatbot to assess an emergency."
            ),
            "emergency_symptoms": emergency_matches,
            "condition": "Possible Emergency Warning",
            "severity": "High",
            "score": 0,
            "matched_symptoms": [],
            "advice": (
                "Seek urgent professional assessment if the warning "
                "symptom is present. This chatbot cannot rule out "
                "a medical emergency."
            ),
            "matches": []
        }

    # Identify symptoms mentioned in the message.
    detected_symptoms = set()

    for item in DATA:
        for symptom in item.get("symptoms", []):
            variants = get_symptom_variants(symptom)

            if any(
                phrase_is_present(text, variant)
                for variant in variants
            ):
                detected_symptoms.add(normalize_text(symptom))

    # No recognized symptoms.
    if not detected_symptoms:
        return {
            "emergency": False,
            "condition": "No Clear Match",
            "severity": "Unknown",
            "score": 0,
            "matched_symptoms": [],
            "advice": (
                "I could not match your message to the symptoms in "
                "the dataset. Try describing your symptoms in simple "
                "words, or consult a healthcare professional."
            ),
            "matches": [],
            "message": (
                "This educational tool does not provide a medical "
                "diagnosis."
            )
        }

    # Count how many conditions contain each symptom.
    symptom_frequency = Counter()

    for item in DATA:
        unique_symptoms = {
            normalize_text(symptom)
            for symptom in item.get("symptoms", [])
            if normalize_text(symptom)
        }

        for symptom in unique_symptoms:
            symptom_frequency[symptom] += 1

    total_conditions = max(len(DATA), 1)

    # Rank conditions by weighted symptom overlap.
    ranked_matches = []

    for item in DATA:
        condition_symptoms = {
            normalize_text(symptom)
            for symptom in item.get("symptoms", [])
            if normalize_text(symptom)
        }

        if not condition_symptoms:
            continue

        matched = condition_symptoms.intersection(
            detected_symptoms
        )

        if not matched:
            continue

        # Less-common dataset symptoms receive greater weight.
        def symptom_weight(symptom):
            frequency = symptom_frequency.get(symptom, 1)

            return 1 + (
                total_conditions / frequency
            ) ** 0.5

        total_weight = sum(
            symptom_weight(symptom)
            for symptom in condition_symptoms
        )

        matched_weight = sum(
            symptom_weight(symptom)
            for symptom in matched
        )

        score = round(
            100 * matched_weight / total_weight
        )

        ranked_matches.append({
            "condition": item["condition"],
            "severity": item["severity"],
            "advice": item["advice"],
            "score": score,
            "matched_symptoms": sorted(matched),
            "matched_count": len(matched)
        })

    # Sort by score and then the number of matched symptoms.
    ranked_matches.sort(
        key=lambda result: (
            result["score"],
            result["matched_count"]
        ),
        reverse=True
    )

    # Return up to three possible matches.
    top_matches = ranked_matches[:3]

    if not top_matches:
        return {
            "emergency": False,
            "condition": "No Clear Match",
            "severity": "Unknown",
            "score": 0,
            "matched_symptoms": [],
            "advice": "Please consult a healthcare professional.",
            "matches": []
        }

    best = top_matches[0]

    return {
        "emergency": False,
        "condition": best["condition"],
        "severity": best["severity"],
        "advice": best["advice"],
        "score": best["score"],
        "matched_symptoms": best["matched_symptoms"],
        "matches": top_matches,
        "message": (
            "These are possible matches from an educational dataset, "
            "not confirmed diagnoses. The score represents symptom "
            "overlap, not the probability of having a condition."
        )
    }


# --------------------------------------------------
# 6. FLASK ROUTES
# --------------------------------------------------

@app.route("/")
def home():
    return render_template("chat.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "error": "Please send a valid JSON request."
            }), 400

        user_message = data.get("message", "")

        if not isinstance(user_message, str):
            return jsonify({
                "error": "Message must be text."
            }), 400

        if not user_message.strip():
            return jsonify({
                "error": "Please enter your symptoms."
            }), 400

        if len(user_message) > 1000:
            return jsonify({
                "error": "Please keep your message under 1000 characters."
            }), 400

        result = analyze(user_message)

        if result.get("error"):
            return jsonify(result), 400

        return jsonify(result), 200

    except Exception:
        app.logger.exception("Error processing chat request")

        return jsonify({
            "error": "Something went wrong. Please try again."
        }), 500


# --------------------------------------------------
# 7. START THE APPLICATION
# --------------------------------------------------

if __name__ == "__main__":
    # Debug mode is disabled by default.
    app.run(host="127.0.0.1", port=5000, debug=False)
