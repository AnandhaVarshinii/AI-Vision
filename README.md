# 🌾 AI-Vision: Sustainable Agricultural Waste Management System

> Turning Agricultural Waste into Wealth Through AI.

A hardware-free, multilingual web platform that classifies farm waste from a smartphone photo, explains its reasoning, recommends recycling pathways via generative AI, and connects farmers to buyers and recycling facilities.

---

## 🏆 What makes this project stand out

Most undergraduate mini-projects stop at a CNN classifier. AI-Vision goes three steps further:

| Feature | What it does | Defensible foundation |
|---|---|---|
| 🔍 **Grad-CAM Explainability** | Shows a heatmap of WHERE the CNN looked to make its decision | Selvaraju et al., ICCV 2017 (25,000+ citations) |
| 📊 **Confidence-Aware Top-K** | Reveals model's full belief distribution; warns when uncertain | Calibrated ML / Trustworthy AI literature |
| 🤖 **Real Generative AI Recommendations** | Llama 3.3 70B via Groq generates contextual advice per image | Live LLM integration, not lookup tables |

See **STANDOUT_FEATURES.md** for technical details and viva answers.

---

## 📊 Model Performance

- **Architecture**: EfficientNetB0 with transfer learning (ImageNet-pretrained)
- **Training**: Two-phase, 20 epochs frozen + 6 epochs fine-tune on Google Colab T4 GPU
- **Validation accuracy**: **90.97%** (131/144 correct on held-out validation set)
- **Macro F1**: 0.83 | **Weighted F1**: 0.91
- **Best classes**: Organic Waste (F1 0.94), Plastic Mulch (F1 0.94)
- **Five categories**: Rice Straw, Wheat Husk, Sugarcane Bagasse, Organic Waste, Plastic Mulch

---

## 🚀 Quick Start

```bash
# 1. Backend
cd backend
npm install
cp .env.example .env
# (Optional) Add your Groq API key in .env for real AI recommendations

# 2. Python ML environment (one-time)
cd ../ai
pip install -r requirements.txt

# 3. Run
cd ../backend
npm start
# Open http://localhost:3000
```

That's it. No external database, no Docker, no Kubernetes.

---

## 🎯 Five Product Modules

| Module | What it does | Live data |
|---|---|---|
| **Classify** | Upload image → get prediction + heatmap + top-K bars + AI recommendations | ✅ Real CNN |
| **Marketplace** | List, search, filter, delete waste-for-sale entries | ✅ LocalStorage |
| **Impact** | Real-time KPIs: tonnes managed, CO₂ saved, farmer revenue, burning prevented | ✅ Computed live |
| **Advisor** | Chat with an agricultural AI advisor about composting, schemes, biogas | ✅ Groq Llama 3.3 |
| **Routes** | Interactive Leaflet map showing real recycling facilities within 15 km | ✅ OpenStreetMap |

---

## 🌐 Multilingual

Every UI label, classification result, and AI recommendation is available in:
- 🇬🇧 English (en)
- 🇮🇳 Hindi (hi)
- 🇮🇳 Telugu (te)

Switching language mid-session automatically re-fetches the prediction so the entire screen translates together.

---

## 🌱 SDG Alignment

SDG 2 (Zero Hunger) · SDG 8 (Decent Work & Growth) · SDG 9 (Industry & Innovation) · SDG 11 (Sustainable Communities) · SDG 12 (Responsible Consumption) · SDG 13 (Climate Action)

---

## 👥 Team

**Stanley College of Engineering & Technology for Women, Hyderabad**
B.Tech CSE — VI Semester — Section A — Academic Year 2025-2026

| Roll No | Name |
|---|---|
| 160623733008 | Bingi Sindhu |
| 160623733012 | Ch. Lohitha |
| 160623733041 | N. Suhavani |
| 160623733051 | R. Anandha Varshini |

**Project Guide:** Ms. M. Swathisree, Assistant Professor, Dept. of CSE
