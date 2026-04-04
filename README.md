\# Email Management Assistant - OpenEnv Environment



A real-world OpenEnv environment for AI agents to practice email management tasks.



\## 🎯 Overview



This environment simulates an email inbox where agents must:

\- \*\*Easy Task\*\*: Categorize emails (spam/promotion/important)

\- \*\*Medium Task\*\*: Draft professional responses

\- \*\*Hard Task\*\*: Handle multi-email conversation threads with context



\## 🏗️ Environment Structure



\- `environment.py` - Core OpenEnv implementation (reset, step, state)

\- `models.py` - Pydantic typed models for Email, Action, State

\- `tasks/` - Task definitions and grading functions

\- `inference.py` - Agent inference script with structured logging

\- `openenv.yaml` - Environment metadata



\## 🎓 Task Difficulties



\### Easy: Email Categorization

Agent categorizes emails into spam, promotion, or important.

\- \*\*Grading\*\*: Exact match = 1.0, partial credit for confusion between important/promotion = 0.3



\### Medium: Response Drafting

Agent writes appropriate responses to customer emails.

\- \*\*Grading\*\*: Partial credit system (politeness + content relevance + completeness)



\### Hard: Thread Management

Agent manages multi-email conversations with context tracking.

\- \*\*Grading\*\*: Context awareness + urgency recognition + solution proposal



\## 🚀 Running the Environment



\### Install dependencies:

```bash

pip install -r requirements.txt

```



\### Run inference:

```bash

python inference.py

```



\### Environment variables:

\- `API\_BASE\_URL` - AI model endpoint

\- `MODEL\_NAME` - Model name to use

\- `HF\_TOKEN` - Authentication token



\## 📋 Requirements Met



✅ Real-world environment (email management)  

✅ Implements reset(), step(), state()  

✅ Has openenv.yaml with task metadata  

✅ Uses Pydantic typed models  

✅ 3 tasks (easy/medium/hard)  

✅ Grader functions with 0.0-1.0 rewards  

✅ Partial progress signals in rewards  

✅ inference.py with \[START]/\[STEP]/\[END] logs  

✅ Dockerfile for deployment  

✅ Runs under 2 vCPU, 8GB RAM constraints  



\## 🏆 Hackathon Submission



Created for the Meta PyTorch Hackathon - OpenEnv Track

