# Base-AI


# Text Translation Application

## Team Members
- Nikola Mitrović, SV18/2021
- Bojan Živanić, SV61/2021

## Problem Definition
The goal of this project is to develop a text translation application that uses artificial intelligence techniques. The problem being solved is to facilitate communication among people who speak different languages, allowing them to quickly and efficiently translate text into the desired language.

## Motivation
Language barriers can pose challenges in many situations, including travel, business meetings, education, and international cooperation. Developing a translation application can ease communication among people of different linguistic backgrounds, contributing to better understanding and collaboration.

## Dataset
The dataset used for training and evaluating our text translation application can be found on GitHub at the following link: [https://github.com/kockarevicivan/vocabulary-dataset/tree/master](#). This dataset contains a total of 158,685 instances.

### Attributes
- **Source Text:** the text in the source language that needs to be translated
- **Target Text:** the reference translation of the source text into the target language

### Key Attributes
- **Source Text:** a key attribute as it is the basis for generating the translation into the target language
- **Target Text:** represents the target label as the model needs to learn to generate the corresponding translation into the target language

## Data Preprocessing
Data preprocessing will include:
- Tokenization of text
- Removal of unnecessary symbols and stop words
- Text normalization
- Techniques such as lemmatization or stemming for text standardization

## Methodology
### Steps:
1. **Data Preparation:** Loading and preprocessing the dataset.
2. **Model Building:** Implementing a translation model using deep learning techniques such as recurrent neural networks (RNN) or transformer models.
3. **Model Training:** Training the model on the prepared data.
4. **Model Evaluation:** Evaluating model performance using relevant metrics such as BLEU score or METEOR score.

## Evaluation
The evaluation will be performed using metrics such as BLEU score or METEOR score, which assess the quality of translations compared to reference translations.

## Technologies
For implementing the application, we will use:
- **Python** as the main programming language
- **TensorFlow** or **PyTorch** for implementing deep learning models
- **Flask** for backend development
- **Python GUI** for frontend development
- **NLTK** or **spaCy** for natural language processing

## Installation
1. **Clone the repository:**
   ```sh
   git clone https://github.com/trami25/bases-ai.git
   cd translation_app
