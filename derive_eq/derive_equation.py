from derive_eq.functions.get_tex_eq import *
from derive_eq.functions.get_tex_file import *
from derive_eq.functions.ask_chat import *

def derive_equation(arxiv_id, eq_number):
    eq_number = int(eq_number)
    current_dir = os.getcwd()
    tex_file_path = get_tex_file_path(arxiv_id, download_dir=current_dir)
    equation = get_tex_eq(tex_file_path, eq_number)
    derivation = bot(equation)
    # print(answer)


    # print(equation)
    # print(tex_file_path)
    
    # Delete the folder and file where the tex file is located
    if os.path.exists(tex_file_path):
        os.remove(tex_file_path)
        folder_path = os.path.dirname(tex_file_path)
        if os.path.isdir(folder_path):
            os.rmdir(folder_path)
    
    # print('it worked')

    return derivation
    

    
