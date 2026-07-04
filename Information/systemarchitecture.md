# AI Support Assistant for PTZ Cameras & ManyCam

## Software Requirements Specification (SRS) & System Architecture

**Version:** 1.0

**Project Type:** AI Customer Support Assistant

**Technology:** Python + FastAPI + LangChain + RAG + LLM

---

# 1. Purpose

The purpose of this project is to develop an AI-powered support assistant that provides customers with accurate answers and troubleshooting guidance for PTZ cameras and ManyCam software using Retrieval-Augmented Generation (RAG).

The system will become the first line of customer support by answering common questions, guiding users through troubleshooting, and reducing repetitive support requests.

---

# 2. Scope

Version 1 includes:

* AI Chatbot
* RAG Search
* Documentation Search
* Troubleshooting Conversations
* Chat History
* Source Citations

Future versions may include:

* Automatic Diagnostics
* Live Camera Health Monitoring
* Ticket Generation
* CRM Integration

---

# 3. Functional Requirements

## FR-1 User Authentication (Optional)

Admin login

Support engineer login

Customer login (optional)

---

## FR-2 Ask Questions

User can ask:

> My camera isn't detected.

> How do I update firmware?

> What does Error 103 mean?

---

## FR-3 Document Search

Search manuals

Search FAQs

Search troubleshooting guides

Search firmware documents

---

## FR-4 RAG Retrieval

Retrieve top relevant document chunks.

---

## FR-5 AI Response

Generate response only using retrieved company documents.

---

## FR-6 Follow-up Questions

If information is missing:

AI asks additional questions.

---

## FR-7 Conversation Memory

Maintain previous messages.

---

## FR-8 Source Reference

Every answer should mention

* Manual Name

* Section

* Page (if possible)

---

## FR-9 Feedback

👍 Helpful

👎 Not Helpful

---

## FR-10 Analytics

Store:

Question

Answer

Documents Retrieved

Feedback

Time

---

# 4. Non-Functional Requirements

Response Time

< 5 seconds

---

Availability

24×7

---

Security

HTTPS

Authentication

Encrypted API Keys

---

Scalability

Support thousands of documents

Multiple users simultaneously

---

Maintainability

Modular architecture

---

# 5. High-Level Architecture

```text
                Customer

                    │

                    ▼

            Web / Streamlit UI

                    │

                    ▼

              FastAPI Backend

        ┌───────────┴───────────┐

        ▼                       ▼

Conversation Service      Authentication

        │

        ▼

RAG Pipeline

        │

 ┌──────┴────────┐

 ▼               ▼

Vector DB     LLM Service

 │

 ▼

Knowledge Base
```

---

# 6. RAG Pipeline

```text
User Question

      │

      ▼

Embedding Model

      │

      ▼

Vector Database Search

      │

Retrieve Top K Chunks

      │

      ▼

Prompt Builder

      │

      ▼

LLM

      │

      ▼

Final Answer
```

---

# 7. System Modules

## Module 1

Chat Interface

Responsibilities

* Receive question

* Display answer

* Display sources

---

## Module 2

Conversation Manager

Responsibilities

Maintain conversation context

Store history

---

## Module 3

RAG Engine

Responsibilities

Embedding

Similarity Search

Chunk Retrieval

---

## Module 4

Prompt Builder

Responsibilities

Combine

Question

Conversation History

Retrieved Documents

---

## Module 5

LLM Service

Responsibilities

Generate final response

---

## Module 6

Knowledge Base

Stores

PDFs

DOCX

FAQs

Markdown

HTML

---

## Module 7

Analytics

Stores

Questions

Answers

Feedback

---

# 8. Folder Structure

```text
ai-support-assistant/

│

├── app/

│   ├── main.py

│   ├── config.py

│   ├── dependencies.py

│

├── api/

│   ├── chat.py

│   ├── upload.py

│   ├── feedback.py

│

├── services/

│   ├── rag_service.py

│   ├── embedding_service.py

│   ├── llm_service.py

│   ├── document_service.py

│   ├── chat_service.py

│

├── database/

│   ├── models.py

│   ├── connection.py

│

├── vector_db/

│   ├── chroma/

│

├── knowledge_base/

│   ├── Manuals/

│   ├── Troubleshooting/

│   ├── Firmware/

│   ├── FAQs/

│

├── prompts/

│   ├── system_prompt.txt

│

├── embeddings/

│

├── tests/

│

├── requirements.txt

│

└── README.md
```

---

# 9. Database Schema

## Users

| Column | Type             |
| ------ | ---------------- |
| id     | UUID             |
| name   | String           |
| email  | String           |
| role   | Admin / Customer |

---

## Conversations

| Column     | Type      |
| ---------- | --------- |
| id         | UUID      |
| user_id    | UUID      |
| created_at | Timestamp |

---

## Messages

| Column          | Type      |
| --------------- | --------- |
| id              | UUID      |
| conversation_id | UUID      |
| sender          | User / AI |
| message         | Text      |
| timestamp       | Timestamp |

---

## Documents

| Column      | Type      |
| ----------- | --------- |
| id          | UUID      |
| filename    | String    |
| category    | String    |
| uploaded_at | Timestamp |

---

## Feedback

| Column          | Type    |
| --------------- | ------- |
| id              | UUID    |
| conversation_id | UUID    |
| helpful         | Boolean |
| comments        | Text    |

---

# 10. Vector Database

Each chunk stores

```text
Document ID

Chunk ID

Embedding

Page Number

Category

Metadata
```

---

# 11. API Design

## POST

/chat

Request

```json
{
  "question":"Camera not detected"
}
```

Response

```json
{
 "answer":"Check USB cable...",
 "sources":[
   "PTZ Manual Page 23"
 ]
}
```

---

## POST

/upload

Upload documents

---

## GET

/documents

Returns all indexed documents

---

## POST

/feedback

```json
{
 "conversation_id":123,
 "helpful":true
}
```

---

## GET

/history/{conversation_id}

Returns chat history

---

# 12. Sequence Diagram

```text
Customer

   │

Ask Question

   │

   ▼

API

   │

Create Embedding

   │

   ▼

Vector DB

Retrieve Chunks

   │

   ▼

Prompt Builder

   │

   ▼

LLM

   │

Generate Answer

   │

   ▼

API

   │

Store Conversation

   │

   ▼

Customer
```

---

# 13. Prompt Template

System Prompt

"You are an AI Support Engineer.

Answer only using the provided documents.

If information is unavailable, clearly state that you don't know.

Never invent information.

Always provide troubleshooting steps before suggesting contacting support."

---

# 14. Implementation Plan

## Sprint 1

Project setup

FastAPI

Streamlit

Folder structure

Git

---

## Sprint 2

PDF parser

Chunking

Embedding generation

---

## Sprint 3

Vector Database

Search

Similarity retrieval

---

## Sprint 4

LLM integration

Prompt engineering

Testing

---

## Sprint 5

Conversation history

Feedback

Sources

---

## Sprint 6

UI improvements

Deployment

Testing

---

# 15. Future Architecture

```text
Customer

   │

   ▼

Chatbot

   │

   ▼

Diagnostics Service

   │

Camera API

Windows API

Network API

ManyCam Status

   │

Diagnostic Report

   │

RAG

   │

LLM

   │

Final Solution
```

---

# 16. Future Enhancements

Automatic Diagnostics

Support Ticket Generation

Voice Chat

Screen Sharing Analysis

Image Upload

OCR

Firmware Detection

Camera Health Monitoring

Remote Support

CRM Integration

Email Integration

Knowledge Base Auto Update

Multilingual Support

---

# 17. Deployment

Backend

FastAPI

Docker

---

Frontend

Streamlit

---

Vector DB

ChromaDB

---

Database

PostgreSQL (Production)

SQLite (Prototype)

---

Reverse Proxy

Nginx

---

Hosting

Azure

AWS

GCP

On-Premise

---

# 18. Recommended Tech Stack

| Component      | Technology                            |
| -------------- | ------------------------------------- |
| Language       | Python                                |
| API            | FastAPI                               |
| Frontend       | Streamlit                             |
| RAG            | LangChain                             |
| Vector DB      | ChromaDB                              |
| Database       | PostgreSQL                            |
| ORM            | SQLAlchemy                            |
| Embeddings     | OpenAI or BGE                         |
| LLM            | OpenAI GPT / Azure OpenAI / Local LLM |
| PDF Parser     | PyMuPDF                               |
| Authentication | JWT                                   |
| Logging        | Python Logging                        |
| Deployment     | Docker                                |

---

# 19. Success Criteria

* Accurate answers from company documentation
* Response time under 5 seconds (typical)
* Reliable source citations
* Reduced repetitive support requests
* Positive user feedback
* Modular design for future diagnostics integration

---

# 20. Development Philosophy

The project should be developed incrementally:

**Version 1:** Document-based RAG chatbot.

**Version 2:** Interactive troubleshooting with guided questioning.

**Version 3:** Automatic diagnostics using live hardware and software status.

This phased approach delivers value early while creating a scalable foundation for more advanced AI-assisted support capabilities.
