<p align="center">
    <a href="https://www.python.org/doc/" alt="Python 3.9">
        <img src="https://img.shields.io/badge/python-v3.7+-blue.svg" />
    </a>
    <a href="https://github.com/EDJINEDJA/NER/blob/main/LICENSE" alt="Licence">
        <img src="https://img.shields.io/badge/license-MIT-yellow.svg" />
    </a>
    <a href="https://github.com/EDJINEDJA/NER/commits/main" alt="Commits">
        <img src="https://img.shields.io/github/last-commit/EDJINEDJA/NER/master" />
    </a>
    <a href="https://github.com/EDJINEDJA/NER" alt="Activity">
        <img src="https://img.shields.io/badge/contributions-welcome-orange.svg" />
    </a>
</p>

## Table of Contents

<!--ts-->
* [Aims and Objectives](#Aims-and-Objectives)
* [Features](#Features)
* [Neuro-symbolic Approach](#Anonymization-Software)
* [NER Model Fine-tuning Approach](#NER-Model-camemBERT)
* [LLM Approach](#LLM-Approach)
<!--te-->

# Aims and Objectives
This folder contains anonymization methodes for cup with de-identification of PHI(Protected Health Information) informations in free text data problem.

# Features

We present three approaches:

- **Neuro-symbolic approach**
- **NER model (camemBERT) fine-tuning approach**
- **LLM (Large Language Model) approach**

## Neuro-symbolic Approach

The **Neuro-symbolic Approach** combines symbolic and neural artificial intelligence methods to tackle complex problems. In this context, it is used to anonymize sensitive data, such as personal health information. This hybrid approach integrates explicit logical rules with machine learning models, enabling it to ensure data confidentiality while effectively analyzing complex and diverse information.

## NER model (camemBERT) Fine-tuning Approach

In this approach, we fine-tune the camemBERT model, a French language model, to recognize and anonymize specific Named Entities (NE) such as patient names, location, organization and other health-related terms. By training the model on a labeled dataset, we enhance its ability to accurately identify and mask PHI in text, ensuring robust data privacy.

## LLM Approach

The LLM approach uses zero-shot learning to process and anonymize data. With this method, the system can perform the anonymization task on various types of text without requiring domain-specific training.