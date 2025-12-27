---

# 📄 Dynamic PDF Template Generation System

**(Streamlit + MongoDB + PDF | app1 & app2 )**

---

## 📌 Project Overview

This project implements a **Dynamic PDF Template Generation System** using **Streamlit**, **MongoDB**, and **ReportLab**.

The application allows users to:

* Create reusable PDF templates
* Dynamically map JSON data from MongoDB
* Apply fallback default values
* Control text alignment (Left / Center / Right)
* Generate professional, realistic PDFs
* Preview PDFs in three formats:

  * **App :** Dynamic PDF Template System (Streamlit Cloud Version)
  * **App 1:** Professional document layout
  * **App 2:** Table-based layout

This project strictly follows the assignment requirements.

---

## 🎯 Assignment Objectives Covered

| Requirement                         | Status |
| ----------------------------------- | ------ |
| Dynamic template creation           | ✅      |
| Header / Body / Footer              | ✅      |
| Key + Mapping Field + Default Value | ✅      |
| JSON path mapping                   | ✅      |
| Alignment support                   | ✅      |
| PDF preview & generation            | ✅      |
| Salary template user dropdown       | ✅      |
| Bill template without input         | ✅      |
| MongoDB database integration        | ✅      |
| Clean UI & realistic PDF            | ✅      |

---

## 🧱 Project Structure

```
dynamic_pdf_template/
│
├── app.py        # Dynamic PDF Template System (Streamlit Cloud Version)
├── app1.py        # Professional PDF layout
├── app2.py        # Table-based PDF layout
├── mongodb.py             # MongoDB connection & queries
├── templates.json         # Salary & Bill templates
├── requirements.txt
└── README.md
```

---

## 🗄️ Database: MongoDB

### Collections Used

#### 1️⃣ `users`

Used for **Salary Template**

```json
{
  "_id": "U001",
  "name": "Prerna Gyanchandani",
  "payDetail": {
    "basic_salary": 50000,
    "hra": 10000,
    "total_salary_amount": 60000
  }
}
```

---

#### 2️⃣ `bills`

Used for **Bill Template**

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

### Salary Template (requires user selection)

* Header: Company Name, Salary Slip Title
* Body: Employee Name, Basic Salary, HRA, Total Salary
* Footer: Authorized Signature

### Bill Template (no input required)

* Header: Store Name, Bill Title
* Body: Customer Name, Product, Quantity, Price
* Footer: Total Amount, Thank You Message

Each field includes:

* **Key** (PDF label)
* **Mapping Field** (MongoDB JSON path)
* **Default Value**
* **Alignment**

---

## 🖥️ Application Screens

### 1️⃣ Template Preview Screen

* Lists available templates:

  * Salary Template
  * Bill Template

### 2️⃣ PDF Generation Screen

* **Salary Template**

  * Dropdown to select a user from MongoDB
* **Bill Template**

  * No input required
* Button to generate PDF
* PDF rendered directly in browser

---

## 📄 PDF Output Styles

---

### 1️⃣ App 1 — Professional Document Layout

**Characteristics**

* Bold template title
* Section separators
* Realistic spacing
* Clean corporate look
* Ideal for salary slips & invoices

**File:** `app1.py`

---

### 2️⃣ App 2 — Table-Based Layout

**Characteristics**

* Key–Value table format
* Neat column alignment
* Easy readability
* Accounting-style layout

**File:** `app2.py`

---

## ⚙️ Installation & Setup

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ MongoDB Setup

Use **MongoDB Atlas** or local MongoDB.

Set Streamlit secrets:

```toml
# .streamlit/secrets.toml
MONGO_URI = "mongodb+srv://<username>:<password>@cluster.mongodb.net/"
DB_NAME = "pdf_templates"
```

---

### 3️⃣ Run Application

#### App 1 (Professional PDF & Dynamic PDF Template System (Streamlit Cloud Version))

```bash
streamlit run app1.py
rstreamlit run app.py
```

#### App 2 (Table PDF)

```bash
streamlit run app2.py
```
#### Mongodb PDF 

```bash
streamlit run main.py
```

## ☁️ Streamlit Cloud Deployment

1. Push code to GitHub
2. Create new Streamlit app
3. Select:

   * `app1.py` OR `app2.py`
4. Add MongoDB secrets in **Streamlit Cloud → Settings → Secrets**
5. Deploy 🚀

---

## 🧪 Sample Test Flow

### Salary Template

1. Select "Salary Template"
2. Choose user from dropdown
3. Generate PDF
4. Salary slip rendered with mapped values

### Bill Template

1. Select "Bill Template"
2. Click Generate
3. Bill PDF rendered directly

---

## 🧠 Technologies Used

* **Streamlit** – UI
* **MongoDB** – Database
* **ReportLab** – PDF generation
* **Python** – Backend logic

---

## ✅ Evaluation Readiness

This project demonstrates:

* Dynamic UI-driven templates
* Real database mapping
* Alignment-aware PDF generation
* Clean architecture
* Production-ready Streamlit app

---
