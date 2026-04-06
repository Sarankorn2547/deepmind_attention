"""
AGI Benchmark Dataset Generator
Kaggle Competition: kaggle-measuring-agi
Generates structured JSON test cases across 8 cognitive evaluation dimensions.
"""

import json
import random
import copy
from itertools import combinations

random.seed(42)

# ─────────────────────────────────────────────
# POOLS (from data_construction_2.py)
# ─────────────────────────────────────────────

math_pool = [
    ("What is 1 + 1?", "2"), ("What is 5 + 5?", "10"), ("What is 10 - 3?", "7"),
    ("What is 2 * 3?", "6"), ("What is 20 / 4?", "5"), ("What is 15 + 7?", "22"),
    ("What is 9 - 4?", "5"), ("What is 3 * 4?", "12"), ("What is 18 / 2?", "9"),
    ("What is 6 + 8?", "14"),
]

factual_pool = [
    ("What is the capital of China?", "beijing"),
    ("Who was the first US president?", "george washington"),
    ("What is the largest planet?", "jupiter"),
    ("What is the chemical symbol for water?", "h2o"),
    ("Who wrote Romeo and Juliet?", "william shakespeare"),
    ("What is the square root of 16?", "4"),
    ("What is the currency of Japan?", "yen"),
    ("Who discovered penicillin?", "alexander fleming"),
    ("What is the longest river in the world?", "nile"),
    ("What is the atomic number of carbon?", "6"),
]

linking_pool = [
    {"contexts": ["John is near the Statue of Peace.", "The Statue of Peace is in the Northern Park."], "question": "Who is at the Northern Park?", "answer": "john"},
    {"contexts": ["The Golden Key is inside the Oak Chest.", "The Oak Chest is in the Attic."], "question": "Where is the Golden Key?", "answer": "attic"},
    {"contexts": ["Alice lives in the Blue House.", "The Blue House is on Elm Street."], "question": "Where does Alice live?", "answer": "elm street"},
    {"contexts": ["The book is on the shelf.", "The shelf is in the library."], "question": "Where is the book?", "answer": "library"},
    {"contexts": ["Tom has the red ball.", "The red ball is under the table."], "question": "Where is Tom's ball?", "answer": "under the table"},
    {"contexts": ["The cat is in the garden.", "The garden is behind the house."], "question": "Where is the cat?", "answer": "behind the house"},
    {"contexts": ["Sarah works at the bank.", "The bank is downtown."], "question": "Where does Sarah work?", "answer": "downtown"},
    {"contexts": ["The car is parked in the garage.", "The garage is next to the house.", "The house is on Maple Avenue."], "question": "Where is the car parked?", "answer": "maple avenue"},
    {"contexts": ["The treasure is in the chest.", "The chest is in the cave.", "The cave is in the mountain."], "question": "Where is the treasure?", "answer": "mountain"},
    {"contexts": ["The phone is on the desk.", "The desk is in the office.", "The office is in the building."], "question": "Where is the phone?", "answer": "building"},
]

info_question_pool = [
    {"info": "The book on the table has a blue cover.", "question": "What is the color of the book on the table?", "answer": "blue"},
    {"info": "John is 25 years old.", "question": "How old is John?", "answer": "25"},
    {"info": "The cat is sleeping on the couch.", "question": "Where is the cat sleeping?", "answer": "on the couch"},
    {"info": "The meeting starts at 3 PM.", "question": "What time does the meeting start?", "answer": "3 pm"},
    {"info": "Sarah lives in a red house.", "question": "What color is Sarah's house?", "answer": "red"},
    {"info": "The train arrives at platform 5.", "question": "At which platform does the train arrive?", "answer": "5"},
    {"info": "Tom has three apples.", "question": "How many apples does Tom have?", "answer": "three"},
    {"info": "The movie lasts for two hours.", "question": "How long does the movie last?", "answer": "two hours"},
    {"info": "The dog is named Max.", "question": "What is the dog's name?", "answer": "max"},
    {"info": "The restaurant is located on Main Street.", "question": "On which street is the restaurant located?", "answer": "main street"},
]

john_apple_list = [
    {"context": "John receives 2 apples", "change": 2},
    {"context": "John throws away 1 apple", "change": -1},
    {"context": "John buys 5 apples from the store", "change": 5},
    {"context": "John finds 3 apples in the garden", "change": 3},
    {"context": "John eats 2 apples", "change": -2},
    {"context": "John gives away 4 apples", "change": -4},
    {"context": "Tom gives John 6 apples", "change": 6},
    {"context": "John loses 1 apple by accident", "change": -1},
    {"context": "John trades 3 apples with Sarah", "change": -3},
    {"context": "John picks 7 apples from the tree", "change": 7},
    {"context": "John receives 4 apples from his friend", "change": 4},
    {"context": "John stole 5 apples from the store", "change": 5},
    {"context": "Sarah gives John 2 apples", "change": 2},
    {"context": "John uses 3 apples for cooking", "change": -3},
    {"context": "John sells 2 apples at the market", "change": -2},
    {"context": "The store delivers 10 apples to John", "change": 10},
    {"context": "John spoils 1 apple", "change": -1},
    {"context": "John gets 4 more apples as a gift", "change": 4},
    {"context": "John removes 2 bad apples", "change": -2},
    {"context": "John receives 3 fresh apples", "change": 3},
]

fantasy_question_pool = [
    {"info": "The magician has a crystal ball that glows blue.", "question": "What color does the magician's crystal ball glow?", "answer": "blue"},
    {"info": "The enchanted sword was forged in the volcanic fires of Mount Inferno.", "question": "Where was the enchanted sword forged?", "answer": "mount inferno"},
    {"info": "The dragon's hoard contains 500 gold coins.", "question": "How many gold coins are in the dragon's hoard?", "answer": "500"},
    {"info": "The wizard lives in a tower made of silver stones.", "question": "What material is the wizard's tower made of?", "answer": "silver stones"},
    {"info": "The fairy queen rules over the Enchanted Forest.", "question": "What does the fairy queen rule over?", "answer": "the enchanted forest"},
    {"info": "The knight's armor is painted crimson red.", "question": "What color is the knight's armor?", "answer": "crimson red"},
    {"info": "The spell requires reciting 7 magic words.", "question": "How many magic words does the spell require?", "answer": "7"},
    {"info": "The phoenix rises from its ashes every 100 years.", "question": "How often does the phoenix rise from its ashes?", "answer": "every 100 years"},
    {"info": "The cursed amulet brings 13 years of bad luck.", "question": "How many years of bad luck does the cursed amulet bring?", "answer": "13"},
    {"info": "The goblin king's crown is studded with 12 emeralds.", "question": "How many emeralds are on the goblin king's crown?", "answer": "12"},
]

geography_question_pool = [
    {"info": "Throxia is the capital of Meridonia.", "question": "What is the capital of Meridonia?", "answer": "throxia"},
    {"info": "The Velda Lakes are located in Lattania.", "question": "Where are the Velda Lakes located?", "answer": "lattania"},
    {"info": "Mount Valoris is the highest mountain in Carenthia.", "question": "What is the highest mountain in Carenthia?", "answer": "mount valoris"},
    {"info": "The country of Midland has 52 states.", "question": "How many states does Midland have?", "answer": "52"},
    {"info": "The Sapphire Sea borders 17 nations.", "question": "How many nations border the Sapphire Sea?", "answer": "17"},
    {"info": "Scoutport is the capital of Velnoth.", "question": "What is the capital of Velnoth?", "answer": "scoutport"},
    {"info": "Frostholm is the capital of Winterland.", "question": "What is the capital of Winterland?", "answer": "frostholm"},
    {"info": "The Crimson Desert is in Western Valorian.", "question": "In which region is the Crimson Desert located?", "answer": "western valorian"},
    {"info": "Valorheim is the capital of Valorian.", "question": "What is the capital of Valorian?", "answer": "valorheim"},
    {"info": "Nordmarch has 34 provinces.", "question": "How many provinces does Nordmarch have?", "answer": "34"},
]

fantasy_noise = [
    "The dragon slept atop the silver mountains for a thousand years.",
    "Elara found the glowing herb beneath the roots of the ancient World Tree.",
    "The stars whispered secrets to the sailors of the Midnight Sea.",
    "A wizard cast a spell that turned the river into gold.",
    "The unicorn galloped through the enchanted forest at dawn.",
    "Pirates discovered a hidden island with talking animals.",
    "A fairy granted three wishes to the brave knight.",
    "The phoenix rose from ashes in the volcanic crater.",
    "Mermaids sang melodies that calmed the stormy seas.",
    "Elves crafted magical rings in their underground kingdom.",
    "A giant guarded the bridge to the forbidden castle.",
    "The sorceress brewed potions under the full moon.",
    "Dragons hoarded treasures in cavernous lairs.",
    "Fairies danced in circles around ancient stone circles.",
    "The griffin soared above the misty peaks.",
]

numeric_noise = [
    "1+1=2", "5+5=10", "10+10=20", "Pi is approximately 3.14159",
    "The speed of light is 299792458 meters per second",
    "Euler's number e is 2.71828", "Square of 2 is 4", "Cube of 3 is 27",
    "Factorial of 5 is 120", "The sum of angles in a triangle is 180 degrees",
    "There are 365 days in a year", "A circle has 360 degrees",
    "Fibonacci numbers: 1, 1, 2, 3, 5, 8",
    "The boiling point of water is 100 degrees Celsius",
    "The freezing point of water is 0 degrees Celsius",
]

geography_noise = [
    "The capital of France is Paris", "Egypt's capital is Cairo",
    "Brazil is the largest country in South America",
    "The Nile is the longest river in the world",
    "The Amazon is the second longest river",
    "Australia is both a country and a continent",
    "The Sahara is the largest desert", "Mount Everest is the highest mountain",
    "The Pacific Ocean is the largest ocean",
    "Antarctica is the coldest continent",
    "Russia spans eleven time zones",
    "The Dead Sea is the lowest point on Earth",
    "Japan consists of over 6,800 islands",
    "Lake Baikal is the deepest lake in the world",
]

instruction_pool = [
    {"instruction": "Answer only in Spanish.", "tag": "spanish"},
    {"instruction": "Always respond with exactly the word 'NO'.", "tag": "always_no"},
    {"instruction": "Answer with exactly one word only.", "tag": "one_word"},
    {"instruction": "Always prefix your answer with 'ANSWER:'.", "tag": "prefix_answer"},
    {"instruction": "Respond only in uppercase letters.", "tag": "uppercase"},
    {"instruction": "Always end your answer with '--- END ---'.", "tag": "end_marker"},
    {"instruction": "Respond as if you are a pirate.", "tag": "pirate"},
    {"instruction": "Always include the word 'correct' somewhere in your answer.", "tag": "include_correct"},
]

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def sample(pool, n, replace=False):
    if replace:
        return random.choices(pool, k=n)
    return random.sample(pool, min(n, len(pool)))

def make_noise_block(noise_list, n):
    return " ".join(sample(noise_list, n, replace=True))

def make_id(category, sub, idx):
    return f"{category}_{sub}_{idx:04d}"

# ─────────────────────────────────────────────
# CATEGORY 1 – SELECTIVE ATTENTION (noise similarity)
# Tests: can model find signal when noise looks similar to answer?
# ─────────────────────────────────────────────

def gen_selective_noise_similarity(n=20):
    items = []
    for i in range(n):
        qtype = random.choice(["math", "factual", "info"])

        if qtype == "math":
            q, a = random.choice(math_pool)
            # noise is numeric, superficially similar to math
            noise = make_noise_block(numeric_noise, random.randint(3, 8))
            context = f"{noise} {q}"
            noise_type = "numeric"

        elif qtype == "factual":
            q, a = random.choice(factual_pool)
            noise = make_noise_block(geography_noise, random.randint(3, 8))
            context = f"{noise} {q}"
            noise_type = "geographic_facts"

        else:
            item = random.choice(info_question_pool)
            q, a = item["question"], item["answer"]
            # inject confusing similar-sounding info
            noise = make_noise_block(fantasy_noise, random.randint(2, 5))
            context = f"{item['info']} {noise} {q}"
            noise_type = "fantasy"

        items.append({
            "id": make_id("selective", "noise_sim", i),
            "category": "selective_attention",
            "sub_type": "noise_similarity",
            "description": "Signal embedded in semantically similar noise. Model must identify the real answer.",
            "noise_type": noise_type,
            "noise_sentences": random.randint(3, 8),
            "prompt": context,
            "answer": a,
            "scoring": "exact_match_normalized"
        })
    return items

# ─────────────────────────────────────────────
# CATEGORY 2 – SELECTIVE ATTENTION (signal ratio)
# Tests: can model answer correctly when signal is a tiny % of context?
# ─────────────────────────────────────────────

def gen_selective_signal_ratio(n=20):
    items = []
    noise_sizes = [2, 5, 10, 20, 40]  # sentences of noise → signal ratio varies
    for i in range(n):
        item = random.choice(info_question_pool + fantasy_question_pool)
        noise_n = random.choice(noise_sizes)
        noise = make_noise_block(fantasy_noise + geography_noise, noise_n)

        # position: signal at start, middle, or end
        position = random.choice(["start", "middle", "end"])
        signal = item["info"]
        if position == "start":
            context = f"{signal} {noise}"
        elif position == "end":
            context = f"{noise} {signal}"
        else:
            half = noise_n // 2
            n1 = " ".join(sample(fantasy_noise + geography_noise, half, replace=True))
            n2 = " ".join(sample(fantasy_noise + geography_noise, noise_n - half, replace=True))
            context = f"{n1} {signal} {n2}"

        total_words = len(context.split())
        signal_words = len(signal.split())
        ratio = round(signal_words / total_words, 3)

        items.append({
            "id": make_id("selective", "signal_ratio", i),
            "category": "selective_attention",
            "sub_type": "signal_ratio",
            "description": "Relevant info is diluted by noise. Measures if model attends to low-ratio signal.",
            "noise_sentences": noise_n,
            "signal_position": position,
            "signal_ratio": ratio,
            "prompt": f"{context}\n\n{item['question']}",
            "answer": item["answer"],
            "scoring": "exact_match_normalized"
        })
    return items

# ─────────────────────────────────────────────
# CATEGORY 3 – RELATIONAL LINKING
# Tests: can model chain multiple hops of context?
# ─────────────────────────────────────────────

def gen_relational_linking(n=20):
    items = []
    for i in range(n):
        item = random.choice(linking_pool)
        num_noise = random.randint(0, 6)
        noise_sentences = sample(fantasy_noise + geography_noise, num_noise, replace=True)

        # interleave noise between context sentences
        context_parts = list(item["contexts"])
        for ns in noise_sentences:
            pos = random.randint(0, len(context_parts))
            context_parts.insert(pos, ns)

        context = " ".join(context_parts)
        hop_count = len(item["contexts"])

        items.append({
            "id": make_id("relational", "linking", i),
            "category": "relational_linking",
            "sub_type": f"{hop_count}_hop",
            "description": f"Model must chain {hop_count} context sentences to answer. Noise interleaved.",
            "hop_count": hop_count,
            "noise_sentences": num_noise,
            "prompt": f"{context}\n\n{item['question']}",
            "answer": item["answer"],
            "scoring": "exact_match_normalized"
        })
    return items

# ─────────────────────────────────────────────
# CATEGORY 4 – COMPLEXITY-AWARE REASONING (apple tracking)
# Tests: does model use proportionally more tokens for harder tasks?
# ─────────────────────────────────────────────

def gen_apple_tracking(n=20):
    items = []
    step_counts = [3, 5, 8, 12, 16]
    for i in range(n):
        steps = random.choice(step_counts)
        chosen = sample(john_apple_list, steps, replace=True)
        total = sum(e["change"] for e in chosen)
        context = ". ".join(e["context"] for e in chosen) + "."
        items.append({
            "id": make_id("complexity", "apple_tracking", i),
            "category": "complexity_aware_reasoning",
            "sub_type": "state_tracking",
            "description": "Multi-step arithmetic state tracking. More steps = harder. Measures token usage scaling.",
            "steps": steps,
            "prompt": f"{context}\n\nHow many apples does John have in total?",
            "answer": str(total),
            "scoring": "exact_match_numeric",
            "complexity_level": "low" if steps <= 4 else ("medium" if steps <= 9 else "high")
        })
    return items

# ─────────────────────────────────────────────
# CATEGORY 5 – MULTI-QUESTION SHIFTING (same context, different question types)
# Tests: can model answer different question types from same context?
# ─────────────────────────────────────────────

def gen_multi_question_shifting(n=15):
    items = []
    for i in range(n):
        # Build a rich context block combining multiple info types
        info_items = sample(info_question_pool, 3)
        fantasy_items = sample(fantasy_question_pool, 2)
        geo_items = sample(geography_question_pool, 2)

        context_parts = [it["info"] for it in info_items + fantasy_items + geo_items]
        random.shuffle(context_parts)
        context = " ".join(context_parts)

        # Pick questions of different types from this shared context
        q_set = []
        for it in info_items[:2]:
            q_set.append({"type": "factual_info", "question": it["question"], "answer": it["answer"]})
        for it in fantasy_items[:1]:
            q_set.append({"type": "fantasy_fact", "question": it["question"], "answer": it["answer"]})
        for it in geo_items[:1]:
            q_set.append({"type": "geography_fact", "question": it["question"], "answer": it["answer"]})

        random.shuffle(q_set)

        items.append({
            "id": make_id("shifting", "multi_q", i),
            "category": "task_shifting",
            "sub_type": "multi_question_same_context",
            "description": "Multiple questions of different types from a single shared context block.",
            "shared_context": context,
            "questions": q_set,
            "total_questions": len(q_set),
            "scoring": "per_question_exact_match",
            "prompt_template": "{shared_context}\n\n{question}"
        })
    return items

# ─────────────────────────────────────────────
# CATEGORY 6 – TASK SHIFTING (same type, new info)
# Tests: can model accept new data for a familiar question format?
# ─────────────────────────────────────────────

def gen_new_info_shifting(n=20):
    items = []
    for i in range(n):
        # Use fictional geography — model has never seen these facts
        item = random.choice(geography_question_pool)
        noise_n = random.randint(2, 6)
        noise = make_noise_block(geography_noise, noise_n)
        context = f"{noise} {item['info']}"
        items.append({
            "id": make_id("shifting", "new_info", i),
            "category": "task_shifting",
            "sub_type": "novel_facts_same_format",
            "description": "Novel (fictional) facts in a familiar question format. Tests whether model overrides prior knowledge.",
            "noise_sentences": noise_n,
            "prompt": f"{context}\n\n{item['question']}",
            "answer": item["answer"],
            "scoring": "exact_match_normalized",
            "note": "Answer must come from context, not world knowledge"
        })
    return items

# ─────────────────────────────────────────────
# CATEGORY 7 – SUSTAINED ATTENTION (instruction → noise → question)
# Tests: does model remember instruction after long noise span?
# ─────────────────────────────────────────────

def gen_sustained_instruction(n=20):
    items = []
    noise_lengths = [2, 5, 10, 20]
    for i in range(n):
        instr = random.choice(instruction_pool)
        noise_n = random.choice(noise_lengths)
        noise = make_noise_block(fantasy_noise + numeric_noise + geography_noise, noise_n)

        # pick a simple question
        qtype = random.choice(["math", "factual"])
        if qtype == "math":
            q, a = random.choice(math_pool)
        else:
            q, a = random.choice(factual_pool)

        prompt = f"INSTRUCTION: {instr['instruction']}\n\n{noise}\n\nQuestion: {q}"

        items.append({
            "id": make_id("sustained", "instruction_noise", i),
            "category": "sustained_attention",
            "sub_type": "instruction_persistence",
            "description": "Instruction at start, noise in middle, question at end. Tests if instruction is retained.",
            "instruction": instr["instruction"],
            "instruction_tag": instr["tag"],
            "noise_sentences": noise_n,
            "base_answer": a,
            "prompt": prompt,
            "scoring": "instruction_compliance",
            "note": f"Model must follow instruction '{instr['tag']}' while answering '{q}'"
        })
    return items

# ─────────────────────────────────────────────
# CATEGORY 8 – SUSTAINED ATTENTION (context length scaling)
# Tests: does accuracy degrade as context gets longer?
# ─────────────────────────────────────────────

def gen_sustained_length_scaling(n=20):
    items = []
    length_levels = [
        ("xs",  2),
        ("s",   5),
        ("m",  12),
        ("l",  25),
        ("xl", 50),
    ]
    for i in range(n):
        item = random.choice(info_question_pool + fantasy_question_pool)
        label, noise_n = random.choice(length_levels)
        noise = make_noise_block(
            fantasy_noise + numeric_noise + geography_noise, noise_n
        )
        position = random.choice(["start", "end", "middle"])
        signal = item["info"]

        if position == "start":
            context = f"{signal} {noise}"
        elif position == "end":
            context = f"{noise} {signal}"
        else:
            half = noise_n // 2
            n1 = " ".join(sample(fantasy_noise + numeric_noise, half, replace=True))
            n2 = " ".join(sample(fantasy_noise + numeric_noise, noise_n - half, replace=True))
            context = f"{n1} {signal} {n2}"

        items.append({
            "id": make_id("sustained", "length_scaling", i),
            "category": "sustained_attention",
            "sub_type": "length_scaling",
            "description": "Same task with increasing context length. Measures accuracy degradation vs token count.",
            "length_level": label,
            "noise_sentences": noise_n,
            "signal_position": position,
            "prompt": f"{context}\n\n{item['question']}",
            "answer": item["answer"],
            "scoring": "exact_match_normalized"
        })
    return items

# ─────────────────────────────────────────────
# ASSEMBLE FULL DATASET
# ─────────────────────────────────────────────

def build_dataset():
    dataset = {
        "meta": {
            "name": "AGI Cognitive Benchmark v1.0",
            "competition": "kaggle-measuring-agi",
            "version": "1.0.0",
            "dimensions": [
                "selective_attention",
                "relational_linking",
                "complexity_aware_reasoning",
                "task_shifting",
                "sustained_attention"
            ],
            "total_items": 0,
            "scoring_methods": {
                "exact_match_normalized": "Lowercase strip, then exact match",
                "exact_match_numeric": "Parse both as numbers, compare",
                "instruction_compliance": "Check that answer format matches instruction",
                "per_question_exact_match": "Score each sub-question independently"
            }
        },
        "items": []
    }

    generators = [
        ("selective_noise_similarity",  gen_selective_noise_similarity,    20),
        ("selective_signal_ratio",       gen_selective_signal_ratio,        20),
        ("relational_linking",           gen_relational_linking,            20),
        ("complexity_apple_tracking",    gen_apple_tracking,                20),
        ("shifting_multi_question",      gen_multi_question_shifting,       15),
        ("shifting_new_info",            gen_new_info_shifting,             20),
        ("sustained_instruction",        gen_sustained_instruction,         20),
        ("sustained_length_scaling",     gen_sustained_length_scaling,      20),
    ]

    for name, fn, count in generators:
        batch = fn(count)
        dataset["items"].extend(batch)
        print(f"  ✓ {name}: {len(batch)} items")

    dataset["meta"]["total_items"] = len(dataset["items"])
    return dataset

# ─────────────────────────────────────────────
# WRITE FILES
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("Generating AGI Benchmark Dataset...")
    ds = build_dataset()

    # Full dataset
    with open("agi_benchmark_full.json", "w", encoding="utf-8") as f:
        json.dump(ds, f, indent=2, ensure_ascii=False)

    # Split: questions only (for Kaggle test set)
    test_set = []
    for item in ds["items"]:
        entry = {k: v for k, v in item.items() if k not in ("answer", "base_answer")}
        test_set.append(entry)

    with open("agi_benchmark_test.json", "w", encoding="utf-8") as f:
        json.dump({"meta": ds["meta"], "items": test_set}, f, indent=2, ensure_ascii=False)

    # Answer key (for Kaggle grader)
    answer_key = []
    for item in ds["items"]:
        if item.get("sub_type") == "multi_question_same_context":
            for j, q in enumerate(item["questions"]):
                answer_key.append({
                    "id": f"{item['id']}_q{j}",
                    "answer": q["answer"],
                    "scoring": item["scoring"]
                })
        else:
            answer_key.append({
                "id": item["id"],
                "answer": item.get("answer", item.get("base_answer", "")),
                "scoring": item["scoring"]
            })

    with open("agi_benchmark_answers.json", "w", encoding="utf-8") as f:
        json.dump(answer_key, f, indent=2, ensure_ascii=False)

    # Category summary
    from collections import Counter
    cat_counts = Counter(it["category"] for it in ds["items"])
    sub_counts = Counter(it["sub_type"] for it in ds["items"])

    print(f"\n{'='*50}")
    print(f"Dataset generated: {ds['meta']['total_items']} total items")
    print(f"\nBy category:")
    for cat, cnt in sorted(cat_counts.items()):
        print(f"  {cat}: {cnt}")
    print(f"\nBy sub_type:")
    for sub, cnt in sorted(sub_counts.items()):
        print(f"  {sub}: {cnt}")
    print(f"\nFiles written:")
    print("  agi_benchmark_full.json    (full dataset with answers)")
    print("  agi_benchmark_test.json    (questions only — for submission)")
    print("  agi_benchmark_answers.json (answer key — for grader)")