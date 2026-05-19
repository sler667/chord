import random

import streamlit as st


NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
NOTE_TO_INDEX = {name: index for index, name in enumerate(NOTE_NAMES)}

STYLE_PRESETS = {
    "J-Pop / Anime": {
        "color": "#f25f5c",
        "description": "明亮、推進感強，常見次屬、六級小和弦與懸浮張力。",
        "tensions": ["add9", "sus2", "maj7", "6/9"],
    },
    "Rock": {
        "color": "#247ba0",
        "description": "穩定骨架、強拍明確，適合八分音符推進與開放音程。",
        "tensions": ["sus4", "add9", "7"],
    },
    "Cinematic": {
        "color": "#4d9078",
        "description": "空間感大，偏好低音踏點、大片和聲與漸進旋律。",
        "tensions": ["maj7", "add9", "11", "6/9"],
    },
}

TRANSITIONS = {
    "I": [("V", 3), ("vi", 3), ("IV", 2), ("iii", 1), ("bVII", 1)],
    "ii": [("V", 5), ("IV", 1), ("vi", 2)],
    "iii": [("vi", 4), ("IV", 2), ("V", 2)],
    "IV": [("I", 2), ("V", 4), ("ii", 2), ("iv", 2), ("bVII", 1)],
    "V": [("I", 6), ("vi", 2), ("bVI", 1)],
    "vi": [("IV", 4), ("ii", 2), ("V", 2), ("III", 1)],
    "vii°": [("I", 5), ("iii", 1)],
    "i": [("VI", 3), ("iv", 3), ("V", 2), ("III", 2)],
    "ii°": [("V", 5), ("iv", 2)],
    "III": [("VI", 3), ("iv", 2), ("VII", 2)],
    "iv": [("V", 5), ("i", 2), ("bVI", 1)],
    "v": [("i", 4), ("VI", 2)],
    "VI": [("III", 2), ("iv", 3), ("VII", 1), ("ii°", 1)],
    "VII": [("III", 2), ("i", 3), ("V", 2)],
    "bVII": [("I", 4), ("IV", 2), ("V", 1)],
    "bVI": [("V", 4), ("iv", 2), ("I", 1)],
}

STYLE_BONUS = {
    "J-Pop / Anime": {
        ("IV", "V"): 2,
        ("V", "vi"): 2,
        ("vi", "IV"): 2,
        ("bVII", "I"): 2,
    },
    "Rock": {
        ("I", "bVII"): 3,
        ("bVII", "IV"): 2,
        ("IV", "I"): 1,
        ("V", "I"): 2,
    },
    "Cinematic": {
        ("i", "VI"): 2,
        ("VI", "III"): 2,
        ("IV", "ii"): 2,
        ("V", "bVI"): 1,
    },
}

MOOD_BONUS = {
    "Lift": {"I": 2, "IV": 2, "V": 2, "VI": 1},
    "Tension": {"ii": 2, "V": 3, "vii°": 2, "iv": 2, "bVI": 1},
    "Melancholy": {"vi": 3, "i": 2, "iv": 2, "III": 1},
    "Wonder": {"maj7": 2, "add9": 2, "sus2": 1},
}

ROMAN_INTERVALS = {
    "major": {
        "I": 0,
        "ii": 2,
        "iii": 4,
        "IV": 5,
        "V": 7,
        "vi": 9,
        "vii°": 11,
        "bVII": 10,
        "bVI": 8,
        "iv": 5,
    },
    "minor": {
        "i": 0,
        "ii°": 2,
        "III": 3,
        "iv": 5,
        "v": 7,
        "V": 7,
        "VI": 8,
        "VII": 10,
        "bVI": 8,
    },
}

BASE_QUALITIES = {
    "I": "maj",
    "ii": "min",
    "iii": "min",
    "IV": "maj",
    "V": "maj",
    "vi": "min",
    "vii°": "dim",
    "i": "min",
    "ii°": "dim",
    "III": "maj",
    "iv": "min",
    "v": "min",
    "VI": "maj",
    "VII": "maj",
    "bVII": "maj",
    "bVI": "maj",
}

QUALITY_INTERVALS = {
    "maj": [0, 4, 7],
    "min": [0, 3, 7],
    "dim": [0, 3, 6],
    "sus2": [0, 2, 7],
    "sus4": [0, 5, 7],
}


def note_name(index: int) -> str:
    return NOTE_NAMES[index % 12]


def build_chord_name(root: str, quality: str, extension: str) -> str:
    suffix_map = {
        "maj": "",
        "min": "m",
        "dim": "dim",
        "sus2": "sus2",
        "sus4": "sus4",
    }
    return f"{root}{suffix_map[quality]}{extension}"


def scale_mode_label(mode: str) -> str:
    return "Major" if mode == "major" else "Minor"


def chord_from_roman(key_root: str, mode: str, roman: str, extension: str = "") -> dict:
    root_index = NOTE_TO_INDEX[key_root]
    semitone = ROMAN_INTERVALS[mode][roman]
    quality = BASE_QUALITIES[roman]

    if extension.startswith("sus"):
        quality = extension
        extension = ""

    chord_root = note_name(root_index + semitone)
    chord_label = build_chord_name(chord_root, quality, extension)
    return {
        "roman": roman,
        "root": chord_root,
        "quality": quality,
        "extension": extension,
        "label": chord_label,
    }


def candidate_extensions(style: str, mood: str, roman: str, quality: str) -> list[str]:
    preferred = STYLE_PRESETS[style]["tensions"][:]
    if roman in {"V", "v"}:
        preferred.append("7")
    if roman in {"I", "i", "III", "VI"}:
        preferred.append("maj7" if quality == "maj" else "add9")
    if mood == "Melancholy" and quality == "min":
        preferred.append("add9")
    if mood == "Wonder":
        preferred.extend(["add9", "maj7"])
    options = [""] + preferred
    deduped = []
    for option in options:
        if option not in deduped:
            deduped.append(option)
    return deduped


def weighted_choice(options: list[tuple[str, int]], style: str, mood: str, last_roman: str) -> str:
    pool = []
    for roman, weight in options:
        weight += STYLE_BONUS.get(style, {}).get((last_roman, roman), 0)
        weight += MOOD_BONUS.get(mood, {}).get(roman, 0)
        pool.extend([roman] * max(weight, 1))
    return random.choice(pool)


def generate_progression(key_root: str, mode: str, style: str, mood: str, bars: int, seed_roman: str) -> list[dict]:
    progression = []
    current = seed_roman
    for _ in range(bars):
        quality = BASE_QUALITIES[current]
        extension = random.choice(candidate_extensions(style, mood, current, quality))
        progression.append(chord_from_roman(key_root, mode, current, extension))
        next_candidates = [
            item for item in TRANSITIONS.get(current, []) if item[0] in ROMAN_INTERVALS[mode]
        ]
        if not next_candidates:
            next_candidates = [(seed_roman, 1)]
        current = weighted_choice(next_candidates, style, mood, current)
    return progression


def suggest_next_chords(key_root: str, mode: str, style: str, mood: str, last_roman: str) -> list[dict]:
    options = [item for item in TRANSITIONS.get(last_roman, []) if item[0] in ROMAN_INTERVALS[mode]]
    ranked = []
    for roman, base_weight in options:
        score = base_weight
        score += STYLE_BONUS.get(style, {}).get((last_roman, roman), 0)
        score += MOOD_BONUS.get(mood, {}).get(roman, 0)
        quality = BASE_QUALITIES[roman]
        extension = candidate_extensions(style, mood, roman, quality)[-1]
        ranked.append((score, chord_from_roman(key_root, mode, roman, extension)))
    ranked.sort(key=lambda item: item[0], reverse=True)
    return [item[1] for item in ranked[:4]]


def voicing_intervals(chord: dict, style: str) -> list[int]:
    quality = chord["quality"]
    extension = chord["extension"]
    if quality in {"sus2", "sus4"}:
        intervals = QUALITY_INTERVALS[quality][:]
    else:
        intervals = QUALITY_INTERVALS[quality][:]
        if extension == "7":
            intervals.append(10)
        elif extension == "maj7":
            intervals.append(11)
        elif extension == "add9":
            intervals.append(14)
        elif extension == "11":
            intervals.extend([10, 17] if quality == "min" else [11, 17])
        elif extension == "6/9":
            intervals.extend([9, 14])

    if style == "Rock" and 14 in intervals:
        intervals.remove(14)
    return intervals


def piano_voicing(chord: dict, style: str) -> dict:
    root_index = NOTE_TO_INDEX[chord["root"]]
    intervals = voicing_intervals(chord, style)

    left_hand = [f"{note_name(root_index)}2", f"{note_name(root_index + 7)}3"]
    if style == "Cinematic":
        left_hand.append(f"{note_name(root_index)}3")

    right_hand = []
    for interval in intervals:
        octave = 4 if interval < 12 else 5
        right_hand.append(f"{note_name(root_index + interval)}{octave}")

    if style == "J-Pop / Anime" and len(right_hand) >= 3:
        right_hand = right_hand[:2] + right_hand[-1:] + right_hand[2:-1]

    return {"left": left_hand, "right": right_hand}


def melody_tone_pool(chord: dict) -> list[int]:
    root_index = NOTE_TO_INDEX[chord["root"]]
    pool = [root_index + 4, root_index + 7] if chord["quality"] == "maj" else [root_index + 3, root_index + 7]
    pool.append(root_index + 12)
    if chord["extension"] == "add9":
        pool.append(root_index + 14)
    if chord["extension"] == "maj7":
        pool.append(root_index + 11)
    return pool


def melody_sketch(progression: list[dict], style: str) -> list[list[str]]:
    contour = []
    last_pitch = None
    for chord in progression:
        tones = melody_tone_pool(chord)
        if last_pitch is None:
            chosen = random.choice(tones)
        else:
            chosen = min(tones, key=lambda pitch: abs(pitch - last_pitch))
        passing = chosen + random.choice([-2, 2]) if style != "Rock" else chosen + 2
        bar_notes = [
            f"{note_name(chosen)}5",
            f"{note_name(passing)}5",
            f"{note_name(chosen + 2)}5",
            f"{note_name(chosen)}5",
        ]
        contour.append(bar_notes)
        last_pitch = chosen
    return contour


def progression_text(progression: list[dict], key_root: str, mode: str) -> str:
    tonic = f"{key_root} {scale_mode_label(mode)}"
    return " | ".join(f"{chord['roman']} ({chord['label']})" for chord in progression) + f"  [{tonic}]"


def render_voicing_cards(progression: list[dict], style: str, melody: list[list[str]]) -> None:
    for index, chord in enumerate(progression, start=1):
        voicing = piano_voicing(chord, style)
        with st.container(border=True):
            st.markdown(f"**Bar {index} · {chord['roman']} / {chord['label']}**")
            st.write(f"Left hand: `{'  '.join(voicing['left'])}`")
            st.write(f"Right hand: `{'  '.join(voicing['right'])}`")
            st.write(f"Melody sketch: `{'  '.join(melody[index - 1])}`")


st.set_page_config(page_title="Chord Canvas Demo", page_icon="🎹", layout="wide")

if "seed" not in st.session_state:
    st.session_state.seed = 7

st.markdown(
    """
    <style>
    .hero {
        padding: 1.2rem 1.4rem;
        border-radius: 22px;
        background:
            radial-gradient(circle at top left, rgba(242, 95, 92, 0.22), transparent 34%),
            linear-gradient(135deg, #111827 0%, #19253a 45%, #243b53 100%);
        color: #f8fafc;
        margin-bottom: 1rem;
    }
    .hero h1 {
        margin: 0 0 0.4rem 0;
        font-size: 2rem;
    }
    .hero p {
        margin: 0;
        color: #dbe4f0;
    }
    .mini-note {
        padding: 0.8rem 1rem;
        border-radius: 16px;
        background: #f8fafc;
        border: 1px solid #d7e0ea;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>Chord Canvas</h1>
        <p>給日系、搖滾、電影配樂使用的編曲草稿工具。先幫你想下一個和弦，再把它攤成純鋼琴配置與簡單旋律線。</p>
    </div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([1.1, 1.4], gap="large")

with left:
    st.subheader("Direction")
    key_root = st.selectbox("Key", NOTE_NAMES, index=0)
    mode = st.radio("Mode", ["major", "minor"], index=0, horizontal=True, format_func=scale_mode_label)
    style = st.selectbox("Style", list(STYLE_PRESETS.keys()))
    mood = st.selectbox("Mood", ["Lift", "Tension", "Melancholy", "Wonder"])
    roman_choices = list(ROMAN_INTERVALS[mode].keys())
    seed_roman = st.selectbox("Current chord / starting point", roman_choices, index=0)
    bars = st.slider("How many bars to sketch", min_value=4, max_value=12, value=8)

    if st.button("Generate New Idea", type="primary", use_container_width=True):
        st.session_state.seed += 1

    random.seed(st.session_state.seed)
    st.markdown(
        f"""
        <div class="mini-note">
            <strong>{style}</strong><br>
            {STYLE_PRESETS[style]["description"]}
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    st.subheader("Next Chord Suggestions")
    suggestions = suggest_next_chords(key_root, mode, style, mood, seed_roman)
    if suggestions:
        columns = st.columns(len(suggestions))
        for column, chord in zip(columns, suggestions):
            with column:
                st.metric(chord["roman"], chord["label"])
    else:
        st.info("這個起點目前沒有對應建議，換個 mode 或起始和弦就能繼續。")

random.seed(st.session_state.seed)
progression = generate_progression(key_root, mode, style, mood, bars, seed_roman)
melody = melody_sketch(progression, style)

st.subheader("Progression Draft")
st.code(progression_text(progression, key_root, mode), language="text")

col_a, col_b = st.columns([1.1, 0.9], gap="large")

with col_a:
    st.subheader("Piano Voicing")
    render_voicing_cards(progression, style, melody)

with col_b:
    st.subheader("Arrangement Notes")
    st.write("Use the left hand as the harmonic spine, then thin or thicken the right hand depending on section size.")
    st.write("For verse-like sections, keep the top melody note sparse; for chorus-like sections, repeat the first two bars one octave higher.")

    st.subheader("How To Use This Demo")
    st.write("1. Choose key, mode, and style.")
    st.write("2. Start from your current chord and generate a fresh progression idea.")
    st.write("3. Take the suggested voicing into your DAW and adjust rhythm first, then color tones.")

    st.subheader("GitHub Ready")
    st.write("This demo is a small Streamlit app, so it is easy to push to GitHub and deploy later on Streamlit Community Cloud or another Python host.")
