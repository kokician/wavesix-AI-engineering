from jinja2 import Template

TEMPLATE = Template("""
You are a helpful assistant.
Context:
{{ context }}

Question:
{{ question }}

Answer:
""")

def format_prompt(context: str, question: str) -> str:
    return TEMPLATE.render(context=context, question=question)