# 🌿 Sustainability Score Checker

*A Case Study for Vrtta - Built by Shushanth*

This project was developed as part of an interview case study for **Vrtta**, a company focused on sustainability analytics. The goal was to build a working prototype of a **Sustainability Score Checker** — a web app that accepts product information, computes a score based on customizable weighting factors, and generates meaningful sustainability insights using AI.

The system evaluates environmental impact across multiple dimensions (carbon footprint, circularity, cost), and also includes dynamic visualizations and an AI-based suggestion engine powered by OpenAI GPT.

---

## ✅ Features

* **🌱 Sustainability Score Calculation**

  * Accepts product name, quantity, and environmental metrics (GWP, circularity, cost).
  * Uses user-defined weights to calculate a composite sustainability score.

* **🧠 AI-Generated Recommendations**

  * Integrates OpenAI GPT to provide actionable suggestions for improving product sustainability.

* **📊 Visual Analytics**

  * Real-time charts using Chart.js to visualize:

    * Rating summary
    * Sustainability issue distribution

* **🗃️ Product History**

  * Maintains a running log of products previously rated and their scores.

* **📦 Easy Deployment**

  * Hosted on [Render](https://render.com)
  * Clean, modern UI using HTML, CSS, and Bootstrap.

---

## 💻 Tech Stack

| Component        | Tech Used            |
| ---------------- | -------------------- |
| Backend          | Python (Flask)       |
| AI Engine        | OpenAI GPT-3.5 API   |
| Frontend         | HTML5, Bootstrap 5   |
| Visualization    | Chart.js, Matplotlib |
| Hosting          | Render.com           |
| Environment Mgmt | python-dotenv, Flask |

---

## 🚀 Getting Started (Run Locally)

Follow these instructions to set up and run the app locally on your machine.

### 1. **Clone the Repository**

```bash
git clone https://github.com/YOUR_USERNAME/sustainability-score-checker.git
cd sustainability-score-checker
```

---

### 2. **(Optional) Create a Virtual Environment**

```bash
python3 -m venv venv
source venv/bin/activate  # For macOS/Linux
# or
venv\Scripts\activate     # For Windows
```

---

### 3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

---

### 4. **Set Up API Keys**

Create a `.env` file in the root directory and paste your OpenAI API key:

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

You can obtain your API key from:
👉 [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)

---

### 5. **Run the Application**

```bash
python app.py
```

Visit your app locally at:
👉 [http://localhost:5000](http://localhost:5000)

---

## ⚙️ Score Calculation Logic

The score is calculated using a weighted sum of three sustainability metrics:

```
score = (weight_gwp * gwp_value)
      + (weight_circularity * circularity_value)
      + (weight_cost * cost_value)
```

* Each input is normalized to a scale of 0–100
* The final score is mapped to a rating:

  * **A** → 85–100
  * **B** → 70–84
  * **C** → 55–69
  * **D** → Below 55

---

## 📈 Charts & Graphs

* **Rating Summary Bar Chart:** Shows how many products received each rating (A–D)
* **Top Sustainability Issues (Pie Chart):** Aggregates most common issues from GPT suggestions
* **Product History:** Keeps a log of all products analyzed in the session

---

## 🌐 Deploying to Render (Optional)

To deploy this app for free:

1. Push the code to a GitHub repo
2. Go to [https://render.com](https://render.com)
3. Click “New +” → **Web Service**
4. Connect your GitHub repo
5. Set Build and Start commands:

   * **Build command**: `pip install -r requirements.txt`
   * **Start command**: `gunicorn app:app`
6. Add your environment variable:

   * `OPENAI_API_KEY = your_key_here`

Render will automatically build and deploy the app!

---

## 📄 Example Use Case

**Product**: Recycled Paper Bag
**Inputs**:

* GWP: 30
* Circularity: 80
* Cost Score: 60
* Weights: All set to 0.4

**Output**:

* Score: 81
* Rating: B
* GPT Suggestions:

  * Promote multi-use of the bag
  * Source recycled paper locally
  * Explore alternate eco-friendly packaging materials

---

## 🙋‍♂️ Author

**Shushanth**
📧 Email: [shushanth03@gmail.com](mailto:shushanth03@gmail.com)
🔗 LinkedIn: [[linkedin.com/in/yourname](https://www.linkedin.com/in/shushanth-prem-anand-6a784b25b/)]([https://linkedin.com/in/yourname](https://www.linkedin.com/in/shushanth-prem-anand-6a784b25b/))

---

## 📃 License

This project is licensed under the [MIT License](LICENSE).

---

## 📌 Future Improvements

* Store history persistently in SQLite or Firebase
* Add product category auto-tagging
* Add carbon savings calculator
* Mobile-first responsive layout

---

## ✨ Live App

👉 [https://sustainability-score-clean.onrender.com](https://sustainability-score-clean.onrender.com)

