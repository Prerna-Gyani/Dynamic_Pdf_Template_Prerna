import streamlit as st
import json
import os
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

TEMPLATE_FILE = "templates.json"

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

def resolve_json_path(data, path):
    try:
        for part in [p.strip() for p in path.split("→")]:
            data = data[part]
        return data
    except:
        return None

def generate_pdf(template, user_json=None):
    file = "generated_table.pdf"
    doc = SimpleDocTemplate(file, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()

    story.append(Paragraph(f"<b>{template['name']}</b>", styles["Heading1"]))
    story.append(Spacer(1, 10))

    for section in ["Header", "Body", "Footer"]:
        story.append(Paragraph(f"<b>{section}</b>", styles["Heading3"]))
        story.append(Spacer(1, 6))

        table_data = [["Key", "Value"]]

        for item in template[section]:
            value = resolve_json_path(user_json or {}, item["map"]) or item["default"]
            table_data.append([item["key"], str(value)])

        t = Table(table_data, colWidths=[200, 250])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.grey),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("GRID", (0,0), (-1,-1), 1, colors.black),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("BACKGROUND", (0,1), (-1,-1), colors.whitesmoke),
            ("ALIGN", (0,0), (-1,-1), "LEFT"),
        ]))

        story.append(t)
        story.append(Spacer(1, 14))

    doc.build(story)
    return file

# UI
st.title("📄 Dynamic PDF Template – Table Layout")
menu = st.sidebar.radio("Menu", ["Create Template", "Preview & Generate PDF"])
templates = load_templates()

if menu == "Create Template":
    st.header("Create Template")
    name = st.text_input("Template Name")

    if name:
        if st.button("Add Header Field"):
            st.session_state.setdefault("h", []).append({"key":"","map":"","default":""})

        for i, f in enumerate(st.session_state.get("h", [])):
            f["key"] = st.text_input(f"Header Key {i}", f["key"])
            f["map"] = st.text_input(f"Header Mapping {i}", f["map"])
            f["default"] = st.text_input(f"Header Default {i}", f["default"])

        if st.button("Add Body Field"):
            st.session_state.setdefault("b", []).append({"key":"","map":"","default":""})

        for i, f in enumerate(st.session_state.get("b", [])):
            f["key"] = st.text_input(f"Body Key {i}", f["key"])
            f["map"] = st.text_input(f"Body Mapping {i}", f["map"])
            f["default"] = st.text_input(f"Body Default {i}", f["default"])

        if st.button("Add Footer Field"):
            st.session_state.setdefault("f", []).append({"key":"","map":"","default":""})

        for i, f in enumerate(st.session_state.get("f", [])):
            f["key"] = st.text_input(f"Footer Key {i}", f["key"])
            f["map"] = st.text_input(f"Footer Mapping {i}", f["map"])
            f["default"] = st.text_input(f"Footer Default {i}", f["default"])

        if st.button("Save Template"):
            templates[name] = {
                "name": name,
                "Header": st.session_state.get("h", []),
                "Body": st.session_state.get("b", []),
                "Footer": st.session_state.get("f", [])
            }
            save_templates(templates)
            st.success("Saved!")

if menu == "Preview & Generate PDF":
    st.header("Generate PDF")

    if templates:
        tname = st.selectbox("Select Template", list(templates.keys()))
        template = templates[tname]

        dummy = {
            "user": {"name":"Amit","payDetail":{"total_salary_amount":"80,000"}},
            "bill": {"bill_no":"BILL-1002","amount":"15,000 INR","date":"01-01-2025"}
        }

        user_json = dummy

        if "salary" in tname.lower():
            user = st.selectbox("User", ["Amit","Ravi","Priya"])
            user_json = dummy

        if st.button("Generate PDF"):
            file = generate_pdf(template, user_json)
            with open(file, "rb") as f:
                st.download_button("Download PDF", f, file_name="table_format.pdf")

