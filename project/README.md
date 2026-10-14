# AI Resume Screening

An ATS-style command-line tool that extracts information from PDF and DOCX resumes, compares each candidate with an embedded DevOps Engineer job description, and ranks candidates using the Groq API.

## How it works

1. Loads `GROQ_API_KEY` from the environment or a `.env` file and creates a Groq client.
2. Sends the embedded job description to the configured Groq model and validates the structured response with Pydantic.
3. Finds supported resumes in the project's `resume/` directory and extracts text from each PDF or DOCX file.
4. Sends each resume's text to Groq to extract structured candidate details.
5. Sends the structured job and candidate data to Groq for a match score, matching/missing skills, and a verdict.
6. Sorts candidates by score and prints the top two and lowest two candidates.

The main pipeline is in `resume_parser.py`. Its data flow is:

```text
Job description -> structured job
Resume file -> extracted text -> structured resume
Structured job + structured resume -> match result
All match results -> ranked terminal output
```

## Requirements

- Python 3.11 or newer
- [uv](https://docs.astral.sh/uv/) for dependency management
- A Groq API key

## Setup

From this directory, install the declared project dependencies:

```powershell
uv sync --package project --inexact
```

Create a `.env` file in this directory and add your API key:

```dotenv
GROQ_API_KEY=your_groq_api_key
```

Put PDF or DOCX resumes you are authorized to process in `resume/`. Resume documents are intentionally excluded from version control because they may contain personal information. Unsupported file types are ignored.

## Run

Run the resume-screening pipeline from this directory:

```powershell
uv run --no-sync --package project python resume_parser.py
```

The package's configured console command is also available:

```powershell
uv run --no-sync --package project project
```

That console command currently prints a greeting; it does not start the resume-screening pipeline.

## Output and notes

- Results are printed in the terminal; the program does not write a report file.
- The script waits five seconds between its parse and scoring requests for each resume.
- The job description and candidate data are processed by the configured Groq model. Do not run the pipeline on resumes unless you are authorized to share their contents with that service.
- Match scores are model-generated screening assistance, not a hiring decision. Review candidate materials independently.