import re

def extract_equations_from_tex(file_path):
    """Extract equations from a LaTeX file."""
    equations = []
    labels = []
    try:
        with open(file_path, 'r', encoding='utf8', errors='ignore') as file:
            content = file.read()
            # regexp = re.compile("begin{document}(.*)$")
            # m = re.search(r'(?<=\\begin{document})(.*)', content)
            # print(m.group(1))
            
            # Find all equations enclosed in \begin{equation} ... \end{equation}
            # print(content)
            unlabeled = re.sub(r'\\label{(.*?)}', '', content)
            content = unlabeled.replace('\label{}', '') 
            
            equations = re.findall(r'\\begin{equation}(.*?)\\end{equation}', content, re.DOTALL)
    except Exception as e:
        print(f"Error reading file: {e}")
    
    return equations

# def find_nearest_equation(equations, search_str):
#     """Find the nearest equation based on the search string."""
#     nearest_equation = None
#     min_distance = float(20)

#     for equation in equations:
#         # Calculate the distance between the search string and the current equation
#         distance = len(set(search_str) - set(equation))
#         if distance < min_distance:
#             min_distance = distance
#             nearest_equation = equation
    
#     return nearest_equation

def get_tex_eq(file_path, equation_number, sure=True):
    # Input LaTeX file path
    # tex_file_path = input("Enter the path to the LaTeX file: ")
    
    # Extract equations from the specified LaTeX file
    equations = extract_equations_from_tex(file_path)
    
    # equation_input = int(input("Enter the equation number: "))
    # print(i+1, equations[i])
    
    # # Get the search string from the user
    # search_input = input("Enter a string to search for the nearest equation: ")
    # # Find the nearest equation
    # nearest_eq = find_nearest_equation(equations, search_input)
    # # Output the result
    # if nearest_eq:
    #     print("Nearest equation found:")
    #     print(nearest_eq.strip())
    # else:
    #     print("No equations found.")
    
    if sure == False and equation_number>=3:
            print(equation_number-2, equations[equation_number-3])
            print(equation_number-1, equations[equation_number-2])
            print(equation_number, equations[equation_number-1])
            print(equation_number+1, equations[equation_number])
            print(equation_number+2, equations[equation_number+1])
            
            equation_confirm = input("Confirm (y) or enter new number: ")
            
            if equation_confirm == 'y': 
                return equations[equation_number-1]
            else:
                return equations[int(equation_confirm)-1]
    else:
        return equations[equation_number-1]

        

print(get_tex_eq('lagrangian.tex',8))    

