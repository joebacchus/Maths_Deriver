from openai import OpenAI
# import markdown2

def bot(tex_eq):
    client = OpenAI(
        api_key=""
)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are a mathematics expert and you are good at providing simple derivations of equations. The user will provide you with an equation in LaTeX and you need to provide the derivation"},
            {
                "role": "user",
                "content": f"Provide me with the derivation of this equation {tex_eq}."
            }
        ]
    )

    return completion.choices[0].message.content



# def format_to_markdown(response):
#     # Basic Markdown formatting rules
#     response = response.replace("\n", "\n\n")  # Markdown reads double newlines as paragraphs
#     response = re.sub(r'(\d+\.\s)', r'\n\1', response)  # Numbered lists
#     response = re.sub(r'(\*\s)', r'\n\1', response)  # Bulleted lists
    
#     # Convert Markdown to HTML for rendering (optional)
#     html_response = markdown2.markdown(response)
#     return html_response



# completion = client.chat.completions.create(
#     model="gpt-3.5-turbo-0125",
#     messages=[
#         {"role": "system", "content": "You are a mathematics expert and you are good at providing simple derivations of equations. The user will provide you with an equation in LaTeX and you need to provide the derivation"},
#         {
#             "role": "user",
#             "content": f"Provide me with the derivation of this equation {tex_eq}."
#         }
#     ]
# )

# print(completion.choices[0].message)