# Day 8: Text Embeddings

This project uses Sentence Transformers to turn two text snippets into vectors
and NumPy to calculate their cosine similarity. The script prints one similarity
score for the example sentences in `embading_rag.py`.

## Prerequisites

- Windows 10/11
- Python 3.11 or newer
- [uv](https://docs.astral.sh/uv/)
- The Microsoft Visual C++ Redistributable (needed by PyTorch on Windows):
  [download the x64 redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)

The first run downloads the `all-MiniLM-L6-v2` model, so it needs an internet
connection and may take longer than later runs.

## Set up the environment

Open PowerShell in the repository root (the folder containing `day8\`).

1. Install uv if it is not installed already:

   ```powershell
   winget install --id astral-sh.uv --exact
   ```

   Close and reopen PowerShell, then check the installation:

   ```powershell
   uv --version
   ```

2. Install a compatible Python version managed by uv:

   ```powershell
   uv python install 3.11
   ```

3. The Day 8 dependencies are declared in `day8\pyproject.toml`. To add them
   explicitly to the project (for a new setup or if you change the imports), run:

   ```powershell
   uv add --project day8 numpy python-dotenv sentence-transformers
   ```

   `numpy` is used for cosine similarity and `sentence-transformers` creates
   embeddings. `python-dotenv` is listed in the project dependencies for
   environment-variable configuration; the current example script does not
   import it.

4. Install/sync the dependencies and create the environment:

   ```powershell
   uv sync --package day8
   ```

   This repository is a uv workspace. The command uses its root `uv.lock` and
   shared `.venv`; running it from the repository root ensures uv finds the
   workspace.

## Run the script

From the repository root, run:

```powershell
uv run --package day8 python day8\embading_rag.py
```

Alternatively, change into the Day 8 folder and run:

```powershell
Set-Location .\day8
uv run python .\embading_rag.py
```

The script prints the cosine similarity between “There are 24 paid leaves” and
“cat is a wild animal”. Cosine similarity is a measure of how close two vectors
point in the same direction; a larger value indicates greater similarity.

## Adding or removing dependencies

Run `uv add` from the repository root and name the workspace project:

```powershell
uv add --project day8 <package-name>
```

For example, to add Groq later if the script starts using its client:

```powershell
uv add --project day8 groq
```

To remove a dependency:

```powershell
uv remove --project day8 <package-name>
```

After changing dependencies, sync and run the script again:

```powershell
uv sync --package day8
uv run --package day8 python day8\embading_rag.py
```