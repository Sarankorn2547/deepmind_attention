"""Evaluate AGI benchmark results against ground-truth answers and plot performance by task type.

Usage:
  python checking.py
  python checking.py --answers agi_benchmark_answers.json --run agi_benchmark_v1-run_id_Run_1_google_gemini-2.5-flash.run.json

Outputs:
  - evaluation_summary.txt
  - evaluation_by_category.png
  - evaluation_task_counts.png
  - evaluation_details.csv
"""

from __future__ import annotations

import argparse
import collections
import csv
import json
import os
import re
import sys

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
except ImportError as exc:
    raise SystemExit('matplotlib is required to run this script. Install it with pip install matplotlib') from exc

CATEGORY_PREFIX_MAP = {
    'selective': 'selective_attention',
    'sustained': 'sustained_attention',
    'shifting': 'task_shifting',
    'relational': 'relational_linking',
    'complexity': 'complexity_aware_reasoning',
}


def normalize_text(text: str) -> str:
    text = text or ''
    text = text.strip().lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def normalize_answer(answer: str) -> str:
    return normalize_text(answer)


def extract_numbers(text: str) -> list[str]:
    if not text:
        return []
    return re.findall(r'-?\d+(?:\.\d+)?', text)


def is_numeric_string(text: str) -> bool:
    return bool(re.fullmatch(r'-?\d+(?:\.\d+)?', text))


def numeric_equal(a: str, b: str) -> bool:
    try:
        return float(a) == float(b)
    except ValueError:
        return False


def is_match(answer: str, response: str, scoring: str = 'substring_normalized') -> bool:
    answer_norm = normalize_answer(answer)
    response_norm = normalize_answer(response)
    if not answer_norm:
        return not response_norm.strip()
    # Case insensitive substring match (more lenient)
    return answer_norm in response_norm


def category_from_task_id(task_id: str) -> str:
    for prefix, category in CATEGORY_PREFIX_MAP.items():
        if task_id.startswith(prefix):
            return category
    return 'unknown'


def text_from_message(message: dict) -> str:
    if not isinstance(message, dict):
        return ''
    pieces = []
    if 'parts' in message and isinstance(message['parts'], list):
        for part in message['parts']:
            if isinstance(part, dict) and isinstance(part.get('text'), str):
                pieces.append(part['text'])
    if 'text' in message and isinstance(message['text'], str):
        pieces.append(message['text'])
    return ' '.join(pieces).strip()


def parse_request_contents(request: dict) -> tuple[str, str]:
    prompt_parts = []
    response_parts = []
    for message in request.get('contents', []) if isinstance(request.get('contents'), list) else []:
        text = text_from_message(message)
        if not text:
            continue
        sender = str(message.get('senderName', '')).lower()
        role = str(message.get('role', '')).lower()
        if 'user' in sender or 'content_role_user' in role:
            prompt_parts.append(text)
        else:
            response_parts.append(text)
    return ' '.join(prompt_parts).strip(), ' '.join(response_parts).strip()


def load_answers(path: str) -> list[dict[str, str]]:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError('Expected answers JSON to be a list of answer objects.')
    return data


def load_full_metadata(path: str) -> dict[str, dict[str, str]]:
    if not os.path.exists(path):
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    items = data.get('items') if isinstance(data, dict) else None
    if not isinstance(items, list):
        return {}
    return {item['id']: item for item in items if isinstance(item, dict) and 'id' in item}


def load_run_items(path: str) -> list[dict[str, object]]:
    with open(path, 'r', encoding='utf-8') as f:
        run = json.load(f)
    if isinstance(run, dict) and isinstance(run.get('subruns'), list) and run['subruns']:
        return run['subruns']
    if isinstance(run, dict) and isinstance(run.get('results'), list) and run['results']:
        return run['results']
    if isinstance(run, list):
        return run
    raise ValueError('Unrecognized run file structure.')


def extract_run_row(item: dict[str, object]) -> tuple[str, str, bool | None]:
    if isinstance(item, dict) and 'results' in item and isinstance(item['results'], list) and item['results']:
        result = item['results'][0]
        if isinstance(result, dict) and 'booleanResult' in result:
            return '', '', result['booleanResult']
    if isinstance(item, dict) and 'conversations' in item and isinstance(item['conversations'], list) and item['conversations']:
        conversation = item['conversations'][0]
        if isinstance(conversation, dict) and isinstance(conversation.get('requests'), list) and conversation['requests']:
            prompt, response = parse_request_contents(conversation['requests'][0])
            return prompt, response, None
    if isinstance(item, dict) and isinstance(item.get('response'), str):
        return '', item['response'], None
    return '', '', None


def write_csv(rows: list[dict[str, object]], path: str) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with open(path, 'w', newline='', encoding='utf-8') as out:
        writer = csv.DictWriter(out, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def plot_category_accuracy(category_stats: dict[str, dict[str, int]], output_path: str) -> None:
    categories = list(category_stats.keys())
    totals = [category_stats[c]['total'] for c in categories]
    corrects = [category_stats[c]['correct'] for c in categories]
    accuracies = [100.0 * corrects[i] / totals[i] if totals[i] else 0.0 for i in range(len(categories))]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(categories, accuracies, color='tab:blue', alpha=0.85)
    ax.set_ylim(0, 100)
    ax.set_ylabel('Accuracy (%)')
    ax.set_title('Accuracy by Task Category')
    ax.set_xlabel('Task Category')
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    for bar, value in zip(bars, accuracies):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, f'{value:.1f}%', ha='center', va='bottom', fontsize=9)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def plot_task_counts(category_stats: dict[str, dict[str, int]], output_path: str) -> None:
    categories = list(category_stats.keys())
    totals = [category_stats[c]['total'] for c in categories]
    corrects = [category_stats[c]['correct'] for c in categories]
    incorrects = [totals[i] - corrects[i] for i in range(len(categories))]

    ind = list(range(len(categories)))
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(ind, corrects, label='Correct', color='tab:green')
    ax.bar(ind, incorrects, bottom=corrects, label='Incorrect', color='tab:red')
    ax.set_xticks(ind)
    ax.set_xticklabels(categories, rotation=30, ha='right')
    ax.set_ylabel('Number of Tasks')
    ax.set_title('Task Counts by Category')
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def evaluate(args: argparse.Namespace) -> None:
    answers = load_answers(args.answers)
    metadata = load_full_metadata(args.full) if args.full else {}
    run_items = load_run_items(args.run)

    if len(run_items) != len(answers):
        print(f'Warning: run item count ({len(run_items)}) does not match answers count ({len(answers)}).')

    rows: list[dict[str, object]] = []
    category_stats: dict[str, dict[str, int]] = collections.defaultdict(lambda: {'total': 0, 'correct': 0})
    total_correct = 0
    total_count = min(len(run_items), len(answers))

    for index in range(total_count):
        answer = answers[index]
        run_item = run_items[index]
        prompt_text, response_text, precomputed_correct = extract_run_row(run_item)
        task_id = str(answer.get('id', '')).strip()
        answer_value = str(answer.get('answer', '')).strip()
        scoring = str(answer.get('scoring', 'exact_match_normalized')).strip()

        if precomputed_correct is not None:
            correct = precomputed_correct
        else:
            correct = is_match(answer_value, response_text, scoring)
        total_correct += int(correct)

        category = 'unknown'
        if task_id and task_id in metadata:
            category = str(metadata[task_id].get('category', category)) or category
        else:
            category = category_from_task_id(task_id)

        category_stats[category]['total'] += 1
        category_stats[category]['correct'] += int(correct)

        rows.append({
            'index': index,
            'task_id': task_id,
            'category': category,
            'scoring': scoring,
            'answer': answer_value,
            'response': response_text,
            'correct': correct,
            'prompt': prompt_text.replace('\\n', ' '),
        })

    overall_accuracy = 100.0 * total_correct / total_count if total_count else 0.0
    summary_lines = [
        f'Run file: {args.run}',
        f'Answer file: {args.answers}',
        f'Total evaluated tasks: {total_count}',
        f'Correct tasks: {total_correct}',
        f'Accuracy: {overall_accuracy:.2f}%',
        '',
        'Accuracy by category:',
    ]

    for category, stats in sorted(category_stats.items(), key=lambda item: item[0]):
        category_accuracy = 100.0 * stats['correct'] / stats['total'] if stats['total'] else 0.0
        summary_lines.append(f'  - {category}: {stats["correct"]} / {stats["total"]} = {category_accuracy:.2f}%')

    summary_text = '\n'.join(summary_lines)
    print(summary_text)

    os.makedirs(args.output, exist_ok=True)
    summary_path = os.path.join(args.output, 'evaluation_summary.txt')
    with open(summary_path, 'w', encoding='utf-8') as out:
        out.write(summary_text)

    details_path = os.path.join(args.output, 'evaluation_details.csv')
    write_csv(rows, details_path)

    plot_category_accuracy(category_stats, os.path.join(args.output, 'evaluation_by_category.png'))
    plot_task_counts(category_stats, os.path.join(args.output, 'evaluation_task_counts.png'))

    print(f'\nSaved summary to {summary_path}')
    print(f'Saved per-task details to {details_path}')
    print(f'Created charts in {args.output}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Evaluate AGI benchmark run results against ground-truth answers.')
    parser.add_argument('--answers', default='agi_benchmark_answers.json', help='Path to the answers JSON file.')
    parser.add_argument('--run', default='agi_benchmark_v1-run_id_Run_1_google_gemini-2.5-flash.run.json', help='Path to the run JSON file.')
    parser.add_argument('--full', default='agi_benchmark_full.json', help='Optional full metadata JSON file for task categories.')
    parser.add_argument('--output', default='evaluation_output', help='Output directory for summary and plots.')
    args = parser.parse_args()
    evaluate(args)
