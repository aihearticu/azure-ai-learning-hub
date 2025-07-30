# Lab 06: Translate Text

This folder contains the work completed for the Microsoft Learn module: [Translate text](https://microsoftlearning.github.io/mslearn-ai-language/Instructions/Labs/06-translate-text.html)

## Overview
Build a Python application that translates text between languages using Azure AI Translator service.

## Lab Components
- Azure AI Translator resource setup
- Language detection and listing
- Text translation between multiple languages
- Interactive translation application

## Technologies Used
- Azure AI Translator Service
- Python/Azure SDK
- azure-ai-translation-text package

## Key Features
- List all supported languages
- Detect source language automatically
- Translate text to user-selected target language
- Interactive console application

## Setup Requirements
- Azure subscription
- Azure AI Translator resource (F0 free tier available)
- Python 3.x with virtual environment

## Lab Completion Status
✅ **Completed**: 2025-07-28

### Key Accomplishments
1. Created Azure Translator resource in East US region
2. Configured Python environment with azure-ai-translation-text SDK
3. Built interactive translation application
4. Successfully tested translation between multiple languages

### Implementation Details
- **Resource Name**: translatorcuratest
- **Region**: East US
- **SDK Version**: azure-ai-translation-text==1.0.1
- **Supported Languages**: 137 languages available for translation

### Application Features Implemented
- Dynamic language selection from supported languages list
- Automatic source language detection
- Interactive translation loop
- Proper error handling and user feedback

### Sample Usage
```
Enter a target language code: es
Enter text to translate: Hello world
'Hello world' was translated from en to es as 'Hola mundo'
```