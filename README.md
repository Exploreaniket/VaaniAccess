# 🎙️ VaaniAccess

### Dialect-Adaptive Public Scheme Voice Navigator

**Hackathon Problem Statement:** CC-GFG-06 — VaaniAccess

VaaniAccess is a voice-first public scheme navigator that helps users discover potentially relevant government schemes using natural language.

Users can speak or type their situation in **Hindi, English, or Hinglish**. The system extracts important profile information such as occupation, education, income level, age, and location, then uses a rule-based eligibility engine to identify and rank potentially relevant schemes.

---

## 🚨 Problem

Many people struggle to discover government schemes because:

- Scheme information can be difficult to understand.
- Government portals often require users to know the scheme name beforehand.
- Users may be more comfortable communicating in Hindi or their local language.
- Literacy and bureaucratic language can create barriers.
- A generic chatbot may generate an answer without providing explainable eligibility matching.

VaaniAccess addresses this problem through a simple **voice-first scheme discovery experience**.

---

## 💡 Solution

VaaniAccess allows a user to simply describe their situation.

For example:

> "Main college student hoon aur meri family ki income bahut kam hai."

The system:

1. Converts voice into text.
2. Understands the user's situation.
3. Extracts a structured user profile.
4. Compares the profile with scheme eligibility rules.
5. Calculates a match score.
6. Ranks potentially suitable schemes.
7. Explains why a scheme matches.
8. Shows required documents and suggested steps.
9. Provides an official source for verification.
10. Can read the recommendation aloud in Hindi.

---

## ✨ Features

### 🎙️ Voice-First Interaction

Users can describe their situation using Hindi or Hinglish voice input.

### ⌨️ Text Fallback

Users can type their situation when voice input is unavailable.

### 🧠 AI Profile Extraction

Gemini helps convert natural-language descriptions into structured information.

Example:

```text
"Main college student hoon aur meri income bahut kam hai."