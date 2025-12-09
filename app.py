import streamlit as st
import json
import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

TEMPLATE_FILE = "templates.json"

# --------------------------
# Utility Functions
# --------------------------

def load_templates():
    if os.path.exists(TEMPLATE_FILE):
        with open(TEMPLATE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_templates(data):
    with open(TEMPLATE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def resolve_json_path(data, path):
    """Fetch value from JSON using path like a → b → c"""
    try:
        parts = [p.strip() for p in path.split("→")]
        for p in parts:
            data = data[p]
        return data
    except:
        return None

def alignment_to_enum(align):
    return {"Left": TA_LEFT, "Center": TA_CENTER, "Right": TA_RIGHT}[align]

def generate_pdf(template, user_json=None):
    filename = "generated_output.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()

    for section in ["Header", "Body", "Footer"]:
        story.append(Paragraph(f"<b>{section}</b>", styles["Heading3"]))
        for item in template[section]:
            key = item["key"]
            path = item["map"]
            default = item["default"]
            align = item["align"]

            val = resolve_json_path(user_json or {}, path)
            if val is None:
                val = default

            style = ParagraphStyle(
                name="custom",
                alignment=alignment_to_enum(align),
                fontSize=12
            )
            story.append(Paragraph(f"{key}: {val}", style))
            story.append(Spacer(1, 6))

    doc.build(story)
    return filename

# --------------------------
# Streamlit UI
# --------------------------

st.title("📄 Dynamic PDF Template System")

menu = st.sidebar.selectbox("Menu", ["Create Template", "Preview & Generate PDF"])
templates = load_templates()

# ------------------------------------------------------
# SCREEN 1 — TEMPLATE CREATION
# ------------------------------------------------------
if menu == "Create Template":
    st.header("Create a New PDF Template")

    template_name = st.text_input("Template Name")

    if template_name:

        st.subheader("Header Fields")
        header = st.session_state.get("header", [])
        if st.button("Add Header Field"):
            header.append({"key": "", "map": "", "default": "", "align": "Left"})
        st.session_state["header"] = header

        for i, f in enumerate(header):
            st.write(f"### Field {i+1}")
            f["key"] = st.text_input(f"Header Key {i}", f["key"])
            f["map"] = st.text_input(f"Header Mapping {i}", f["map"])
            f["default"] = st.text_input(f"Header Default {i}", f["default"])
            f["align"] = st.selectbox(f"Header Alignment {i}", ["Left", "Center", "Right"], index=["Left", "Center", "Right"].index(f["align"]))

        st.subheader("Body Fields")
        body = st.session_state.get("body", [])
        if st.button("Add Body Field"):
            body.append({"key": "", "map": "", "default": "", "align": "Left"})
        st.session_state["body"] = body

        for i, f in enumerate(body):
            st.write(f"### Field {i+1}")
            f["key"] = st.text_input(f"Body Key {i}", f["key"])
            f["map"] = st.text_input(f"Body Mapping {i}", f["map"])
            f["default"] = st.text_input(f"Body Default {i}", f["default"])
            f["align"] = st.selectbox(f"Body Alignment {i}", ["Left", "Center", "Right"], index=["Left", "Center", "Right"].index(f["align"]))

        st.subheader("Footer Fields")
        footer = st.session_state.get("footer", [])
        if st.button("Add Footer Field"):
            footer.append({"key": "", "map": "", "default": "", "align": "Left"})
        st.session_state["footer"] = footer

        for i, f in enumerate(footer):
            st.write(f"### Field {i+1}")
            f["key"] = st.text_input(f"Footer Key {i}", f["key"])
            f["map"] = st.text_input(f"Footer Mapping {i}", f["map"])
            f["default"] = st.text_input(f"Footer Default {i}", f["default"])
            f["align"] = st.selectbox(f"Footer Alignment {i}", ["Left", "Center", "Right"], index=["Left", "Center", "Right"].index(f["align"]))

        if st.button("Save Template"):
            templates[template_name] = {
                "Header": header,
                "Body": body,
                "Footer": footer
            }
            save_templates(templates)
            st.success("Template Saved Successfully!")

# ------------------------------------------------------
# SCREEN 2 — PDF GENERATION
# ------------------------------------------------------
if menu == "Preview & Generate PDF":
    st.header("Generate PDF from Template")

    if not templates:
        st.warning("No templates found. Please create one first.")
    else:
        template_name = st.selectbox("Select Template", list(templates.keys()))
        template = templates[template_name]

        dummy_user_data = {
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

        if "salary" in template_name.lower():
            st.subheader("Select User")
            user_list = ["Amit Sharma", "Ravi Kumar", "Priya Nair"]
            selected_user = st.selectbox("User", user_list)

            # For demo, same dummy JSON for all users
            user_json = dummy_user_data

        if st.button("Generate PDF"):
            file = generate_pdf(template, user_json)
            st.success("PDF Generated Successfully!")
            with open(file, "rb") as f:
                st.download_button("Download PDF", f, file_name="output.pdf")

