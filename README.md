🌾 ##Fertilizer Recommendation System (Punjab)##
** working link ** - 

** Overview **

This project is a crop-specific fertilizer recommendation system for Wheat and Rice cultivation in Punjab.

It predicts nutrient requirement levels (Nitrogen, Phosphorus, Potassium) based on basic field information and converts them into fertilizer quantity ranges (kg per acre and total kg).

The system is built as an applied machine learning project using agronomic rules and a Random Forest model.

** Problem **

Many farmers do not have access to soil testing facilities.
This system provides an advisory recommendation based on:

Crop type (Wheat / Rice)

Growth stage (days since sowing/transplanting)

Soil type

Previous N, P, K application

Time since last fertilizer

Irrigation information

Field area

Method

Crop-specific datasets were generated using agronomic logic.

A multi-output Random Forest model was trained to predict:

N requirement class (Low / Medium / High)

P requirement class

K requirement class

Predicted classes are converted into fertilizer quantity ranges (kg/acre).

Tech Stack

Python

Pandas

Scikit-learn

Streamlit

** Notes ** 

This is a decision-support tool.

Dataset is rule-generated.

Not a replacement for laboratory soil testing.
