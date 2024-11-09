# Customer Service AI Chat

A simple customer service chat application powered by OpenAI's GPT, built with Django. Features product catalog integration and real-time AI responses.

## Prerequisites

- Python 3.8+
- OpenAI API key

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/Edwin2711/assistant_tools_openai.git
cd assistant_tools_openai
```
2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
```
or
```bash
venv\Scripts\activate  # Windows
```
3. Install dependencies:

```bash
pip install -r requirements.txt
```
4. Create .env file in project root:
```bash
OPENAI_API_KEY=your_api_key_here
```

6. Run migrations:
```bash
python manage.py migrate
```

6. Start development server:
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000 to use the chat.

### Features

- Real-time chat interface
- OpenAI GPT integration
- Product catalog with function calling
- Simple UI

### Tech Stack

- Django
- OpenAI API
- JavaScript
- HTML/CSS

