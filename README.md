# CuisineChat: AI-Powered Restaurant Assistant

CuisineChat revolutionizes restaurant order management through an AI-powered chatbot. Leveraging Natural Language Processing (NLP) and machine learning, it enhances customer service and operational efficiency. Integrated with Dialogflow and a Python backend, it offers real-time order handling and a seamless user experience.

### Code Review Request for Siemens Interview

As requested in your email, please review the main.py file within this repository. This file is central to the application's functionality, and I believe it showcases my coding skills and understanding of Software Development skills. I welcome any feedback or suggestions you may have.

## Features

- **Dialogflow Integration**: Advanced user intent recognition for a natural chat experience.
- **Real-Time Order Management**: Direct database communication for order tracking and updates.
- **MySQL Database Integration**: Reliable order processing with persistent data storage.
- **Session Management**: Dynamic order management through user session tracking.
- **Customizable Responses**: Personalized user interactions to improve service quality.

## Getting Started

### Prerequisites

Ensure you have the following installed:
- Python 3.8+
- FastAPI
- Uvicorn
- MySQL

### Installation
- pip install fastapi uvicorn mysql-connector-python python-dotenv

### Running the Application
-uvicorn main:app --reload

### Use the ngrok URL provided for Dialogflow webhook integration and secure connection
-ngrok http 8000

### Usage
Interact with CuisineChat through Dialogflow or any integrated platform. Users can add to their order, track it, or complete it, with real-time processing and feedback.

### Acknowledgments
Dialogflow: For NLP capabilities.
FastAPI: For the web framework.
The Python Community: For their extensive libraries and tools.
CuisineChat showcases the potential of AI in enhancing the dining experience, making restaurant operations more efficient and customer-friendly.
