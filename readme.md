# 📘 GLR Auto-Filler (Template-based, No Samples)

A Streamlit application that **automatically fills a GLR (General Loss Report)** by extracting information from uploaded PDF inspection reports.

No sample GLRs are needed — the app learns the narrative style directly from your uploaded template.

---

## 🚀 Features

### ✅ **Upload Your Own Template**

* Accepts **DOCX GLR templates** containing placeholders like:
  <pre class="overflow-visible!" data-start="551" data-end="603"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>[</span><span>INSURED_NAME</span><span>]
  [</span><span>LOSS_DATE</span><span>]
  [</span><span>ADDRESS</span><span>]
  </span></span></code></div></div></pre>
* Automatically detects all placeholders.

### ✅ **Extract Text From PDF Reports**

* Reads multiple PDF inspection reports using `pdfplumber`.
* Merges extracted text for LLM processing.

### ✅ **AI-Powered Field Extraction**

Uses **Google Gemini 2.5 Flash Lite** to:

* Map extracted PDF text → placeholder fields
* Follow the writing style of your uploaded template
* Output a **strict JSON mapping**
* Avoid hallucination (never invents info not found in the PDF)

### ✅ **Auto-Fill Final GLR**

* Replaces placeholders in the original template
* Generates a fully completed **DOCX GLR** for download

### ✅ **No Sample GLR Needed**

* The LLM uses the style extracted directly from your uploaded template.

---

## 🛠️ Tech Stack

| Component           | Technology        |
| ------------------- | ----------------- |
| UI                  | Streamlit         |
| PDF Parsing         | pdfplumber        |
| Template Processing | python-docx       |
| LLM                 | Google Gemini API |
| Language            | Python 3.9+       |

---

## 📦 Installation

### 1. Clone the Repository

<pre class="overflow-visible!" data-start="1590" data-end="1682"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>git </span><span>clone</span><span> https://github.com/yourusername/GLR-Auto-Filler.git
</span><span>cd</span><span> GLR-Auto-Filler
</span></span></code></div></div></pre>

### 2. Create a Virtual Environment (Recommended)

<pre class="overflow-visible!" data-start="1734" data-end="1845"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>python -m venv venv
</span><span>source</span><span> venv/bin/activate    </span><span># macOS/Linux</span><span>
venv\Scripts\activate       </span><span># Windows</span><span>
</span></span></code></div></div></pre>

### 3. Install Dependencies

<pre class="overflow-visible!" data-start="1875" data-end="1918"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>pip install -r requirements.txt
</span></span></code></div></div></pre>

---

## ▶️ Run the App

<pre class="overflow-visible!" data-start="1944" data-end="1976"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>streamlit run app.py
</span></span></code></div></div></pre>

The app will open automatically in your browser at:

<pre class="overflow-visible!" data-start="2030" data-end="2059"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>http:</span><span>//localhost:8501</span><span>
</span></span></code></div></div></pre>

---

## 🔐 Gemini API Key Setup

You must provide a valid  **Google Gemini API key** .

Get one here:

[https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

Enter it in the Streamlit UI when prompted.

---

## 📁 How It Works (Flow)

![https://miro.medium.com/v2/resize%3Afit%3A1400/0%2AutDXBCEk62y-2f10](https://miro.medium.com/v2/resize%3Afit%3A1400/0%2AutDXBCEk62y-2f10)

![https://www.researchgate.net/publication/378223942/figure/fig1/AS%3A11431281244290354%401715910984449/The-flowchart-of-extraction-approach-LLM-large-language-model-Q-A-question-and.ppm](https://www.researchgate.net/publication/378223942/figure/fig1/AS%3A11431281244290354%401715910984449/The-flowchart-of-extraction-approach-LLM-large-language-model-Q-A-question-and.ppm)

1. Upload GLR DOCX template
2. App extracts placeholders + template narrative style
3. Upload PDF inspection reports
4. PDF text is extracted using `pdfplumber`
5. Gemini LLM analyzes PDF text & fills all placeholders
6. Template is auto-filled
7. Final GLR DOCX is downloaded

---

## 📌 File Structure

<pre class="overflow-visible!" data-start="2641" data-end="2852"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>├── app.py                  </span><span># Streamlit application</span><span>
├── README.md               </span><span># Documentation</span><span>
├── requirements.txt        </span><span># Dependencies</span><span>
└── sample/                 </span><span># Optional: sample templates or PDFs</span><span>
</span></span></code></div></div></pre>

---

## ⚙️ Core Functions

### 🔹 `extract_placeholders(doc)`

Finds placeholders like `[FIELD_NAME]`.

### 🔹 `extract_pdf_text(file)`

Reads and extracts text from PDF files.

### 🔹 `call_gemini(...)`

Sends placeholders + PDF text + template style to Gemini and returns JSON mapping.

### 🔹 `fill_template(doc, mapping)`

Replaces placeholders in the DOCX template.

---

## 🧪 Example Output

<pre class="overflow-visible!" data-start="3249" data-end="3405"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-json"><span><span>{</span><span>
  </span><span>"INSURED_NAME"</span><span>:</span><span></span><span>"John Doe"</span><span>,</span><span>
  </span><span>"LOSS_DATE"</span><span>:</span><span></span><span>"02/14/2024"</span><span>,</span><span>
  </span><span>"ADDRESS"</span><span>:</span><span></span><span>"123 Street Name, City"</span><span>,</span><span>
  </span><span>"CAUSE_OF_LOSS"</span><span>:</span><span></span><span>"Tree fall during storm"</span><span>
</span><span>}</span><span>
</span></span></code></div></div></pre>

---

## ❗ Notes

* The app will **never invent data** — unknown fields return empty strings.
* Style consistency is guaranteed since the template's text is provided to the LLM.
* Works only with  **DOCX templates** , not PDFs.

---

## 🤝 Contributing

Pull requests are welcome!

For major changes, please open an issue first to discuss your proposals.
