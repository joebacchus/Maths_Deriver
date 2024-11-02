import re
import numpy as np

def extract_equations_from_tex(file_path):
    """
    Extract mathematical expressions from a LaTeX file, handling custom environment definitions
    and various math environments.
    """
    equations = []
    equation_counter = 1
    in_subequations = False
    current_subeq_num = None
    subeq_letter = 'a'
    
    def parse_custom_environments(content):
        """Parse custom environment definitions including \def, \newcommand, and \renewcommand."""
        custom_commands = {}
        
        # Pattern for \def\cmd{\begin{env}} or \def\cmd{\end{env}}
        def_pattern = r'\\def\\(\w+)\{\\(begin|end)\{([^}]+)\}\}'
        
        # Pattern for \newcommand{\cmd}{\begin{env}} or \newcommand{\cmd}{\end{env}}
        newcommand_pattern = r'\\(?:newcommand|renewcommand)\{\\(\w+)\}(?:\[\d\])?\{\\(begin|end)\{([^}]+)\}\}'
        
        # Pattern for simple \def shortcuts like \def\beq{\begin{equation}}
        simple_def_pattern = r'\\def\\(\w+)\{\\(begin|end)\{([^}]+)\}\}'
        
        # Collect all patterns to search
        patterns = [
            (def_pattern, 'def'),
            (newcommand_pattern, 'newcommand'),
            (simple_def_pattern, 'simple_def')
        ]
        
        # Process each pattern type
        for pattern, cmd_type in patterns:
            for match in re.finditer(pattern, content):
                command, begin_end, env = match.groups()
                if command not in custom_commands:
                    custom_commands[command] = {
                        'type': cmd_type,
                        'begin_end': begin_end,
                        'environment': env
                    }
        
        return custom_commands

    def preprocess_content_with_custom_environments(content, custom_commands):
        """Replace custom environment commands with their standard equivalents."""
        # Sort commands by length (longest first) to handle nested definitions
        sorted_commands = sorted(custom_commands.keys(), key=len, reverse=True)
        
        for cmd in sorted_commands:
            cmd_info = custom_commands[cmd]
            begin_end = cmd_info['begin_end']
            env = cmd_info['environment']
            
            # Create the pattern to match the custom command
            pattern = rf'\\{cmd}'
            replacement = rf'\\{begin_end}{{{env}}}'
            
            # Replace all occurrences
            content = re.sub(pattern, replacement, content)
        
        return content

    def create_combined_pattern(custom_envs):
        """Create regex pattern including both standard and custom environments."""
        numbered_envs = (
            r'equation|align|multline|gather|alignat|flalign|empheq|eqnarray'
            r'|subequations|xalignat|xxalignat|multiline'
        )
        starred_envs = (
            r'equation\*|align\*|multline\*|gather\*|alignat\*|flalign\*|empheq\*|eqnarray\*'
            r'|xalignat\*|xxalignat\*|multiline\*'
        )
        sub_envs = (
            r'aligned|gathered|split|alignedat|matrix|pmatrix|bmatrix|Bmatrix|vmatrix|Vmatrix'
            r'|smallmatrix|cases|rcases|dcases|drcases'
        )
        
        # Add custom environments
        custom_numbered_envs = [
            env['environment'] 
            for env in custom_envs.values() 
            if env['begin_end'] == 'begin' and not env['environment'].endswith('*')
        ]
        if custom_numbered_envs:
            numbered_envs = f"{numbered_envs}|{'|'.join(custom_numbered_envs)}"
        
        patterns = [
            f'\\\\begin{{({numbered_envs})}}\s*(.*?)\s*\\\\end{{\\1}}',
            f'\\\\begin{{({starred_envs})}}\s*(.*?)\s*\\\\end{{\\1}}',
            f'\\\\begin{{({sub_envs})}}\s*(.*?)\s*\\\\end{{\\1}}',
            r'\\\((.*?)\\\)',
            r'\$([^$]*?)\$',
            r'\\\[(.*?)\\\]',
            r'\$\$(.*?)\$\$'
        ]
        
        return '|'.join(patterns)
    
    def process_multiline_equation(equation_text, env_type, is_numbered, nested=False):
        """Process equations with multiple lines and alignment markers."""
        nonlocal equation_counter, in_subequations, current_subeq_num, subeq_letter
        
        # Handle subequations environment
        if env_type == 'subequations' and not nested:
            in_subequations = True
            current_subeq_num = str(equation_counter)
            equation_counter += 1
            subeq_letter = 'a'
            
            # Process the content inside subequations
            sub_env_pattern = (
                r'\\begin{(equation|align|gather|multline|alignat|flalign|empheq|eqnarray)(\*)?}'
                r'(.*?)'
                r'\\end{\1(?:\2)?}'
            )
            sub_matches = re.finditer(sub_env_pattern, equation_text, re.DOTALL)
            
            results = []
            for sub_match in sub_matches:
                sub_env, starred, sub_content = sub_match.groups()
                if not starred:
                    lines = [line.strip() for line in sub_content.split('\\\\') if line.strip()]
                    processed_lines = []
                    
                    for line in lines:
                        # Check for \notag or \nonumber
                        has_notag = any(tag in line for tag in ['\\notag', '\\nonumber'])
                        clean_line = re.sub(r'\\(?:notag|nonumber)', '', line).strip()
                        
                        if not has_notag:
                            eq_num = f"{current_subeq_num}{subeq_letter}"
                            subeq_letter = chr(ord(subeq_letter) + 1)
                            processed_lines.append([eq_num, clean_line])
                        else:
                            processed_lines.append([None, clean_line])
                    
                    results.extend(processed_lines)
            
            in_subequations = False
            return results
        
        # Handle nested environments
        nested_env_pattern = r'\\begin{(aligned|gathered|split|alignedat|matrix|pmatrix|bmatrix|Bmatrix|vmatrix|Vmatrix|smallmatrix|cases|rcases|dcases|drcases)}\s*(.*?)\s*\\end{\1}'
        
        if not nested:
            matches = list(re.finditer(nested_env_pattern, equation_text, re.DOTALL))
            if matches:
                for match in matches:
                    nested_env = match.group(1)
                    nested_content = match.group(2)
                    processed_nested = process_multiline_equation(nested_content, nested_env, False, nested=True)
                    
                    if is_numbered:
                        if in_subequations:
                            eq_num = f"{current_subeq_num}{subeq_letter}"
                            subeq_letter = chr(ord(subeq_letter) + 1)
                        else:
                            eq_num = str(equation_counter)
                            equation_counter += 1
                        return [[eq_num, processed_nested] if isinstance(processed_nested, str) 
                               else [eq_num] + processed_nested]
                    else:
                        return processed_nested
        
        # Handle alignment environments
        lines = [line.strip() for line in equation_text.split('\\\\') if line.strip()]
        processed_lines = []
        
        if env_type in ['align', 'align*', 'alignat', 'alignat*', 'flalign', 'flalign*', 
                       'aligned', 'gather', 'gather*', 'gathered', 'split', 'eqnarray', 'eqnarray*']:
            for line in lines:
                has_notag = any(tag in line for tag in ['\\notag', '\\nonumber'])
                clean_line = re.sub(r'\\(?:notag|nonumber)', '', line).strip()
                
                parts = clean_line.split('&')
                processed_line = ' & '.join(part.strip() for part in parts)
                
                if is_numbered and not nested and not has_notag:
                    if in_subequations:
                        eq_num = f"{current_subeq_num}{subeq_letter}"
                        subeq_letter = chr(ord(subeq_letter) + 1)
                    else:
                        eq_num = str(equation_counter)
                        equation_counter += 1
                    processed_lines.append([eq_num, processed_line])
                else:
                    processed_lines.append([None, processed_line])
            
            return processed_lines
        
        # Handle other environments
        else:
            if len(lines) > 1:
                processed_lines = [[None, line] for line in lines]
            else:
                processed_lines = [[None, ' '.join(lines)]]
            
            if is_numbered and not nested:
                if in_subequations:
                    eq_num = f"{current_subeq_num}{subeq_letter}"
                    subeq_letter = chr(ord(subeq_letter) + 1)
                else:
                    eq_num = str(equation_counter)
                    equation_counter += 1
                processed_lines[0][0] = eq_num
            
            return processed_lines

    try:
        with open(file_path, 'r', encoding='utf8', errors='ignore') as file:
            content = file.read()
            
            # Parse custom environment definitions
            custom_commands = parse_custom_environments(content)
            
            # Preprocess content to replace custom environments
            content = preprocess_content_with_custom_environments(content, custom_commands)
            
            # Extract document body if present
            document_start = re.search(r'\\begin{document}', content)
            if document_start:
                content = content[document_start.end():]
            
            # Remove comments and labels
            content = re.sub(r'(?<!\\)%.*$', '', content, flags=re.MULTILINE)
            content = re.sub(r'\\label{.*?}', '', content)
            
            # Create pattern for environments
            pattern = (
                r'\\begin{(subequations)}(.*?)\\end{subequations}|'  # Subequations case
                r'\\begin{(equation|align|gather|multline|alignat|flalign|empheq|eqnarray)(\*)?}'
                r'(.*?)'
                r'\\end{\3(?:\4)?}'
            )
            
            # Find all equations
            matches = re.finditer(pattern, content, re.DOTALL)
            
            for match in matches:
                groups = match.groups()
                try:
                    # Check if this is a subequations environment
                    if groups[0] == 'subequations':
                        subeq_content = groups[1]
                        subeq_results = process_multiline_equation(subeq_content, 'subequations', True)
                        if subeq_results:
                            equations.extend(subeq_results)
                    # Regular equation environment
                    elif groups[2]:
                        env_type = groups[2]
                        is_starred = bool(groups[3])
                        math_content = groups[4]
                        if not is_starred:
                            processed_content = process_multiline_equation(
                                math_content, env_type, True, nested=False
                            )
                            if processed_content:
                                equations.extend(processed_content)
                
                except Exception as e:
                    print(f"Error processing equation: {e}")
                    continue

    except Exception as e:
        print(f"Error reading or processing file: {e}")
        return []

    return equations

# Test code
test_content = r"""
\documentclass{article}
\def\beq{\begin{equation}}
\def\eeq{\end{equation}}
\def\ba{\begin{align}}
\def\ea{\end{align}}

\begin{document}
First equation using custom environment:
\beq
E = mc^2
\eeq

Custom align environment with nested matrix and \notag:
\ba
x &= \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix} \notag \\
z &= w \\
\begin{cases}
a &= b \nonumber \\
c &= d
\end{cases}
\ea

Regular equation with nested aligned:
\begin{equation}
\begin{aligned}
F &= ma \\
E &= mc^2
\end{aligned}
\end{equation}

\begin{subequations}
\begin{align}
A &= B \\
C &= D \notag \\
E &= F
\end{align}
\end{equation}
\end{subequations}

\end{document}
"""
def testcode():
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as f:
        f.write(test_content)
        test_file = f.name
    
    print("\nExtracting equations...")
    path = "/mnt/c/Users/alexa/Desktop/Mathhack/misc stuff/"
    equations = extract_equations_from_tex(path+"cuts.tex")
    # equations = extract_equations_from_tex(test_file)
    
    print("\nExtracted equations:")
    for eq in equations:
        if isinstance(eq, list):
            if eq[0] is not None:
                print(f"\nEquation ({eq[0]}):")
                print(f"  {eq[1]}")
            else:
                print(f"\nUnnumbered line:")
                print(f"  {eq[1]}")
                
def get_tex_eq(file_path, equation_number, sure=True):
    # Extract equations from the specified LaTeX file
    equations = extract_equations_from_tex(file_path)
    
    for i in range(len(equations)):
        
        if equations[i][0] == str(equation_number):
            tex_eq = equations[i][1:]
            
            if sure: print('\n', tex_eq, '\n')
            if sure == False:
                if i > 3: 
                    a = -3
                else:
                    a = 1-i
                while a<4 and i+a < len(equations):
                    print(equations[i+a])
                    a+=1
                
                equation_confirm = input("Confirm (y) or enter new number: ")
                
                if equation_confirm == 'y': 
                    print('\n', tex_eq, '\n')
                else:
                    for j in range(len(equations)):
                        if equations[j][0] == str(equation_confirm):
                            tex_eq = equations[j][1:]
                            print('\n', tex_eq, '\n')