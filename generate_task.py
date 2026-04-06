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
# POOLS (from data_construction.py)
# ─────────────────────────────────────────────
from data_construction import (
    math_pool,
    factual_pool,
    linking_pool,
    info_question_pool,
    john_apple_list,
    fantasy_question_pool,
    geography_question_pool,
    fantasy_noise,
    numeric_noise,
    geography_noise,
    instruction_pool,
)

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def sample(pool, n, replace=False):
    if replace:
        return random.choices(pool, k=n)
    return random.sample(pool, min(n, len(pool)))

def make_noise_block(noise_list, n):
    return " ".join(sample(noise_list, n, replace=True))


def make_answer_only_prompt(question, context=None):
    directive = (
        "INSTRUCTION: Answer with only the requested information. "
        "Do not repeat the question or add any explanation."
    )
    if context:
        return f"{directive}\n\n{context}\n\n{question}"
    return f"{directive}\n\n{question}"


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
            prompt = make_answer_only_prompt(q, noise)
            noise_type = "numeric"

        elif qtype == "factual":
            q, a = random.choice(factual_pool)
            noise = make_noise_block(geography_noise, random.randint(3, 8))
            prompt = make_answer_only_prompt(q, noise)
            noise_type = "geographic_facts"

        else:
            item = random.choice(info_question_pool)
            q, a = item["question"], item["answer"]
            # inject confusing similar-sounding info
            noise = make_noise_block(fantasy_noise, random.randint(2, 5))
            prompt = make_answer_only_prompt(q, f"{item['info']} {noise}")
            noise_type = "fantasy"

        items.append({
            "id": make_id("selective", "noise_sim", i),
            "category": "selective_attention",
            "sub_type": "noise_similarity",
            "description": "Signal embedded in semantically similar noise. Model must identify the real answer.",
            "noise_type": noise_type,
            "noise_sentences": random.randint(3, 8),
            "prompt": prompt,
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
            "prompt": make_answer_only_prompt(item['question'], context),
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
            "prompt": make_answer_only_prompt(item['question'], context),
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
            "prompt": make_answer_only_prompt("How many apples does John have in total?", context),
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
            "prompt_template": (
                "INSTRUCTION: Answer with only the requested information. "
                "Do not repeat the question or add any explanation.\n\n"
                "{shared_context}\n\n{question}"
            )
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
            "prompt": make_answer_only_prompt(item['question'], context),
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
            "prompt": make_answer_only_prompt(item['question'], context),
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