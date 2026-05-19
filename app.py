import random

import streamlit as st


NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
NOTE_TO_INDEX = {name: index for index, name in enumerate(NOTE_NAMES)}
ENHARMONIC_EQUIV = {"Db": "C#", "Eb": "D#", "Gb": "F#", "Ab": "G#", "Bb": "A#"}
OPEN_STRING_INDICES = [4, 9, 2, 7, 11, 4]
STRING_NAMES = ["6(E)", "5(A)", "4(D)", "3(G)", "2(B)", "1(E)"]

STYLE_PRESETS = {
    "J-Pop / Anime": {
        "description": "明亮、推進感強，常見六級小和弦、流動低音與 add9 色彩。",
        "tensions": ["add9", "sus2", "maj7", "6/9"],
    },
    "Rock": {
        "description": "骨架明確、重拍穩，適合直接有力的和聲推進。",
        "tensions": ["sus4", "add9", "7"],
    },
    "Cinematic": {
        "description": "空間感大，適合寬廣和弦、踏點低音與漸進旋律。",
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
    "Wonder": {"I": 1, "III": 1, "VI": 1},
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

SCALE_INTERVALS = {
    "major": [0, 2, 4, 5, 7, 9, 11],
    "minor": [0, 2, 3, 5, 7, 8, 10],
}

DIATONIC_TRIADS = {
    "major": ["I", "ii", "iii", "IV", "V", "vi", "vii°"],
    "minor": ["i", "ii°", "III", "iv", "v", "VI", "VII"],
}

GUITAR_CHORD_LIBRARY = {
    "C": {"frets": ["x", 3, 2, 0, 1, 0], "fingers": ["", 3, 2, 0, 1, 0]},
    "Cm": {"frets": ["x", 3, 5, 5, 4, 3], "fingers": ["", 1, 3, 4, 2, 1]},
    "D": {"frets": ["x", "x", 0, 2, 3, 2], "fingers": ["", "", 0, 1, 3, 2]},
    "Dm": {"frets": ["x", "x", 0, 2, 3, 1], "fingers": ["", "", 0, 2, 3, 1]},
    "E": {"frets": [0, 2, 2, 1, 0, 0], "fingers": [0, 2, 3, 1, 0, 0]},
    "Em": {"frets": [0, 2, 2, 0, 0, 0], "fingers": [0, 2, 3, 0, 0, 0]},
    "F": {"frets": [1, 3, 3, 2, 1, 1], "fingers": [1, 3, 4, 2, 1, 1]},
    "Fm": {"frets": [1, 3, 3, 1, 1, 1], "fingers": [1, 3, 4, 1, 1, 1]},
    "G": {"frets": [3, 2, 0, 0, 0, 3], "fingers": [2, 1, 0, 0, 0, 3]},
    "Gm": {"frets": [3, 5, 5, 3, 3, 3], "fingers": [1, 3, 4, 1, 1, 1]},
    "A": {"frets": ["x", 0, 2, 2, 2, 0], "fingers": ["", 0, 1, 2, 3, 0]},
    "Am": {"frets": ["x", 0, 2, 2, 1, 0], "fingers": ["", 0, 2, 3, 1, 0]},
    "B": {"frets": ["x", 2, 4, 4, 4, 2], "fingers": ["", 1, 3, 4, 4, 1]},
    "Bm": {"frets": ["x", 2, 4, 4, 3, 2], "fingers": ["", 1, 3, 4, 2, 1]},
    "C#": {"frets": ["x", 4, 6, 6, 6, 4], "fingers": ["", 1, 3, 4, 4, 1]},
    "C#m": {"frets": ["x", 4, 6, 6, 5, 4], "fingers": ["", 1, 3, 4, 2, 1]},
    "D#": {"frets": ["x", 6, 8, 8, 8, 6], "fingers": ["", 1, 3, 4, 4, 1]},
    "D#m": {"frets": ["x", 6, 8, 8, 7, 6], "fingers": ["", 1, 3, 4, 2, 1]},
    "F#": {"frets": [2, 4, 4, 3, 2, 2], "fingers": [1, 3, 4, 2, 1, 1]},
    "F#m": {"frets": [2, 4, 4, 2, 2, 2], "fingers": [1, 3, 4, 1, 1, 1]},
    "G#": {"frets": [4, 6, 6, 5, 4, 4], "fingers": [1, 3, 4, 2, 1, 1]},
    "G#m": {"frets": [4, 6, 6, 4, 4, 4], "fingers": [1, 3, 4, 1, 1, 1]},
    "A#": {"frets": [6, 8, 8, 7, 6, 6], "fingers": [1, 3, 4, 2, 1, 1]},
    "A#m": {"frets": [6, 8, 8, 6, 6, 6], "fingers": [1, 3, 4, 1, 1, 1]},
    "Bdim": {"frets": ["x", 2, 3, 4, 3, "x"], "fingers": ["", 1, 2, 4, 3, ""]},
    "C#dim": {"frets": ["x", 4, 5, 6, 5, "x"], "fingers": ["", 1, 2, 4, 3, ""]},
    "D#dim": {"frets": ["x", 6, 7, 8, 7, "x"], "fingers": ["", 1, 2, 4, 3, ""]},
    "Fdim": {"frets": ["x", 8, 9, 10, 9, "x"], "fingers": ["", 1, 2, 4, 3, ""]},
    "Gdim": {"frets": ["x", 10, 11, 12, 11, "x"], "fingers": ["", 1, 2, 4, 3, ""]},
    "Adim": {"frets": ["x", 0, 1, 2, 1, "x"], "fingers": ["", 0, 1, 3, 2, ""]},
}


def normalize_note(note: str) -> str:
    return ENHARMONIC_EQUIV.get(note, note)


def note_name(index: int) -> str:
    return NOTE_NAMES[index % 12]


def scale_mode_label(mode: str) -> str:
    return "Major" if mode == "major" else "Minor"


def quality_suffix(quality: str) -> str:
    return {"maj": "", "min": "m", "dim": "dim", "sus2": "sus2", "sus4": "sus4"}[quality]


def build_chord_name(root: str, quality: str, extension: str) -> str:
    return f"{root}{quality_suffix(quality)}{extension}"


def chord_from_roman(key_root: str, mode: str, roman: str, extension: str = "") -> dict:
    root_index = NOTE_TO_INDEX[normalize_note(key_root)]
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

    options = [""]
    for option in preferred:
        if option not in options:
            options.append(option)
    return options


def weighted_choice(options: list[tuple[str, int]], style: str, mood: str, last_roman: str) -> str:
    pool = []
    for roman, weight in options:
        adjusted = weight
        adjusted += STYLE_BONUS.get(style, {}).get((last_roman, roman), 0)
        adjusted += MOOD_BONUS.get(mood, {}).get(roman, 0)
        pool.extend([roman] * max(adjusted, 1))
    return random.choice(pool)


def generate_progression(key_root: str, mode: str, style: str, mood: str, bars: int, seed_roman: str) -> list[dict]:
    progression = []
    current = seed_roman
    for _ in range(bars):
        quality = BASE_QUALITIES[current]
        extension = random.choice(candidate_extensions(style, mood, current, quality))
        progression.append(chord_from_roman(key_root, mode, current, extension))
        next_candidates = [item for item in TRANSITIONS.get(current, []) if item[0] in ROMAN_INTERVALS[mode]]
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
    fifth = 6 if chord["quality"] == "dim" else 7
    left_hand = [f"{note_name(root_index)}2", f"{note_name(root_index + fifth)}3"]
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
        chosen = random.choice(tones) if last_pitch is None else min(tones, key=lambda pitch: abs(pitch - last_pitch))
        passing = chosen + (2 if style == "Rock" else random.choice([-2, 2]))
        contour.append(
            [
                f"{note_name(chosen)}5",
                f"{note_name(passing)}5",
                f"{note_name(chosen + 2)}5",
                f"{note_name(chosen)}5",
            ]
        )
        last_pitch = chosen
    return contour


def progression_text(progression: list[dict], key_root: str, mode: str) -> str:
    tonic = f"{key_root} {scale_mode_label(mode)}"
    body = " | ".join(f"{chord['roman']} ({chord['label']})" for chord in progression)
    return f"{body}  [{tonic}]"


def render_voicing_cards(progression: list[dict], style: str, melody: list[list[str]]) -> None:
    for index, chord in enumerate(progression, start=1):
        voicing = piano_voicing(chord, style)
        with st.container(border=True):
            st.markdown(f"**Bar {index} · {chord['roman']} / {chord['label']}**")
            st.write(f"Left hand: `{'  '.join(voicing['left'])}`")
            st.write(f"Right hand: `{'  '.join(voicing['right'])}`")
            st.write(f"Melody sketch: `{'  '.join(melody[index - 1])}`")


def scale_note_set(key_root: str, mode: str) -> set[int]:
    tonic = NOTE_TO_INDEX[normalize_note(key_root)]
    return {(tonic + interval) % 12 for interval in SCALE_INTERVALS[mode]}


def build_fretboard_rows(key_root: str, mode: str, max_fret: int = 12) -> list[list[dict]]:
    tonic = NOTE_TO_INDEX[normalize_note(key_root)]
    scale_notes = scale_note_set(key_root, mode)
    rows = []
    for string_index, open_note in enumerate(OPEN_STRING_INDICES):
        row = []
        for fret in range(max_fret + 1):
            note_index = (open_note + fret) % 12
            row.append(
                {
                    "string": STRING_NAMES[string_index],
                    "fret": fret,
                    "note": note_name(note_index),
                    "in_scale": note_index in scale_notes,
                    "is_root": note_index == tonic,
                }
            )
        rows.append(row)
    return rows


def render_fretboard(key_root: str, mode: str) -> None:
    rows = build_fretboard_rows(key_root, mode)
    header = "".join(f"<div class='fret-label'>{fret}</div>" for fret in range(13))
    html_parts = [
        "<div class='fretboard-shell'>",
        f"<div class='fretboard-header'><div class='string-label'></div>{header}</div>",
        "<div class='fretboard-board'>",
    ]
    for row in rows:
        row_html = [f"<div class='string-label'>{row[0]['string']}</div>"]
        for cell in row:
            if cell["is_root"]:
                marker = "root"
            elif cell["in_scale"]:
                marker = "scale"
            else:
                marker = "off"
            if marker == "off":
                row_html.append("<div class='fret-cell off'></div>")
            else:
                row_html.append(
                    f"<div class='fret-cell {marker}'><span class='note-marker {marker}'>{cell['note']}</span></div>"
                )
        html_parts.append(f"<div class='fret-row'>{''.join(row_html)}</div>")
    html_parts.append("</div></div>")
    st.markdown("".join(html_parts), unsafe_allow_html=True)


def chord_symbol(root: str, quality: str) -> str:
    return f"{root}{quality_suffix(quality)}"


def diatonic_guitar_chords(key_root: str, mode: str) -> list[dict]:
    chords = []
    for roman in DIATONIC_TRIADS[mode]:
        chord = chord_from_roman(key_root, mode, roman)
        symbol = chord_symbol(chord["root"], chord["quality"])
        chords.append(
            {
                "roman": roman,
                "symbol": symbol,
                "diagram": GUITAR_CHORD_LIBRARY.get(symbol),
            }
        )
    return chords


def diagram_start_fret(frets: list) -> int:
    numeric_frets = [fret for fret in frets if isinstance(fret, int) and fret > 0]
    if not numeric_frets:
        return 1
    minimum = min(numeric_frets)
    return 1 if minimum <= 4 else minimum


def render_chord_diagram(symbol: str, diagram: dict | None, roman: str) -> None:
    with st.container(border=True):
        st.markdown(f"**{roman} · {symbol}**")
        if not diagram:
            st.write("這個和弦目前還沒有內建指法圖。")
            return

        frets = diagram["frets"]
        fingers = diagram["fingers"]
        start_fret = diagram_start_fret(frets)
        top_markers = []
        for fret in frets:
            if fret == "x":
                top_markers.append("<div class='top-marker muted'>x</div>")
            elif fret == 0:
                top_markers.append("<div class='top-marker open'>o</div>")
            else:
                top_markers.append("<div class='top-marker'>&nbsp;</div>")

        grid_cells = []
        for string_number in range(6):
            for fret_offset in range(5):
                absolute_fret = start_fret + fret_offset
                cell_class = "diagram-cell"
                label = ""
                if frets[string_number] == absolute_fret:
                    finger_text = fingers[string_number]
                    label = "" if finger_text in {"", 0} else str(finger_text)
                    cell_class += " active"
                if "active" in cell_class:
                    grid_cells.append(
                        f"<div class='{cell_class}'><span class='diagram-dot'>{label}</span></div>"
                    )
                else:
                    grid_cells.append(f"<div class='{cell_class}'></div>")

        st.markdown(
            f"""
            <div class="diagram-wrap wood">
                <div class="diagram-top">{''.join(top_markers)}</div>
                <div class="diagram-grid">{''.join(grid_cells)}</div>
                <div class="diagram-footer">Fret {start_fret} to {start_fret + 4}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_arranger_page() -> None:
    left, right = st.columns([1.08, 1.42], gap="large")

    with left:
        st.subheader("編曲方向")
        key_root = st.selectbox("Key", NOTE_NAMES, index=0)
        mode = st.radio("Mode", ["major", "minor"], index=0, horizontal=True, format_func=scale_mode_label)
        style = st.selectbox("Style", list(STYLE_PRESETS.keys()))
        mood = st.selectbox("Mood", ["Lift", "Tension", "Melancholy", "Wonder"])
        roman_choices = list(ROMAN_INTERVALS[mode].keys())
        seed_roman = st.selectbox("Current chord / starting point", roman_choices, index=0)
        bars = st.slider("How many bars to sketch", min_value=4, max_value=12, value=8)

        if st.button("Generate New Idea", type="primary", use_container_width=True):
            st.session_state.seed += 1

        st.markdown(
            f"""
            <div class="info-card">
                <strong>{style}</strong><br>
                {STYLE_PRESETS[style]["description"]}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.subheader("下一個和弦建議")
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

    col_a, col_b = st.columns([1.12, 0.88], gap="large")
    with col_a:
        st.subheader("鋼琴配置")
        render_voicing_cards(progression, style, melody)

    with col_b:
        st.subheader("使用提示")
        st.write("左手先穩住根音與五度，右手再依段落大小決定要不要加滿色彩音。")
        st.write("主歌可以保守一些，只留三和弦或 add9；副歌再把上方旋律整體抬高一個八度。")

        st.subheader("這頁會幫你什麼")
        st.write("1. 給你下一個和弦的方向。")
        st.write("2. 自動延伸成一段可用的 progression 草稿。")
        st.write("3. 直接把每小節攤成鋼琴配置與簡單旋律線。")


def render_guitar_page() -> None:
    st.subheader("吉他指板與和弦圖")
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        guitar_key = st.selectbox("調性根音", NOTE_NAMES, index=0, key="guitar_key")
        guitar_mode = st.radio(
            "音階模式",
            ["major", "minor"],
            index=0,
            horizontal=True,
            key="guitar_mode",
            format_func=scale_mode_label,
        )
        st.markdown(
            """
            <div class="info-card">
                Root 會用紅色標示。<br>
                同一個調內的其他音階音會用藍綠色標示。<br>
                目前顯示 0 到 12 fret，方便你快速找位置。
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_right:
        scale_notes = [note_name(index) for index in sorted(scale_note_set(guitar_key, guitar_mode))]
        st.subheader(f"{guitar_key} {scale_mode_label(guitar_mode)} 音階")
        st.write("Scale notes: " + " - ".join(scale_notes))
        st.write("下方也會列出這個調常見的七個自然和弦，並顯示可直接按的吉他指法圖。")

    render_fretboard(guitar_key, guitar_mode)

    st.subheader("Diatonic Chord Shapes")
    chords = diatonic_guitar_chords(guitar_key, guitar_mode)
    columns = st.columns(3)
    for index, chord in enumerate(chords):
        with columns[index % 3]:
            render_chord_diagram(chord["symbol"], chord["diagram"], chord["roman"])


st.set_page_config(page_title="Chord Canvas Demo", page_icon="🎹", layout="wide")

if "seed" not in st.session_state:
    st.session_state.seed = 7

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at top right, rgba(120, 119, 198, 0.06), transparent 26%),
            linear-gradient(180deg, #f4f6f8 0%, #eef2f5 100%);
        color: #17212b;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2.5rem;
        max-width: 1280px;
    }
    .stRadio > div {
        gap: 0.55rem;
    }
    .stButton > button,
    .stDownloadButton > button {
        border-radius: 12px;
        border: 1px solid #243b53;
        background: linear-gradient(180deg, #243b53 0%, #192534 100%);
        color: #f8fafc;
        font-weight: 600;
        letter-spacing: 0.01em;
        box-shadow: 0 8px 18px rgba(15, 23, 42, 0.12);
    }
    .stButton > button:hover,
    .stDownloadButton > button:hover {
        border-color: #102a43;
        background: linear-gradient(180deg, #2c4a67 0%, #1d3147 100%);
    }
    div[data-testid="stMetric"] {
        background: linear-gradient(180deg, #ffffff 0%, #f7fafc 100%);
        border: 1px solid #d9e2ec;
        border-radius: 14px;
        padding: 0.75rem 0.85rem;
        box-shadow: 0 6px 16px rgba(15, 23, 42, 0.06);
    }
    div[data-testid="stCodeBlock"] {
        border-radius: 14px;
        border: 1px solid #d9e2ec;
    }
    div[data-testid="stVerticalBlock"] div[data-testid="stContainer"] {
        border-radius: 14px;
    }
    .hero {
        padding: 1.35rem 1.5rem;
        border-radius: 18px;
        background:
            linear-gradient(135deg, rgba(179, 123, 58, 0.14), transparent 18%),
            linear-gradient(135deg, #10161f 0%, #16212d 48%, #1e2d3a 100%);
        color: #f8fafc;
        border: 1px solid rgba(148, 163, 184, 0.18);
        box-shadow: 0 18px 36px rgba(15, 23, 42, 0.18);
        margin-bottom: 1.1rem;
    }
    .hero h1 {
        margin: 0 0 0.4rem 0;
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: 0.01em;
    }
    .hero p {
        margin: 0;
        color: #c8d4df;
        max-width: 760px;
        line-height: 1.55;
    }
    .info-card {
        padding: 0.95rem 1rem;
        border-radius: 14px;
        background: linear-gradient(180deg, #ffffff 0%, #f7fafc 100%);
        border: 1px solid #d9e2ec;
        box-shadow: 0 8px 18px rgba(15, 23, 42, 0.05);
        line-height: 1.6;
        color: #243b53;
    }
    .fretboard-shell {
        margin-top: 0.95rem;
    }
    .fretboard-header, .fret-row {
        display: grid;
        grid-template-columns: 88px repeat(13, minmax(36px, 1fr));
        gap: 6px;
        align-items: center;
    }
    .fretboard-header {
        margin-bottom: 0.45rem;
    }
    .fretboard-board {
        padding: 1.1rem 0.85rem 0.85rem 0.85rem;
        border-radius: 18px;
        background:
            linear-gradient(180deg, rgba(255,255,255,0.06), rgba(0,0,0,0.14)),
            repeating-linear-gradient(
                90deg,
                #7a4d27 0px,
                #7a4d27 24px,
                #6e431f 24px,
                #6e431f 48px,
                #85532a 48px,
                #85532a 72px
            );
        border: 1px solid #5b3819;
        box-shadow:
            inset 0 1px 0 rgba(255,255,255,0.16),
            inset 0 -10px 20px rgba(33, 18, 8, 0.28),
            0 14px 30px rgba(15, 23, 42, 0.14);
    }
    .string-label, .fret-label {
        font-size: 0.82rem;
        color: #52606d;
        text-align: center;
        font-weight: 600;
    }
    .fret-cell {
        min-height: 42px;
        border-right: 4px solid rgba(213, 219, 226, 0.82);
        border-left: 1px solid rgba(86, 57, 31, 0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        background:
            linear-gradient(180deg, rgba(255,255,255,0.03), rgba(0,0,0,0.08));
    }
    .fret-cell::before {
        content: "";
        position: absolute;
        left: 0;
        right: 0;
        top: 50%;
        height: 3px;
        transform: translateY(-50%);
        background: linear-gradient(180deg, #f2f4f7 0%, #c4cbd3 48%, #7b8794 100%);
        box-shadow: 0 1px 0 rgba(255,255,255,0.26);
    }
    .fret-cell.off::before {
        opacity: 0.95;
    }
    .note-marker {
        position: relative;
        z-index: 1;
        width: 28px;
        height: 28px;
        border-radius: 999px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        font-weight: 700;
        box-shadow:
            inset 0 1px 1px rgba(255,255,255,0.2),
            0 4px 10px rgba(0,0,0,0.22);
    }
    .note-marker.scale {
        background: linear-gradient(180deg, #d7e8f7 0%, #6b8fb1 100%);
        color: #f8fafc;
        border: 1px solid rgba(255,255,255,0.28);
    }
    .note-marker.root {
        background: linear-gradient(180deg, #f2d3a8 0%, #b7792c 100%);
        color: #fffaf5;
        border: 1px solid rgba(255,255,255,0.26);
    }
    .fret-cell.scale,
    .fret-cell.root {
        font-weight: 700;
    }
    .diagram-wrap {
        padding: 0.8rem 0.85rem 0.6rem 0.85rem;
        border-radius: 14px;
    }
    .diagram-wrap.wood {
        background:
            linear-gradient(180deg, rgba(255,255,255,0.06), rgba(0,0,0,0.14)),
            repeating-linear-gradient(
                90deg,
                #8f5c31 0px,
                #8f5c31 18px,
                #7b4c26 18px,
                #7b4c26 36px,
                #98663a 36px,
                #98663a 54px
            );
        border: 1px solid #643d1b;
        box-shadow:
            inset 0 1px 0 rgba(255,255,255,0.16),
            inset 0 -8px 14px rgba(55, 31, 12, 0.24);
    }
    .diagram-top {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 6px;
        margin-bottom: 4px;
    }
    .top-marker {
        text-align: center;
        font-size: 0.82rem;
        color: #e8dccf;
        min-height: 20px;
        font-weight: 600;
    }
    .top-marker.muted {
        color: #fca5a5;
        font-weight: 700;
    }
    .top-marker.open {
        color: #bfdbfe;
        font-weight: 700;
    }
    .diagram-grid {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        grid-template-rows: repeat(5, 34px);
        gap: 6px;
    }
    .diagram-cell {
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        border-right: 4px solid rgba(220, 225, 231, 0.86);
    }
    .diagram-cell::before {
        content: "";
        position: absolute;
        left: 0;
        right: 0;
        top: 50%;
        height: 3px;
        transform: translateY(-50%);
        background: linear-gradient(180deg, #edf2f7 0%, #cbd2d9 45%, #7b8794 100%);
        box-shadow: 0 1px 0 rgba(255,255,255,0.24);
    }
    .diagram-cell.active {
        font-weight: 700;
    }
    .diagram-dot {
        position: relative;
        z-index: 1;
        width: 24px;
        height: 24px;
        border-radius: 999px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(180deg, #e9c89b 0%, #a96c28 100%);
        color: #fffaf5;
        border: 1px solid rgba(255,255,255,0.24);
        box-shadow:
            inset 0 1px 1px rgba(255,255,255,0.18),
            0 4px 8px rgba(0,0,0,0.22);
    }
    .diagram-footer {
        margin-top: 0.45rem;
        font-size: 0.8rem;
        color: #ead8c4;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>Chord Canvas</h1>
        <p>以編曲與樂器實作為核心的和聲工作台。Arranger 負責 progression 與 piano voicing，Guitar 負責指板定位與 chord shape 參考。</p>
    </div>
    """,
    unsafe_allow_html=True,
)

page = st.radio(
    "Page",
    ["1. Arranger", "2. Guitar"],
    horizontal=True,
    label_visibility="collapsed",
)

if page == "1. Arranger":
    render_arranger_page()
else:
    render_guitar_page()
