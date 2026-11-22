# 🌟 AI-Vision — Standout Features

These three features take AI-Vision beyond a standard mini-project into research-grade territory. Each one has a defensible academic foundation and a visible UI contribution.

---

## 1. Grad-CAM Explainability (Explainable AI)

### What it does
After classifying a waste image, the model produces a **heatmap overlay** showing exactly which pixels of the input image contributed most to the prediction. Red/yellow regions = high attention from the CNN; blue regions = low attention.

### Academic foundation
Implementation follows **Selvaraju et al., "Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization", IEEE International Conference on Computer Vision (ICCV) 2017** — one of the most-cited papers in explainable AI with 25,000+ citations.

### How it works (technical)
1. Forward pass: image flows through EfficientNetB0; we capture the activations of the last convolutional layer (`top_conv`).
2. Backward pass: we compute gradients of the predicted class score with respect to those activations.
3. Channel weighting: gradients are global-average-pooled per channel — channels that respond more strongly to the target class get higher weights.
4. Heatmap: we multiply weights by activations, ReLU, normalize to [0, 1], upsample to 224×224, apply the JET colormap, and overlay on the original image at 45% opacity.

### Why it matters
- **Trust**: farmers and examiners can SEE that the model is looking at the actual waste material, not the background or random noise.
- **Debugging**: when the model misclassifies, the heatmap reveals if it was distracted by an irrelevant object.
- **Research-grade**: explainable AI (XAI) is an active research area; very few undergraduate mini-projects implement Grad-CAM properly.

### Defensible viva answer
> "We use Grad-CAM, a class-discriminative localization technique from Selvaraju et al. ICCV 2017. It computes gradients of the predicted class with respect to the final convolutional layer's activations, then uses those gradients to weight the activation maps. The result is a heatmap showing which image regions drove the prediction — providing explainability rather than treating the CNN as a black box."

### Code location
- `ai/predict.py` — functions: `find_last_conv_layer`, `make_gradcam_heatmap`, `overlay_heatmap_on_image`
- Frontend: `index.html` (panel id `xaiPanel`), `app.js` (renders `r.heatmap`), `style.css` (`.xai-block`)

---

## 2. Confidence-Aware Top-K Predictions

### What it does
Beyond the single top prediction, the UI shows the **top 3 candidates with confidence bars**. When the top confidence is below 80%, a yellow warning banner appears: *"The model is not fully confident. Please review the top candidates."*

### Why it matters
- **No silent failures**: many ML systems give one confident-looking answer even when the model is uncertain. AI-Vision exposes this honestly.
- **User correction**: the farmer can see if the second candidate looks more correct from the image context.
- **Better calibration**: showing confidence distributions encourages users to act differently for 95%-confidence vs 60%-confidence predictions.

### How it works
The `predict.py` script returns the full softmax probability vector, sorted descending, top 3 with their confidence percentages. The frontend renders them as horizontal bars: the winner gets a gold gradient, the others get blue.

### Defensible viva answer
> "Standard classifiers report only the argmax, hiding the model's full belief distribution. We instead return the top-3 candidates with their softmax confidences. When the top confidence falls below 80%, we surface a warning to the user. This pattern — confidence-aware UX — comes from research on AI decision support, where overconfident predictions cause more harm than 'I'm not sure' admissions."

### Code location
- `ai/predict.py` — returns `topK` array
- Frontend: `index.html` (panel id `topkPanel`), `app.js` (renders `r.topK`), `style.css` (`.topk-*`)

---

## 3. Real Generative AI Recommendations (Groq + Llama 3.3 70B)

### What it does
After classification, recycling recommendations are **generated live by Llama 3.3 70B** via the Groq API. Each set of recommendations is:
- Tailored to the detected waste type AND the estimated quantity (small lots get on-farm advice; larger lots get sale routes with mandi pricing).
- Localized in the user's chosen language (English, Hindi, Telugu).
- Different on every call (temperature 0.6) — no two responses are identical.
- Required to contain concrete numbers (₹/kg prices, day counts, ratios, percentages).

### Why it matters
- Truly fulfills the "Generative AI" promise on Slide 7 of the PPT.
- Recommendations are contextual, not from a static lookup table.
- The fallback (curated ICAR/KVK best practices) ensures the demo works even without an API key — graceful degradation.

### Setup
1. Get a free key at https://console.groq.com/keys (Google sign-in, no payment)
2. Copy `backend/.env.example` to `backend/.env`
3. Paste your key into the `GROQ_API_KEY=` line
4. Restart `npm start` — recommendations are now AI-generated

### Defensible viva answer
> "The recommendation engine has two paths: when a Groq API key is configured, we send the waste type, estimated quantity, and language to Llama 3.3 70B with a carefully engineered prompt that requires 4 specific recommendations covering on-farm method, sale route with pricing, scheme angle, and an actionable tip — each containing concrete numbers. When the API key is not set, we fall back to a curated knowledge base derived from ICAR and KVK best practices. This dual-path design ensures the system always works while leveraging real generative AI when available."

### Code location
- `backend/services/groq.js` — `generateRecommendations()` and `advisorReply()`
- `backend/routes/analyze.js` — wires Groq call with fallback
- `backend/.env.example` — setup instructions

---

## How these three features work TOGETHER

A complete classification call now produces:

1. **The prediction** (e.g., "Organic Waste, 100%")
2. **The Grad-CAM heatmap** — "the model looked at the watermelon and vegetable matter"
3. **The Top-K bars** — "the model was 100% sure; second guess was Plastic Mulch at 0%"
4. **AI-generated recommendations** — "Vermicompost the 79 kg with 5 kg red wigglers — sell at ₹4-5/kg in 30 days. Apply for GOBAR-Dhan subsidy. Note: organic peels above 20% citric load slow composting — neutralize with wood ash."

This is no longer a black-box classifier; it's an explainable, calibrated, generative AI system.

---

## Three-sentence summary for the lecturer

> "AI-Vision combines three modern AI techniques in one platform. Grad-CAM explainability (Selvaraju 2017) shows which image regions the CNN attended to, so farmers and examiners can verify the model's reasoning. Confidence-aware top-K prediction surfaces the model's full belief distribution and warns when confidence is low, avoiding overconfident misclassifications. Real Llama 3.3 70B recommendations via Groq deliver context-aware, multilingual, quantity-scaled recycling advice that goes beyond static lookup tables."
