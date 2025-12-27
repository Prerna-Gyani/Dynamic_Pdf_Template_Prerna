import streamlit as st
from pymongo import MongoClient
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4

# --------------------------------
# MongoDB Connection
# --------------------------------
@st.cache_resource
def get_db():
    client = MongoClient(st.secrets["MONGO_URI"])
    return client["pdf_app"]

db = get_db()
template_col = db["templates"]
user_col = db["users"]
bill_col = db["bills"]

# --------------------------------
# Utility Functions
# --------------------------------
def resolve_json_path(data, path):
    try:
        for p in path.split("→"):
            data = data[p.strip()]
        return data
    except:
        return None

def align_enum(a):
    return {"Left": TA_LEFT, "Center": TA_CENTER, "Right": TA_RIGHT}[a]

def load_templates():
    return list(template_col.find({}, {"_id": 0}))

# --------------------------------
# PDF Generator (Professional)
# --------------------------------
def generate_pdf(template, data):
    file_name = "generated_output.pdf"
    doc = SimpleDocTemplate(file_name, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle(
        "title",
        alignment=TA_CENTER,
        fontSize=18,
        spaceAfter=20
    )

    story.append(Paragraph(f"<b>{template['name']}</b>", title_style))

    for section in ["Header", "Body", "Footer"]:
        story.append(Paragraph(
            f"<b>-------------------- {section.upper()} --------------------</b>",
            styles["Heading4"]
        ))
        story.append(Spacer(1, 10))

        for f in template[section]:
            value = resolve_json_path(data, f["map"])
            if value is None:
                value = f["default"]

            pstyle = ParagraphStyle(
                "field",
                alignment=align_enum(f["align"]),
                fontSize=12
            )

            story.append(Paragraph(f"<b>{f['key']}</b>: {value}", pstyle))
            story.append(Spacer(1, 6))

        story.append(Spacer(1, 12))

    doc.build(story)
    return file_name

# --------------------------------
# Streamlit UI
# --------------------------------
st.title("📄 Dynamic PDF Template System (MongoDB)")

menu = st.sidebar.radio("Menu", ["Create Template", "Preview & Generate PDF"])

# --------------------------------
# Create Template Screen
# --------------------------------
if menu == "Create Template":
    st.header("Create PDF Template")

    template_name = st.text_input("Template Name (e.g., Salary Template / Bill Template)")
    template_type = st.selectbox("Template Type", ["salary", "bill"])

    if template_name:
        for section in ["Header", "Body", "Footer"]:
            st.subheader(section)
            key = f"{section}_fields"
            st.session_state.setdefault(key, [])

            if st.button(f"Add {section} Field"):
                st.session_state[key].append(
                    {"key": "", "map": "", "default": "", "align": "Left"}
                )

            for i, f in enumerate(st.session_state[key]):
                f["key"] = st.text_input(f"{section} Key {i}", f["key"])
                f["map"] = st.text_input(f"{section} Mapping {i}", f["map"])
                f["default"] = st.text_input(f"{section} Default {i}", f["default"])
                f["align"] = st.selectbox(
                    f"{section} Alignment {i}",
                    ["Left", "Center", "Right"],
                    index=["Left", "Center", "Right"].index(f["align"])
                )

        if st.button("Save Template"):
            template_col.update_one(
                {"name": template_name},
                {"$set": {
                    "name": template_name,
                    "type": template_type,
                    "Header": st.session_state["Header_fields"],
                    "Body": st.session_state["Body_fields"],
                    "Footer": st.session_state["Footer_fields"]
                }},
                upsert=True
            )
            st.success("Template saved to MongoDB")

# --------------------------------
# PDF Preview & Generate Screen
# --------------------------------
if menu == "Preview & Generate PDF":
    st.header("Generate PDF")

    templates = load_templates()

    if not templates:
        st.warning("No templates found.")
    else:
        tname = st.selectbox(
            "Select Template",
            [t["name"] for t in templates]
        )
        template = next(t for t in templates if t["name"] == tname)

        data = {}

        # Salary Template → User Dropdown
        if template["type"] == "salary":
            users = list(user_col.find({}, {"_id": 0}))
            if not users:
                st.error("No users in database")
            else:
                uname = st.selectbox("Select User", [u["name"] for u in users])
                data = next(u for u in users if u["name"] == uname)

        # Bill Template → Direct
        if template["type"] == "bill":
            bill = bill_col.find_one({}, {"_id": 0})
            if not bill:
                st.error("No bill data found")
            else:
                data = bill

        if st.button("Generate PDF"):
            pdf = generate_pdf(template, data)
            with open(pdf, "rb") as f:
                st.download_button("Download PDF", f, file_name="output.pdf")

# --------------------------------
# Sample Data Inserter (Run Once)
# --------------------------------
st.sidebar.markdown("---")
if st.sidebar.button("Insert Sample MongoDB Data"):
    user_col.delete_many({})
    bill_col.delete_many({})

    user_col.insert_many([
        {
            "name": "Amit Sharma",
            "company": {"name": "ABC Pvt Ltd"},
            "payDetail": {
                "total_salary_amount": "75,000 INR",
                "hra": "10,000 INR"
            }
        },
        {
            "name": "Ravi Kumar",
            "company": {"name": "XYZ Ltd"},
            "payDetail": {
                "total_salary_amount": "65,000 INR",
                "hra": "8,000 INR"
            }
        }
    ])

    bill_col.insert_one({
        "store": {"name": "Fresh Mart – Indiranagar"},
        "number": "BILL-67329",
        "customer": {"name": "Rohit Kumar"},
        "amount": {
            "total_items": "3 items",
            "tax": "₹18",
            "grand_total": "₹418"
        },
        "payment": {"method": "UPI"},
        "thankyou": "Visit Again!"
    })

    st.sidebar.success("Sample data inserted")
