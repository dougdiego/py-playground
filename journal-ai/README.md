## Prerequisites

- Python 3.13 or higher
- [uv](https://docs.astral.sh/uv/) package manager

## Installation

### 1. Install uv

**Via curl:**

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

**Via Homebrew (macOS):**

```bash
brew install uv
```

**Via pip:**

```bash
pip install uv
```

### 2. Clone and Setup

```bash
git clone <your-repo-url>
cd py-vertex-as
```

### 3. Setup

```bash
uv init --no-readme
```

```
uv add --requirements requirements.txt
```

### 3. Install Dependencies

```bash
uv sync
```

## Configuration

Create a `.env` file in the project root:

## Usage

### Basic Usage

```bash
uv run python main.py
```

### Alternative Usage

```bash
source .venv/bin/activate
python main.py
```
