import os
import json
import re
import time
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq, RateLimitError
from pydantic import BaseModel
from pypdf import PdfReader
from docx import Document

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY is missing. Add it to your .env file.")

client = Groq(api_key=groq_api_key)
MODEL = "openai/gpt-oss-20b"


def create_completion_with_rate_limit_retry(**kwargs):
    for attempt in range(3):
        try:
            return client.chat.completions.create(**kwargs)
        except RateLimitError as exc:
            if attempt == 2:
                raise

            retry_after_ms = exc.response.headers.get("retry-after-ms")
            retry_after = exc.response.headers.get("retry-after")
            if retry_after_ms is not None:
                delay = float(retry_after_ms) / 1000
            elif retry_after is not None:
                delay = float(retry_after)
            else:
                match = re.search(
                    r"try again in ([0-9]+(?:\.[0-9]+)?)s",
                    str(exc),
                    re.IGNORECASE,
                )
                if match is None:
                    raise
                delay = float(match.group(1))

            time.sleep(delay + 1)


job_description = ''' # DevOps Engineer, Public Sector

## Role Overview

* Build, improve, and maintain CI/CD pipelines.
* Help move the organization from manual and separate deployment processes to a unified and automated SDLC.
* Work closely with product and engineering teams to improve deployment workflows.
* Develop a strong understanding of product architecture and deployment requirements.
* Integrate machine-learning (ML) tasks and updates into the software development lifecycle.
* ML expertise is not required, but willingness to learn and integrate ML components is important.

## Mandatory Requirement

* Must have an **active TS/SCI security clearance**.
* Must have the **ability and willingness to obtain a CI Poly**.
* Candidates without at least TS/SCI clearance will not be considered.

## Responsibilities

* Design, develop, and maintain robust CI/CD pipelines.
* Automate deployment of low-side and high-side products.
* Collaborate with product and engineering teams.
* Modify or improve application code to work effectively with automated CI/CD pipelines.
* Contribute to deployment-system architecture and design.
* Develop new solutions to improve deployment efficiency and reliability.
* Troubleshoot and resolve complex deployment issues.
* Minimize disruptions to development cycles.
* Develop a deep understanding of product architecture.
* Understand ML architectures and integrate ML components into deployment workflows.
* Integrate ML tasks and updates into the SDLC.
* Document CI/CD pipelines, configurations, and deployment processes.
* Ensure deployment processes are maintainable and easy to understand.
* Apply security best practices throughout the CI/CD pipeline.
* Integrate security into the software development process.
* Standardize CI/CD and deployment processes across product teams.
* Improve collaboration and create a unified and efficient SDLC.

## Required Experience

* **2–3 years** of experience in:

  * DevOps Engineering
  * DevSecOps Engineering
  * Software Engineering with a strong CI/CD focus
  * Similar roles
* Proven experience building or significantly improving CI/CD pipelines.
* Experience adapting application code to work with CI/CD environments.
* Experience with containerization and deployment technologies.
* Experience with Kubernetes, Terraform, Docker, or similar technologies.
* Experience with cloud platforms such as:

  * AWS
  * Azure
  * GCP

## Technical Skills

### CI/CD

* Jenkins
* GitHub Actions
* GitLab CI
* Azure DevOps
* CI/CD pipeline development
* Deployment automation

### Infrastructure & Containers

* Kubernetes
* Docker
* Terraform
* Containerization
* Infrastructure/deployment automation

### Cloud

* AWS
* Azure
* GCP

### Programming & Scripting

* Python
* Bash
* PowerShell
* Automation scripting

### Software Engineering

* Software architecture
* System design
* Version control
* Application integration
* Troubleshooting

### Security / DevSecOps

* Software security best practices
* Secure software development
* Security within CI/CD pipelines
* Secure SDLC
* DevSecOps concepts

## ML / MLOps

* ML expertise is **not required**.
* Willingness to learn ML systems is important.
* Interest in integrating ML components into CI/CD workflows.
* Interest in ML deployment and lifecycle processes.
* Exposure to MLOps concepts is a plus.
* Experience with ML lifecycles is a plus.

## Nice-to-Have Qualifications

* Experience with Docker.
* Experience with Kubernetes.
* Exposure to machine-learning lifecycles.
* Knowledge of MLOps concepts.
* Previous experience working in classified environments.

## Soft Skills

* Strong problem-solving skills.
* Strong analytical skills.
* Strong communication skills.
* Strong collaboration skills.
* Ability to work in rapidly changing environments.
* Ability to work in fast-paced environments.
* Passion for automation.
* Ability to find automated solutions to complex problems.
* Strong willingness to learn new technologies.
* Interest in ML and integrating ML into automated workflows.

## Company / Role Context

* Scale develops reliable AI systems for important real-world decisions.
* Scale provides data and full-stack technologies for AI models and AI applications.
* The company works with industry and government organizations.
* The role supports the development, deployment, and automation of AI-related products.

## Compensation

* San Francisco, New York, Seattle: **$198,400–$311,000 USD**
* Hawaii, Washington DC, Texas, Colorado: **$178,400–$279,000 USD**
* St. Louis: **$148,800–$233,000 USD**
* Compensation may include:

  * Base salary
  * Equity
  * Health benefits
  * Dental benefits
  * Vision benefits
  * Retirement benefits
  * Learning and development stipend
  * PTO
  * Potential commuter benefits

## Application Note

* Candidates must meet the TS/SCI clearance requirement.
* There is a **90-day waiting period** before candidates can be reconsidered for the same role.
'''

class JobD(BaseModel):
    title: str
    role_overview: str
    mandatory_requirement: str
    responsibilities: str
    required_experience: str
    technical_skills: str
    ml_mops: str
    nice_to_have_qualifications: str
    soft_skills: str
    company_role_context: str
    compensation: str
    application_note: str


Jobd_schema = JobD.model_json_schema()


system_prompt = f"""
you are expert HR assistant.

your job is to analyze the job description and extract the structured relevant information.

return ONLY valid JSON following this schema:

{Jobd_schema}

important:
DO not return the schema itself.
Do not return fields like "properties", "title", "type".
fill the schema with the relevant information extracted from the job description.

if minimum experience is not mentioned, return null.
if information for a list is missing, return an empty list.
do not invent information """


user_prompt = f"""
analyze the following job description and extract the relevant information.

JOB DESCRIPTION:
{job_description}
"""
message_system = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt}
]
response_format = {
    "type" : "json_object"
}


# 4. Call the LLM
response = create_completion_with_rate_limit_retry(
    model=MODEL,
    messages=message_system,
    temperature=0,
    max_completion_tokens= 8888,
    response_format=response_format
)

# 5. Get the response
result = response.choices[0].message.content

job_data = json.loads(result)
if not isinstance(job_data, dict):
    raise ValueError("Groq returned a non-object JSON response for the job description.")

job = JobD.model_validate(job_data)

# PARSE REAL
class MatchResult(BaseModel):
    match_score: float
    matched_skills: list[str]
    missing_skills: list[str]
    missing_experience: list[str]
    missing_education: list[str]
    missing_certifications: list[str]
    details: dict

class Experience(BaseModel):
    company: str | None = None
    role: str | None = None
    duration: str | None = None
    skill_used: list[str] | None = None

class Resume(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None

    total_experience_year: float | None = None

    education: list[str] | None = None
    experience: list[Experience] | None = None
    projects: list[str] | None = None
    skills: list[str] | None = None
    certifications: list[str] | None = None

resume_schema = Resume.model_json_schema()



def final_score(job: JobD, candidate_resume: Resume) -> MatchResult:
    match_schema = MatchResult.model_json_schema()
    prompt = f"""
    You are an HR recruiter.

    Compare the candidate's resume with the job description.

    JOB DESCRIPTION:
    {job.model_dump_json(indent=2)}

    CANDIDATE RESUME:
    {candidate_resume.model_dump_json(indent=2)}
    Return JSON matching this schema:

    {match_schema}

    Give me:

    1. Candidate name
    2. Matching skills
    3. Missing important skills
    4. Whether experience requirement is met
    5. Overall match percentage from 0 to 100
    6. A short final verdict

    Keep the response concise and easy to read.
    """
    message={
        "role": "user",
        "content" : prompt
    }
    messages=[message]
    response_format={
        "type": "json_object"
    }
    response = create_completion_with_rate_limit_retry(
        model=MODEL,
        messages=messages,
        temperature=0,
        max_completion_tokens= 8888,
        response_format=response_format,
    )
    data = json.loads(response.choices[0].message.content)
    if not isinstance(data, dict):
        raise ValueError("Groq returned a non-object JSON response for the candidate match.")
    return MatchResult.model_validate(data)

def parse_resume(resume_text: str) -> Resume:
    system_prompt = f"""
    You are an expert resume parser.

    Extract information from the resume based on its meaning,
    not only based on exact section headings.

    Different resumes may use different headings.

    For example:
    - Experience
    - Professional Experience
    - Work History
    - Employment
    - Internships

    These may all contain relevant experience.

    Skills may also appear in the skills section, work experience,
    internships or projects.

    Return ONLY valid JSON matching this schema:

    {resume_schema}

    Important rules:

    1. Do not invent information.
    2. If a value is not available, return null.
    3. If a list has no information, return an empty list.
    4. Include internships inside experiences.
    5. Extract skills mentioned across the entire resume.
    """
    user_prompt = f"""
    Parse the following resume:

    {resume_text}
    """
    message_system={
        "role" : "system",
        "content" : system_prompt
    }
    message_user={
        "role" : "user",
        "content" : user_prompt
    }
    messages=[message_system, message_user]
    response_format={
        "type": "json_object"
    }
    response = create_completion_with_rate_limit_retry(
        model=MODEL,
        messages=messages,
        temperature=0,
        max_completion_tokens= 8888,
        response_format=response_format,
    )
    raw_output = response.choices[0].message.content
    data = json.loads(raw_output)
    if not isinstance(data, dict):
        raise ValueError(
            "Groq returned a top-level "
            f"{type(data).__name__} instead of a JSON object for the resume."
        )
    return Resume.model_validate(data)












def read_pdf(file_path: Path) -> str:
    """Read text from a PDF file."""
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        text = ''
        for page in reader.pages:
            text += (page.extract_text() or "") + "\n"
    return text


def read_docx(file_path: Path) -> str:
    """Read text from a DOCX file."""
    doc = Document(file_path)
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text

def read_resume(file_path: Path) -> str:
    """Read text from a resume file (PDF or DOCX)."""
    if file_path.suffix.lower() == ".pdf":
        return read_pdf(file_path)
    if file_path.suffix.lower() == ".docx":
        return read_docx(file_path)
    raise ValueError(f"Unsupported resume format: {file_path.suffix}")


# lets do it now
resume_folder = Path(__file__).resolve().parent / "resume"
if not resume_folder.is_dir():
    raise FileNotFoundError(f"Resume folder does not exist: {resume_folder}")

all_results=[]
for file_path in resume_folder.iterdir():
    #C:\Users\Pratyush\padho_with_pratyush\week1\day5\resumes\abhay resume new - Abhay Singh.pdf
    if file_path.suffix.lower() not in [".pdf", ".docx"]:
        continue
    print("\nProcessing:", file_path.name)
    resume_text = read_resume(file_path)
    parsed_resume=parse_resume(resume_text) # llm call1
    time.sleep(5)
    result = final_score(job, parsed_resume) #llm caLL2
    #score and details
    #acount chtgpt
    # request bhejna shhur krega millions
    #chattgot server jam ho jayega
    time.sleep(5)
    print("Score:", result.match_score)
    all_results.append({
        "name": parsed_resume.name or file_path.stem,
        "score": result.match_score,
        "details": result.details
    })
all_results.sort(
    key=lambda candidate: candidate["score"],
    reverse=True
)
top_2 = all_results[:2]
worst_2 = all_results[-2:]


print("TOP 2 CANDIDATES")
for candidate in top_2:

    print(
        candidate["name"],
        "-",
        candidate["score"],
        "%"
    )

    print(candidate["details"])

print("LOWEST 2 CANDIDATES")
for candidate in worst_2:

    print(
        candidate["name"],
        "-",
        candidate["score"],
        "%"
    )
    print(candidate["details"])