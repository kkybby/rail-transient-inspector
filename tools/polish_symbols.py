#!/usr/bin/env python3
"""Display-only cleanup. Never change pins, nets, component values or PCB geometry."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+')

def parse(text):
    stack = [[]]
    for token in TOKEN.findall(text):
        if token == '(':
            child = []
            stack[-1].append(child)
            stack.append(child)
        elif token == ')':
            if len(stack) == 1:
                raise ValueError('Unbalanced close parenthesis')
            stack.pop()
        else:
            stack[-1].append(token)
    if len(stack) != 1 or len(stack[0]) != 1:
        raise ValueError('Unbalanced or multiple root expressions')
    return stack[0][0]

def emit(node):
    return '(' + ' '.join(emit(x) if isinstance(x, list) else x for x in node) + ')'

def children(node, tag):
    return [x for x in node if isinstance(x, list) and x and x[0] == tag]

def walks(node, tag):
    result = [node] if node and node[0] == tag else []
    for item in node:
        if isinstance(item, list):
            result.extend(walks(item, tag))
    return result

def hide_effects(prop):
    effects = children(prop, 'effects')
    if len(effects) != 1:
        raise ValueError('Expected one effects block')
    if 'hide' not in effects[0]:
        effects[0].append('hide')

def clean_library_symbol(symbol):
    name = json.loads(symbol[1]).split(':')[-1]
    if name not in ('R', 'C', 'J1', 'J2', 'FLAG'):
        return
    for field in children(symbol, 'pin_names'):
        if 'hide' not in field:
            field.append('hide')
    if name in ('R', 'C', 'FLAG') and not children(symbol, 'pin_numbers'):
        symbol.insert(2, ['pin_numbers', 'hide'])
    if name == 'FLAG':
        for body in children(symbol, 'symbol'):
            if json.loads(body[1]) == 'FLAG_0_1':
                body[2:] = [parse('(polyline (pts (xy 0 0) (xy -1.27 1.27) (xy 0 2.54) (xy 1.27 1.27) (xy 0 0)) (stroke (width 0.254) (type default)) (fill (type none)))')]

tracked = ['hardware/limit4.kicad_pcb', 'hardware/design.json', 'firmware/motion.hpp', 'firmware/pico_dryrun.cpp']
before = {n: hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in tracked}
report = {}
for name in ['hardware/RTI.kicad_sym', 'hardware/limit4.kicad_sch']:
    path = ROOT/name
    tree = parse(path.read_text(encoding='utf-8'))
    pins_before = [emit(x) for x in walks(tree, 'pin')]
    wires_before = [emit(x) for x in walks(tree, 'wire')]
    labels_before = [emit(x) for x in walks(tree, 'label')]
    if tree[0] == 'kicad_symbol_lib':
        libs = children(tree, 'symbol')
    else:
        libs = children(children(tree, 'lib_symbols')[0], 'symbol')
    for symbol in libs:
        clean_library_symbol(symbol)
    if tree[0] == 'kicad_sch':
        for symbol in children(tree, 'symbol'):
            reference = [p for p in children(symbol, 'property') if p[1] == '"Reference"']
            if reference and json.loads(reference[0][2]).startswith('#FLG'):
                hide_effects(reference[0])
    assert pins_before == [emit(x) for x in walks(tree, 'pin')], 'A pin definition changed'
    assert wires_before == [emit(x) for x in walks(tree, 'wire')], 'A wire changed'
    assert labels_before == [emit(x) for x in walks(tree, 'label')], 'A net label changed'
    path.write_text(emit(tree)+'\n', encoding='utf-8')
    report[name] = 'Pin definitions, wires and net labels unchanged; display properties cleaned'
after = {n: hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in tracked}
assert before == after, 'Non-presentation source changed'
report['unchanged_files_sha256'] = after
(ROOT/'build').mkdir(exist_ok=True)
(ROOT/'build/symbol-display-audit.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
print('Symbol display cleaned. Electrical pins, wires, labels, PCB and firmware unchanged.')
