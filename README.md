<p align="center">
    <a href="https://github.com/EDJINEDJA/NER">
        <img src="https://github.com/EDJINEDJA/NER/blob/main/hands.png" alt="anonymizationSoftware">
    </a> 
<br>


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
* [Anonymization Software](#Anonymization-Software)
* [Usage](#Usage)
* [Inference](#Inference)
* [NER Model (camemBERT)](#NER-Model-camemBERT)
* [LLM Approach](#LLM-Approach)
<!--te-->

# Aims and Objectives
This folder contains anonymization methodes for cup with de-identification of PHI(Protected Health Information) informations in free text data problem.

# Features

We present three approaches:

- **Neuro-symbolic approach**
- **NER model (camemBERT) fine-tuning approach**
- **LLM (Large Language Model) approach** which leverages zero-shot learning.

## Neuro-symbolic Approach

In the context of the SIA-REMU project, funded thanks to FEDER and Swiss Federal Interreg subventions, this software was developed to address the challenge of how to ensure the privacy of patients when using their data.

The tool implements an optimal algorithm capable of guaranteeing confidentiality while processing sensitive data.

## Usage

#### Installation

- **Clone the repository**

Clone this repository into the main folder of your project to use the Anonymization Software.

```bash
$ git clone https://github.com/EDJINEDJA/NER
```
- requirements

The toolkit support Python 3.10.6 

To install required packages use:

```bash
$ pip3 install -r requirements.txt
```

####  Usage

```python
$ python Processing.py 
 
```
### Inference

For test this software you are Processing adated to take a text file on docx doc pdf formats and return text

change you text file link and run  this code 

```python
$ python Processing.py 
 
```
BatchProcessing is adapted to infer the algorithme on several text
Just fil give a text folders to the algorithme and run the following scrypte
```python
$ python BatchProcessing.py 
```
## NER model (camemBERT) Fine-tuning Approach
In this approach, we fine-tune the camemBERT model, a French language model, to recognize and anonymize specific Named Entities (NE) such as patient names, location, organization and other health-related terms. By training the model on a labeled dataset, we enhance its ability to accurately identify and mask PHI in text, ensuring robust data privacy.

## LLM Approach

The LLM approach uses zero-shot learning to process and anonymize data. With this method, the system can perform the anonymization task on various types of text without requiring domain-specific training.