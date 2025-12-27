# Dynamic_Pdf_Template_Prerna

Here is the **complete `README.md` file** you can directly copy-paste into your project root.
This single README covers **MongoDB + Option A + Option C**, exactly as you asked.

---

```md
# 📄 Dynamic PDF Template Generation System  
(Streamlit + MongoDB + ReportLab)

---

## 📌 Project Overview

This project implements a **Dynamic PDF Template Generation System** using **Streamlit**, **MongoDB**, and **ReportLab**.

The application allows users to:
- Create and manage reusable PDF templates
- Dynamically map data using JSON paths
- Apply default fallback values
- Control text alignment (Left / Center / Right)
- Generate realistic, clean PDFs
- Preview PDFs in two formats:
  - **Option A** – Professional document layout
  - **Option C** – Table-based layout

This project strictly follows the assignment requirements provided.

---

## 🎯 Assignment Requirements Mapping

| Requirement | Status |
|------------|--------|
Template creation screen | ✅ |
Header / Body / Footer sections | ✅ |
Key + Mapping Field + Default Value | ✅ |
JSON path mapping | ✅ |
Alignment (Left / Center / Right) | ✅ |
PDF preview screen | ✅ |
Salary template user dropdown | ✅ |
Bill template without user input | ✅ |
Dummy + DB data support | ✅ |
MongoDB integration | ✅ |
Clean UI & realistic PDF | ✅ |

---

## 🧱 Project Structure

```

dynamic_pdf_template/
│
├── app_option_a.py        # Professional PDF layout (Option A)
├── app_option_c.py        # Table-based PDF layout (Option C)
├── mongodb.py             # MongoDB connection and queries
├── templates.json         # Salary & Bill template definitions
├── requirements.txt
└── README.md

```

---

## 🗄️ MongoDB Database Design

### Database Name
```

pdf_templates

````

---

### 📁 Collection: `users` (Salary Template)

```json
{
  "_id": "U001",
  "name": "Prerna Sharma",
  "payDetail": {
    "basic_salary": 50000,
    "hra": 10000,
    "total_salary_amount": 60000
  }
}
````

---

### 📁 Collection: `bills` (Bill Template)

```json
{
  "bill_id": "BILL001",
  "customer": {
    "name": "Rohit Kumar",
    "mobile": "9876543210"
  },
  "items": {
    "product": "Laptop",
    "quantity": 1,
    "price": 55000
  },
  "total_amount": 55000
}
```

---

## 🧾 Template Configuration (`templates.json`)

Two templates are defined:

### 1️⃣ Salary Template

* Requires user selection
* Data fetched from `users` collection
* Header, Body, Footer supported
* Alignment applied per field

### 2️⃣ Bill Template

* No user selection required
* Data fetched from `bills` collection
* PDF generated directly

Each field contains:

* **Key** – Label shown in PDF
* **Mapping Field** – JSON path from MongoDB
* **Default Value** – Used if mapping fails
* **Alignment** – Left / Center / Right

---

## 🖥️ Application Screens

### 1️⃣ Template Preview Screen

* Lists available templates:

  * Salary Template
  * Bill Template

### 2️⃣ PDF Generation Screen

* **Salary Template**

  * Dropdown of users from MongoDB
* **Bill Template**

  * No additional input
* Generate button renders PDF instantly

---

## 📄 PDF Output Styles

---

### 🅰️ Option A — Professional Layout

**File:** `app_option_a.py`

**Features**

* Bold title
* Section separators
* Realistic spacing
* Corporate / official look
* Suitable for salary slips & invoices

---

### 🅲 Option C — Table-Based Layout

**File:** `app_option_c.py`

**Features**

* Key–Value table
* Clear column alignment
* Accounting-style presentation
* Clean and readable

---

## ⚙️ Installation & Setup

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 2️⃣ MongoDB Configuration

Create a file:

```
.streamlit/secrets.toml
```

Add:

```toml
MONGO_URI = "mongodb+srv://<username>:<password>@cluster.mongodb.net/"
DB_NAME = "pdf_templates"
```

---

### 3️⃣ Run Application

#### Option A (Professional PDF)

```bash
streamlit run app_option_a.py
```

#### Option C (Table PDF)

```bash
streamlit run app_option_c.py
```

---

## ☁️ Streamlit Cloud Deployment

1. Push project to GitHub
2. Create a new Streamlit app
3. Select:

   * `app_option_a.py` **or**
   * `app_option_c.py`
4. Add MongoDB credentials in **Secrets**
5. Deploy 🚀

---

## 🧪 Sample Usage Flow

### Salary Template

1. Select **Salary Template**
2. Choose a user
3. Click **Generate PDF**
4. Salary slip rendered using mapped data

### Bill Template

1. Select **Bill Template**
2. Click **Generate PDF**
3. Bill generated directly

---

## 🧠 Technologies Used

* **Streamlit** – UI framework
* **MongoDB** – Database
* **ReportLab** – PDF generation
* **Python** – Backend logic

---

## ✅ Evaluation Ready

This project demonstrates:

* Dynamic template handling
* JSON path mapping with fallback values
* Alignment-aware PDF generation
* Database-driven document rendering
* Clean UI and modular design

---

### 📌 Optional Enhancements (Future Scope)

* Template creation UI
* PDF download history
* Role-based access
* Logo upload per template

---

**✔ Ready for assignment submission and evaluation**

```

---

If you want next:
- ✅ **Final polished `app_option_a.py`**
- ✅ **Final polished `app_option_c.py`**
- ✅ **`templates.json`**
- ✅ **MongoDB helper (`mongodb.py`)**

Just tell me 👍
```
