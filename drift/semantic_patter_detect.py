import re
from collections import defaultdict
import matplotlib.pyplot as plt

# --- Patterns für die Zutaten der Meta-Marker ---
# (Ausbau für Produktivbetrieb empfohlen, hier nur beispielhaft!)

META_MARKERS = [
    {
        "name": "Emotionaler Rückzugsdruck",
        "patterns": [
            # Zutaten
            [r"(ich bin.*nichts wert|ich schaff das nicht|ich kann nicht mehr)",  # Selbstabwertung
             r"(du kümmerst dich.*nie um mich|dir ist eh alles egal)",             # Latenter Vorwurf
             r"(dann melde ich mich.*nicht mehr|ich ziehe mich zurück)",           # Rückzugsandrohung
             r"(na klar|ja, ist schon gut|schön für dich)"]                       # Milder Sarkasmus
        ]
    },
    {
        "name": "Vorwurfsvoller Sarkasmus",
        "patterns": [
            [r"(na klar|ja, genau|wie nett von dir)",         # Sarkasmus
             r"(immer bist du|wieder typisch du|war ja klar)",# Latenter Vorwurf
             r"(ironisch|haha|ist halt so)",                  # Emotionale Verschlüsselung
             r"(wütend|nervt|genervt)"]                      # Wut/Ärger unterschwellig
        ]
    },
    {
        "name": "Ambivalenter Nähe-Distanz-Knoten",
        "patterns": [
            [r"(ich brauche dich|vermissen|bleib bei mir)",   # Klammern
             r"(lass mich in ruhe|ich will allein sein)",     # Vermeidung
             r"(aber gleichzeitig|und doch|trotzdem)",        # Widerspruch
             r"(jetzt so, dann wieder so|plötzlich anders)"]  # Polarity-Flip
        ]
    }
    # ... hier kannst du alle weiteren Meta-Marker ergänzen!
]

def sliding_windows(text, window_size=3):
    """Teilt Text in Sätze auf und liefert Sliding-Window-Abschnitte (z.B. immer 3 Sätze)"""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    for i in range(len(sentences) - window_size + 1):
        yield ' '.join(sentences[i:i+window_size]), i

def detect_meta_markers(text, min_zutaten=3, window_size=3):
    """
    Erkennt Meta-Marker in Textabschnitten (Sliding Window)
    Gibt Heatmap, Marker-Treffer und semantische Dichte aus.
    """
    heatmap = defaultdict(list)
    found_spots = []

    for window, idx in sliding_windows(text, window_size):
        for marker in META_MARKERS:
            zutaten = marker['patterns'][0]
            zutaten_hits = [bool(re.search(pattern, window, re.IGNORECASE)) for pattern in zutaten]
            score = sum(zutaten_hits)
            if score >= min_zutaten:
                found_spots.append({
                    "marker": marker["name"],
                    "window": window,
                    "zutaten_hits": zutaten_hits,
                    "score": score,
                    "start_sentence": idx
                })
                heatmap[marker["name"]].append(idx)
    return found_spots, heatmap

def print_semantic_analysis(found_spots):
    for spot in found_spots:
        print(f"\nMeta-Marker erkannt: **{spot['marker']}** (Score: {spot['score']}/4)")
        print(f"Textausschnitt: {spot['window']}")
        print(f"Gefundene Zutaten: {spot['zutaten_hits']}\n")

def plot_heatmap(heatmap, total_windows):
    plt.figure(figsize=(10, 2 * len(heatmap)))
    for i, (marker, positions) in enumerate(heatmap.items()):
        plt.scatter(positions, [i]*len(positions), label=marker, s=200, alpha=0.7)
    plt.yticks(range(len(heatmap)), list(heatmap.keys()))
    plt.xlabel("Position im Chat (Window-Index)")
    plt.title("Meta-Marker Heatmap (semantische Hotspots)")
    plt.legend()
    plt.tight_layout()
    plt.show()

# Demo/Test
if __name__ == "__main__":
    chat = (
        "Ich weiß auch nicht, ich bin halt nichts wert. Du kümmerst dich ja eh nie um mich. "
        "Dann melde ich mich halt einfach nicht mehr. Ist schon klar, interessiert dich sowieso nicht. "
        "Manchmal brauch ich dich total, aber dann will ich plötzlich wieder alleine sein. "
        "Das ist halt so bei mir, aber gleichzeitig will ich dich auch nicht verlieren. "
        "Na klar, du bist ja immer so verständnisvoll. Aber immer muss ich alles alleine machen, haha."
    )

    found_spots, heatmap = detect_meta_markers(chat)
    print_semantic_analysis(found_spots)
    total_windows = max((idx for positions in heatmap.values() for idx in positions), default=0) + 1
    if heatmap:
        plot_heatmap(heatmap, total_windows)
    else:
        print("Keine semantisch zusammengesetzten Meta-Marker gefunden.")

