# MCP-DeepResearcher

A lightweight Python application designed to work with the Model Context Protocol (MCP) framework, enabling advanced AI agent orchestration and deep research workflows. The repository hosts core scripts for agent management, server setup, and a Streamlit-based UI.

## 🚀 Features

- **Agent orchestration** via `agents.py` using MCP protocol
- **Web server** support through `server.py` for API endpoints
- **Streamlit UI** in `app.py` for interactive research and demos
- Easy environment setup with `requirements.txt` and `pyproject.toml`

## 🛠️ Getting Started

### Prerequisites
- Python 3.10+ (virtual environment recommended)
- Git installed

### Setup
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd MCP-DeepResearcher
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration
- Review `.env` for environment variables used by the project (e.g., API keys, ports).

## 🧩 Usage

- Launch the Streamlit interface:
  ```bash
  streamlit run app.py
  ```
- Run the server API:
  ```bash
  python server.py
  ```
- Manage agents:
  ```bash
  python agents.py
  ```

## 📁 Project Structure

```
agents.py           # Agent orchestration logic
app.py              # Streamlit UI
server.py           # API server implementation
requirements.txt    # Python dependencies
pyproject.toml      # Project metadata
.env                # Environment variables (excluded from VCS)
```

## 🤝 Contributing
Contributions are welcome! Please open issues or submit pull requests for enhancements and bug fixes.

## 📄 License
Specify your license here (e.g., MIT).
