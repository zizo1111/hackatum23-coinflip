# Hackathon Loganalysis Tum 2023 11

Welcome to the "Hackathon Loganalysis Tum 2023 11" repository. This project is part of a broader initiative to develop log analysis tools, as part of a competition hosted by Rohde & Schwarz.
 
## Motivation:

In today's data-driven world, handling and understanding large log files is a significant challenge. This hackathon aims to leverage transformer models to simplify this process. The goal is to create a solution that can summarize these log files and provide a user-friendly QA system to interact with the summarized data.
Furthermore, by linking the answers back to the original log lines, we aim to maintain data credibility and provide a verification method. This hackathon is an opportunity to contribute to a solution that can revolutionize how organizations interact with their log data, leading to more efficient data handling and informed decision-making.

## Virtual Machine for Hackathon Teams
To support all hackathon teams, we will provide a Virtual Machine (VM) that is enabled with a GPU. This VM will also have the capability to broadcast a frontend application, such as Streamlit, which will allow teams to present their results effectively. This setup will ensure that all teams have the necessary computational resources and presentation tools to excel in the hackathon.
 
## Task Description:
In this hackathon challenge, your task is to develop a two-step solution using transformer models for handling large log files.

### Step 1: Summarization of Log Files
Your first task is to create a transformer model that can effectively summarize large log files. The model should be able to parse through the log files, understand the context, and generate a concise summary of the logs. The goal is to distill the essential information from the logs into a format that is easily understandable and manageable.

### Step 2: QA with Summarized Context
Once the summarization is done, your next task is to use another transformer model to perform a QA (Question-Answering) task with the summarized context. The user should be able to ask questions related to the log files, and the transformer model should provide accurate answers based on the summary created in the first step.

### Additional Requirement: Traceability of Answers
An additional requirement for this challenge is to maintain the traceability of the answers given by the QA transformer. This means that for every answer provided by the transformer, there should be a way to link it back to the original log lines used for the summarization. This will help in ensuring the credibility of the answers and provide a way for users to verify the information if required.
The solution should be efficient, scalable, and robust, capable of handling log files of varying sizes and complexity.

### Measurement of Success:
As a part of the hackathon, you are also required to devise a method to measure the success of your solution. This could be based on the accuracy of the summarization, the relevance of the answers provided by the QA transformer, and the effectiveness of the traceability feature.

## Streamlit as possible frontend

Inside the "streamlit" folder, you will find Python code snippets to help you develop a frontend for your hackathon project with Streamlit. Streamlit is a powerful tool that allows you to turn data scripts into shareable web apps in just a few minutes.

## Tutorial to NLP and Log files

Inside the ‘tutorial’ folder, you will find some snippets and explanations related to the hackathon and NLP tools that might be useful. These tutorials are designed to help you understand the basics of Natural Language Processing (NLP) and how to work with log files.
