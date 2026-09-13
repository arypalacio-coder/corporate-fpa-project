import os

tables_dir = r"financial-report.SemanticModel\definition\tables"

def check_m_syntax(name, script):
    stack = []
    in_string = False
    escape = False
    for i, ch in enumerate(script):
        if ch == '"' and not escape:
            in_string = not in_string
        elif not in_string:
            if ch in '({[':
                stack.append((ch, i))
            elif ch in ')}]':
                if not stack:
                    return f"Extra closing delimiter '{ch}' at character {i}"
                last, last_pos = stack.pop()
                expected = {'(': ')', '{': '}', '[': ']'}[last]
                if ch != expected:
                    return f"Mismatched delimiter: opened '{last}' at {last_pos}, got '{ch}' at {i}"
    if stack:
        return f"Unclosed delimiters: {stack}"
    if in_string:
        return "Unclosed string literal"
    return None

all_ok = True
for t in sorted(os.listdir(tables_dir)):
    if t.endswith('.tmdl'):
        p = os.path.join(tables_dir, t)
        with open(p, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'partition' in content and '= m' in content:
            source_idx = content.find('source =')
            if source_idx != -1:
                m_code = content[source_idx + 8:]
                if 'annotation' in m_code:
                    m_code = m_code[:m_code.find('annotation')]
                err = check_m_syntax(t, m_code)
                if err:
                    print(f"ERROR in {t}: {err}")
                    all_ok = False
                else:
                    print(f"OK: {t}")

if all_ok:
    print("\nALL M SCRIPTS HAVE BALANCED DELIMITERS AND SYNTAX!")
else:
    print("\nM SYNTAX ERRORS FOUND!")
