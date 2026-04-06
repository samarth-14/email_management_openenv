---
title: Email Management OpenEnv
emoji: 📧
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# 📧 Email Management Assistant — OpenEnv Environment

A real-world OpenEnv environment where AI agents practice email management tasks across three difficulty levels.

## 🌐 Live API
Base URL: `https://samm14-email-management-openenv.hf.space`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/reset` | POST | Reset environment with new task |
| `/step` | POST | Execute action, get reward |
| `/state` | GET | Get current state |

## 🎯 Tasks

| Difficulty | Task | Reward Logic |
|------------|------|--------------|
| Easy | Categorize email (spam/promotion/important) | Exact match = 1.0, partial = 0.3 |
| Medium | Draft professional response | Partial credit for politeness + content |
| Hard | Handle multi-email thread with context | Context awareness + solution quality |

## 🚀 Quick Start

### Reset (start a task):
```bash
curl -X POST https://samm14-email-management-openenv.hf.space/reset \
  -H "Content-Type: application/json" \
  -d '{"task_type": "easy"}'
```

### Step (take an action):
```bash
curl -X POST https://samm14-email-management-openenv.hf.space/step \
  -H "Content-Type: application/json" \
  -d '{"action": {"category": "spam"}}'
```

### Run inference locally:
```bash
pip install -r requirements.txt
python inference.py
```

## 🏗️ Project Structure
├── server.py          # FastAPI REST server
├── environment.py     # Core OpenEnv (reset/step/state)
├── models.py          # Pydantic typed models
├── inference.py       # Inference script with structured logs
├── openenv.yaml       # Environment metadata
├── Dockerfile         # Docker deployment
├── requirements.txt   # Dependencies
└── tasks/
├── easy.py        # Categorization task + grader
├── medium.py      # Response drafting task + grader
└── hard.py        # Thread management task + grader
## ✅ Hackathon Requirements Met
- ✅ Real-world environment (not a game)
- ✅ Implements reset(), step(), state()
- ✅ REST API with /reset and /step endpoints
- ✅ Pydantic typed models
- ✅ 3 difficulty levels (Easy/Medium/Hard)
- ✅ Graders with partial rewards (0.0–1.0)
- ✅ [START]/[STEP]/[END] structured logging
- ✅ Dockerized on Hugging Face Spaces
- ✅ Runs under 2 vCPU, 8GB RAM

## 🏆 Meta PyTorch Hackathon — OpenEnv Track
