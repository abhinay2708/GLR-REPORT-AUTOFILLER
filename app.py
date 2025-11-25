import streamlit as st
import io
import json
import pdfplumber
import google.generativeai as genai
from docx import Document
import re


# ---------------------------------------------------------
# PDF TEXT EXTRACTION
# ---------------------------------------------------------
def extract_pdf_text(file):
    pdf_bytes = file.read()
    try:
        txt = ""
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for p in pdf.pages:
                t = p.extract_text()
                if t:
                    txt += t + "\n\n"
        return txt.strip()
    except:
        return ""


def extract_all_pdf_texts(pdf_files):
    out = {}
    for i, pdf in enumerate(pdf_files):
        name = pdf.name if hasattr(pdf, "name") else f"report_{i}.pdf"
        out[name] = extract_pdf_text(pdf)
    return out


# ---------------------------------------------------------
# TEMPLATE PLACEHOLDER EXTRACTION
# ---------------------------------------------------------
def extract_placeholders(doc):
    """Detect placeholders like [FIELD_NAME]"""
    ph = set()
    pattern = re.compile(r"\[([A-Za-z0-9_]+)\]")
    for para in doc.paragraphs:
        for m in pattern.findall(para.text):
            ph.add(m)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for m in pattern.findall(cell.text):
                    ph.add(m)
    return list(ph)


# ---------------------------------------------------------
# EXTRACT TEMPLATE STYLE (OPTION A)
# ---------------------------------------------------------
def extract_template_style(doc):
    """
    Convert the template paragraphs + tables into plain text.
    This becomes the 'style guide' for Option A.
    """
    parts = []
    for p in doc.paragraphs:
        if p.text.strip():
            parts.append(p.text.strip())

    for table in doc.tables:
        for row in table.rows:
            row_text = " | ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
            if row_text:
                parts.append(row_text)

    return "\n".join(parts)


# ---------------------------------------------------------
# CALL GEMINI (NO SAMPLES, STRICT JSON)
# ---------------------------------------------------------
def call_gemini(placeholders, pdf_texts, template_style, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash-lite")

    prompt = f"""
You are an expert GLR (General Loss Report) generator.

You are given:
1. A list of placeholder fields extracted from a GLR template.
2. Extracted inspection report text from PDF files.
3. The template's narrative paragraphs (THIS IS THE STYLE TO FOLLOW).

Your job:
- Extract the correct value for each placeholder.
- Follow the writing style and tone from the template paragraphs.
- Return ONLY a JSON object mapping placeholder → extracted value.
- If a value cannot be found, return an empty string.
- NEVER invent random addresses or fields. Only use information from the PDF text.
- Keep values concise (e.g., dates: MM/DD/YYYY).

PLACEHOLDERS:
{json.dumps(placeholders)}

PDF TEXT:
{json.dumps(pdf_texts)}

GLR TEMPLATE STYLE EXCERPT:
{template_style}

Now output ONLY a valid JSON dictionary.
"""

    response = model.generate_content(prompt)
    text = response.text

    # Extract JSON
    try:
        return json.loads(text)
    except:
        s = text.find("{")
        e = text.rfind("}")
        try:
            return json.loads(text[s:e+1])
        except:
            return {p: "" for p in placeholders}


# ---------------------------------------------------------
# FILL TEMPLATE
# ---------------------------------------------------------
def fill_template(doc, mapping):
    new_doc = Document()

    def repl(t):
        for k, v in mapping.items():
            t = t.replace(f"[{k}]", str(v))
        return t

    # paragraphs
    for p in doc.paragraphs:
        new_doc.add_paragraph(repl(p.text))

    # tables
    for table in doc.tables:
        cols = len(table.rows[0].cells) if table.rows else 1
        new_table = new_doc.add_table(rows=0, cols=cols)
        for row in table.rows:
            new_row = new_table.add_row()
            for i, cell in enumerate(row.cells):
                new_row.cells[i].text = repl(cell.text)

    return new_doc


# ---------------------------------------------------------
# STREAMLIT UI
# ---------------------------------------------------------
st.set_page_config(page_title="GLR Auto Filler (No Samples)", layout="wide")
st.title("📘 GLR Auto-Filler (Template-based, No Samples)")

st.markdown("""
### Upload:
- **GLR Template (.docx)** – with placeholders like `[INSURED_NAME]`
- **PDF inspection reports**
- **Gemini API Key**

The app will:
✔ Extract placeholder fields  
✔ Extract PDF text  
✔ Infer values using Gemini  
✔ Follow the narrative style of YOUR uploaded template  
✔ Produce a fully completed GLR  
""")


template_file = st.file_uploader("Upload GLR Template (.docx)", type=["docx"])
pdf_files = st.file_uploader("Upload PDF Reports", type=["pdf"], accept_multiple_files=True)
api_key = st.text_input("Gemini API Key", type="password")

if st.button("Generate Completed GLR"):
    if not template_file:
        st.error("Please upload a GLR template DOCX.")
        st.stop()
    if not pdf_files:
        st.error("Please upload one or more PDF reports.")
        st.stop()
    if not api_key:
        st.error("Please enter your Gemini API key.")
        st.stop()

    # Load template
    template_bytes = template_file.read()
    template_doc = Document(io.BytesIO(template_bytes))

    # Extract placeholders
    placeholders = extract_placeholders(template_doc)
    st.success(f"Detected {len(placeholders)} placeholders.")
    st.json(placeholders)

    # Extract template style (Option A)
    template_style = extract_template_style(template_doc)
    st.info("Extracted narrative style from template.")

    # Extract PDF text
    with st.spinner("Extracting PDF text..."):
        pdf_texts = extract_all_pdf_texts(pdf_files)

    # Call Gemini
    with st.spinner("Asking Gemini to extract field values..."):
        mapping = call_gemini(placeholders, pdf_texts, template_style, api_key)

    st.success("LLM extracted field values:")
    st.json(mapping)

    # Fill template
    final_doc = fill_template(template_doc, mapping)
    out = io.BytesIO()
    final_doc.save(out)
    out.seek(0)

    st.download_button(
        "Download Completed GLR",
        data=out,
        file_name="Completed_GLR.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    st.success("GLR successfully generated!")
