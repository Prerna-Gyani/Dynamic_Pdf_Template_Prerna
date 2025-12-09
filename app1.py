import streamlit as st
import json
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import A4

TEMPLATE_FILE = "templates.json"

# ---------------------------
# SAFE JSON METHODS
# ---------------------------
def load_templates():
    if os.path.exists(TEMPLATE_FILE):
        try:
            with open(TEMPLATE_FILE, "r") as f:
                content = f.read().strip()
                if content == "":
                    return {}
                return json.loads(content)
        except:
            save_templates({})
            return {}
    return {}

def save_templates(data):
    with open(TEMPLATE_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------------------------
# JSON MAPPING
# ---------------------------
def resolve_json_path(data, path):
    try:
        parts = [p.strip() for p in path.split("→")]
        for p in parts:
            data = data[p]
        return data
    except:
        return None

def alignment_to_enum(al):
    return {"Left": TA_LEFT, "Center": TA_CENTER, "Right": TA_RIGHT}[al]

# ---------------------------
# PDF: PROFESSIONAL LAYOUT
# ---------------------------
def generate_pdf(template, user_json=None):
    file = "generated_output.pdf"
    doc = SimpleDocTemplate(file, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    header_style = ParagraphStyle("header", alignment=TA_CENTER, fontSize=18, spaceAfter=15, leading=22)

    story.append(Paragraph(f"<b>{template['name']}</b>", header_style))
    story.append(Spacer(1, 10))

    for section in ["Header", "Body", "Footer"]:
        story.append(Paragraph(f"<b>---------------------<br/>{section.upper()} SECTION<br/>---------------------</b>",
                               styles["Heading4"]))
        story.append(Spacer(1, 8))

        for item in template[section]:
            key, path, default, align = item["key"], item["map"], item["default"], item["align"]
            value = resolve_json_path(user_json or {}, path) or default

            pstyle = ParagraphStyle("val", alignment=alignment_to_enum(align), fontSize=12)
            story.append(Paragraph(f"<b>{key}</b>: {value}", pstyle))
            story.append(Spacer(1, 4))

        story.append(Spacer(1, 8))

    doc.build(story)
    return file

# ---------------------------
# STREAMLIT UI
# ---------------------------
st.title("📄 Dynamic PDF Template System – Option A (Professional Format)")
menu = st.sidebar.radio("Menu", ["Create Template", "Preview & Generate PDF"])
templates = load_templates()

# ---------------------------
# TEMPLATE CREATION
# ---------------------------
if menu == "Create Template":
    st.header("Create Template")
    name = st.text_input("Template Name")

    if name:
        st.subheader("Header Fields")
        if st.button("Add Header Field"):
            st.session_state.setdefault("hdr", []).append({"key":"", "map":"", "default":"", "align":"Left"})
        for i, f in enumerate(st.session_state.get("hdr", [])):
            f["key"] = st.text_input(f"Header Key {i}", f["key"])
            f["map"] = st.text_input(f"Header Mapping {i}", f["map"])
            f["default"] = st.text_input(f"Header Default {i}", f["default"])
            f["align"] = st.selectbox(f"Header Align {i}", ["Left","Center","Right"], index=["Left","Center","Right"].index(f["align"]))

        st.subheader("Body Fields")
        if st.button("Add Body Field"):
            st.session_state.setdefault("bdy", []).append({"key":"", "map":"", "default":"", "align":"Left"})
        for i, f in enumerate(st.session_state.get("bdy", [])):
            f["key"] = st.text_input(f"Body Key {i}", f["key"])
            f["map"] = st.text_input(f"Body Mapping {i}", f["map"])
            f["default"] = st.text_input(f"Body Default {i}", f["default"])
            f["align"] = st.selectbox(f"Body Align {i}", ["Left","Center","Right"], index=["Left","Center","Right"].index(f["align"]))

        st.subheader("Footer Fields")
        if st.button("Add Footer Field"):
            st.session_state.setdefault("ftr", []).append({"key":"", "map":"", "default":"", "align":"Left"})
        for i, f in enumerate(st.session_state.get("ftr", [])):
            f["key"] = st.text_input(f"Footer Key {i}", f["key"])
            f["map"] = st.text_input(f"Footer Mapping {i}", f["map"])
            f["default"] = st.text_input(f"Footer Default {i}", f["default"])
            f["align"] = st.selectbox(f"Footer Align {i}", ["Left","Center","Right"], index=["Left","Center","Right"].index(f["align"]))

        if st.button("Save Template"):
            templates[name] = {
                "name": name,
                "Header": st.session_state.get("hdr", []),
                "Body": st.session_state.get("bdy", []),
                "Footer": st.session_state.get("ftr", [])
            }
            save_templates(templates)
            st.success("Template saved!")

# ---------------------------
# GENERATE PDF
# ---------------------------
if menu == "Preview & Generate PDF":
    st.header("Generate PDF")

    if not templates:
        st.warning("No templates found.")
    else:
        tname = st.selectbox("Select Template", list(templates.keys()))
        template = templates[tname]

        dummy = {
            "user": {
                "name": "Amit Sharma",
                "company": {"name": "ABC Pvt Ltd"},
                "payDetail": {"total_salary_amount": "75,000", "hra": "10,000"}
            },
            "bill": {"bill_no": "INV-9001", "amount": "12,000 INR", "date": "01-12-2025"}
        }

        user_json = dummy

        if "salary" in tname.lower():
            user = st.selectbox("Select User", ["Amit Sharma", "Ravi Kumar", "Priya"])
            user_json = dummy

        if st.button("Generate PDF"):
            file = generate_pdf(template, user_json)
            with open(file, "rb") as f:
                st.download_button("Download PDF", f, file_name="professional.pdf")
