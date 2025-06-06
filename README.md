# Install uv

```
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
```

# Create .env

```
OPENAI_API_KEY="sk-..."
OPENAI_BASE_URL="http://..."
LLM_MODEL="gpt-4.1"
```

# Fetch latest universe.json

```
wget -O universe.json https://raw.githubusercontent.com/bgoosman/studiofinder/refs/heads/main/packages/view/slots/universe.json
```

# Run streamlit app

```
source .venv/bin/activate
streamlit run main.py
```

On Azure:

```
sudo /home/azurevm/studiofinder-assistant/.venv/bin/streamlit run main.py --server.port=80
```