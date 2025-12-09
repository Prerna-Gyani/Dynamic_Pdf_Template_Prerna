import streamlit as st
import json
import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

TEMPLATE_FILE = "templates.json"

# -------------------------------------
# JSON Utility Functions
# -------------------------------------

def load_templates():
    """Safely load templates.json without crashing"""
    if os.path.exists(TEMPLATE_FILE):
        try:
            with open(TEMPLATE_FILE, "r") as f:
                content = f.read().strip()
                if content == "" or content is None:
                    return {}
                return json.loads(content)
        except:
            # auto-reset corrupted file
            save_templates({})
            return {}
    return {}

def save_templates(data):
    with open(TEMPLATE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def resolve_json_path(data, path):
    """Fetch value from JSON using path like: user → payDetail → total_salary_amount"""
    try:
        parts = [p.strip() for p in path.split("→")]
        for p in parts:
            data = data[p]
        return data
    except:
        return None

def alignment_to_enum(align):
    return {"Left": TA_LEFT, "Center": TA_CENTER, "Right": TA_RIGHT}[align]

# -------------------------------------
# PDF GENERATION
# -------------------------------------

def generate_pdf(template, user_json=None):
    filename = "generated_output.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()

    for section in ["Header", "Body", "Footer"]:
        story.append(Paragraph(f"<b>{section}</b>", styles["Heading3"]))

        for item in template.get(section, []):
            key = item["key"]
            path = item["map"]
            default = item["default"]
            align = item["align"]

            value = resolve_json_path(user_json or {}, path)
            if value is None:
                value = default

            style = ParagraphStyle(
                name="custom_align",
                alignment=alignment_to_enum(align),
                fontSize=12
            )

            story.append(Paragraph(f"{key}: {value}", style))
            story.append(Spacer(1, 6))

    doc.build(story)
    return filename

# -------------------------------------
# STREAMlit UI
# -------------------------------------

st.title("📄 Dynamic PDF Template System (Streamlit Cloud Version)")

menu = st.sidebar.selectbox("Menu", ["Create Template", "Preview & Generate PDF"])
templates = load_templates()

# -------------------------------------
# 1. TEMPLATE CREATION SCREEN
# -------------------------------------

if menu == "Create Template":
    st.header("Create New Template")

    template_name = st.text_input("Template Name")

    if template_name:

        # --- Header Section ---
        st.subheader("Header Fields")
        header = st.session_state.get("header", [])

        if st.button("Add Header Field"):
            header.append({"key": "", "map": "", "default": "", "align": "Left"})

        st.session_state["header"] = header

        for i, f in enumerate(header):
            st.write(f"### Header Field {i+1}")
            f["key"] = st.text_input(f"Header Key {i}", f["key"])
            f["map"] = st.text_input(f"Header Mapping {i}", f["map"])
            f["default"] = st.text_input(f"Header Default {i}", f["default"])
            f["align"] = st.selectbox(f"Header Align {i}", ["Left", "Center", "Right"], index=["Left", "Center", "Right"].index(f["align"]))

        # --- Body Section ---
        st.subheader("Body Fields")
        body = st.session_state.get("body", [])

        if st.button("Add Body Field"):
            body.append({"key": "", "map": "", "default": "", "align": "Left"})

        st.session_state["body"] = body

        for i, f in enumerate(body):
            st.write(f"### Body Field {i+1}")
            f["key"] = st.text_input(f"Body Key {i}", f["key"])
            f["map"] = st.text_input(f"Body Mapping {i}", f["map"])
            f["default"] = st.text_input(f"Body Default {i}", f["default"])
            f["align"] = st.selectbox(f"Body Align {i}", ["Left", "Center", "Right"], index=["Left", "Center", "Right"].index(f["align"]))

        # --- Footer Section ---
        st.subheader("Footer Fields")
        footer = st.session_state.get("footer", [])

        if st.button("Add Footer Field"):
            footer.append({"key": "", "map": "", "default": "", "align": "Left"})

        st.session_state["footer"] = footer

        for i, f in enumerate(footer):
            st.write(f"### Footer Field {i+1}")
            f["key"] = st.text_input(f"Footer Key {i}", f["key"])
            f["map"] = st.text_input(f"Footer Mapping {i}", f["map"])
            f["default"] = st.text_input(f"Footer Default {i}", f["default"])
            f["align"] = st.selectbox(f"Footer Align {i}", ["Left", "Center", "Right"], index=["Left", "Center", "Right"].index(f["align"]))

        # Save Template Button
        if st.button("Save Template"):
            templates[template_name] = {
                "Header": header,
                "Body": body,
                "Footer": footer
            }
            save_templates(templates)
            st.success("Template saved successfully!")

# -------------------------------------
# 2. PDF PREVIEW / GENERATION SCREEN
# -------------------------------------

if menu == "Preview & Generate PDF":
    st.header("Generate PDF")

    if not templates:
        st.warning("No templates found. Please create one first.")
    else:
        template_name = st.selectbox("Select Template", list(templates.keys()))
        template = templates[template_name]

        # Dummy Data
        dummy_data = {
            "user": {
                "name": "Amit Sharma",
                "payDetail": {
                    "total_salary_amount": "75,000 INR",
                    "hra": "10,000 INR"
                }
            },
            "bill": {
                "bill_no": "BILL-2025-009",
                "amount": "12,500 INR"
            }
        }

        user_json = None

        # Salary Template check
        if "salary" in template_name.lower():
            st.subheader("Select User")
            users = ["Amit Sharma", "Ravi Kumar", "Priya Nair"]
            selected = st.selectbox("User", users)
            user_json = dummy_data  # same for demo

        if st.button("Generate PDF"):
            file = generate_pdf(template, user_json)
            st.success("PDF Generated!")

            with open(file, "rb") as f:
                st.download_button("Download PDF", f, file_name="output.pdf")
