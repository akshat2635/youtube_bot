# YouTube Chatbot Assistant

A Chrome extension that allows you to ask questions about any YouTube video using AI. The extension extracts video transcripts and uses Google's Gemini AI to provide intelligent answers about the video content.

## 🚀 Features

- **Ask Questions About Videos**: Simply ask any question about the YouTube video you're currently watching
- **Intelligent Responses**: Powered by Google's Gemini 2.0 Flash AI model
- **Automatic Transcript Processing**: Automatically fetches and processes video transcripts in multiple languages
- **Smart Search**: Uses vector embeddings and semantic search to find relevant parts of the transcript
- **Clean UI**: Simple and intuitive popup interface

## 🏗️ Architecture

### Frontend (Chrome Extension)

- **Manifest V3** Chrome extension
- **popup.html/css/js**: Clean interface for user interaction
- **background.js**: Service worker for extension lifecycle

### Backend (FastAPI Server)

- **FastAPI**: RESTful API server
- **LangChain**: Framework for building AI applications
- **FAISS**: Vector database for semantic search
- **Google Gemini AI**: Large language model for answering questions
- **YouTube Transcript API**: For fetching video transcripts

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**
- **Google Chrome Browser**
- **Google API Key** (for Gemini AI)

## 🛠️ Installation & Setup

### Step 1: Clone the Repository

```bash
git clone <your-repository-url>
cd youtube_bot
```

### Step 2: Set Up the Backend

1. **Navigate to the backend directory:**

   ```bash
   cd backend
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**

   ```bash
   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

4. **Install required packages:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables:**

   - Create a `.env` file in the `backend` directory
   - Add your Google API key:

   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

6. **Get a Google API Key:**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the key to your `.env` file

### Step 3: Install the Chrome Extension

1. **Open Google Chrome**

2. **Navigate to Chrome Extensions:**

   - Type `chrome://extensions/` in the address bar
   - Or go to Menu → More Tools → Extensions

3. **Enable Developer Mode:**

   - Toggle the "Developer mode" switch in the top right corner

4. **Load the Extension:**

   - Click "Load unpacked"
   - Navigate to your project folder and select the `extension` directory
   - Click "Select Folder"

5. **Verify Installation:**
   - You should see "YouTube Chatbot Assistant" in your extensions list
   - The extension icon should appear in your Chrome toolbar

## 🚀 Running the Application

### Step 1: Start the Backend Server

1. **Navigate to the backend directory:**

   ```bash
   cd backend
   ```

2. **Activate your virtual environment** (if not already activated):

   ```bash
   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Start the FastAPI server:**

   ```bash
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

4. **Verify the server is running:**
   - Open your browser and go to `http://127.0.0.1:8000/docs`
   - You should see the FastAPI interactive documentation

### Step 2: Use the Extension

1. **Navigate to any YouTube video** in Chrome

2. **Click the extension icon** in your toolbar

3. **Ask a question** about the video in the text area

4. **Click "Ask"** and wait for the AI response

## 🎯 Usage Examples

Once set up, you can ask various types of questions about YouTube videos:

- **Summary Questions**: "What is this video about?"
- **Specific Details**: "What tools does the speaker mention?"
- **Key Points**: "What are the main takeaways?"
- **Explanations**: "How does the speaker explain [concept]?"
- **Quotes**: "What did the speaker say about [topic]?"

## 🔧 Configuration

### Customizing AI Behavior

You can modify the AI prompt in `backend/agent.py`:

```python
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=""" You are a helpful assistant.
You will be given a context and a question. Use the context to answer the question in detail.
If the answer is not interpretable from context, say 'I don't know'.
context: {context}
question: {question}"""
)
```

### Adjusting Search Parameters

Modify the retriever settings in `backend/agent.py`:

```python
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5},  # Number of chunks to retrieve
    search_type="mmr",       # Search algorithm
    search_score_threshold=0.7  # Similarity threshold
)
```

## 🛠️ Troubleshooting

### Common Issues

1. **"Could not talk to the agent" Error:**

   - Ensure the backend server is running on `http://127.0.0.1:8000`
   - Check that your Google API key is correctly set in the `.env` file

2. **"Transcript not found" Error:**

   - The video doesn't have captions/transcripts available
   - Try with a different video that has closed captions

3. **Extension not appearing:**

   - Make sure you loaded the `extension` folder (not the root folder)
   - Check that Developer mode is enabled in Chrome

4. **Import errors when starting the server:**
   - Ensure all packages are installed: `pip install -r requirements.txt`
   - Make sure you're in the correct virtual environment

### Debug Mode

To enable debug mode, modify `backend/main.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📁 Project Structure

```
youtube_bot/
├── backend/
│   ├── agent.py              # AI agent logic
│   ├── main.py               # FastAPI server
│   ├── transcripts.py        # YouTube transcript fetching
│   ├── requirements.txt      # Python dependencies
│   └── .env                  # Environment variables (create this)
├── extension/
│   ├── background.js         # Extension background script
│   ├── manifest.json         # Extension configuration
│   ├── popup.css            # Extension UI styles
│   ├── popup.html           # Extension UI layout
│   └── popup.js             # Extension UI logic
└── README.md                # This file
```

## 🔒 Privacy & Security

- The extension only accesses the current YouTube tab URL to extract video IDs
- Video transcripts are processed locally on your machine
- No personal data is stored or transmitted to external services (except Google AI API)
- All communication between extension and backend happens locally

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Please check the license file for more details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Ensure all prerequisites are installed correctly
3. Verify your Google API key is valid and has the necessary permissions
4. Check the browser console for any error messages

---

**Note**: This extension requires an active internet connection and a valid Google API key to function properly.
