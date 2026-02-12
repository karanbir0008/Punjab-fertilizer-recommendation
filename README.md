# 🌾 Punjab Fertilizer Recommendation System

**working link** - 

## 📌 Overview

This project is a **crop-specific fertilizer recommendation system** designed for **Wheat and Rice cultivation in Punjab**.

The system predicts nutrient requirement levels — **Nitrogen (N), Phosphorus (P), and Potassium (K)** — based on field conditions and converts them into **fertilizer quantity ranges (kg per acre and total kg for the field)**.

It is built as an **applied machine learning project** that combines agronomic rules with a Random Forest model and an interactive Streamlit interface.

---

## 🎯 Problem Statement

Many farmers do not have access to laboratory soil testing facilities. As a result, fertilizer usage is often imbalanced.

This system provides a **decision-support recommendation** based on:

- **Crop type** (Wheat / Rice)
- **Days since sowing / transplanting**
- **Growth stage**
- **Soil type**
- **Previous N, P, K application levels**
- **Time since last fertilizer application**
- **Irrigation history**
- **Field area (acres)**

---

## 🧠 Methodology

### 1️⃣ Dataset Design

- Separate datasets were generated for **Wheat** and **Rice** using agronomic logic based on Punjab cultivation practices.
- Nutrient requirement levels were categorized as:
  - **Low**
  - **Medium**
  - **High**

### 2️⃣ Machine Learning Model

- Model Used: **Random Forest (Multi-Output Classification)**
- Target Variables:
  - `N_class`
  - `P_class`
  - `K_class`

The model predicts nutrient requirement classes based on input field features.

### 3️⃣ Output Conversion

Predicted nutrient classes are converted into:

- **kg per acre**
- **Total kg required for the entire field**

This keeps the ML model simple and interpretable while applying agronomic ranges for quantity estimation.

---

## 💻 Tech Stack

- **Python**
- **Pandas**
- **Scikit-learn**
- **Streamlit**
- **Joblib**

---

## 📂 Project Structure

