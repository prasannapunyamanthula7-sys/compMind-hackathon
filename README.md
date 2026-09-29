# CompMind — Competitive Intelligence Agent

**Know what changed. Remember why it matters.**

CompMind is a memory-first competitive intelligence agent for HackWithHyderabad 3.0.

## Flow
**New competitor signal → Hindsight memory → Historical context → Pattern → Watch next**

## Stack
Python, FastAPI, Hindsight Cloud (`hindsight-client`), optional Groq, HTML/CSS/JS, Render.

## Local run
```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000

Without API keys the app still runs in demo mode. For the real hackathon demo, add `HINDSIGHT_API_KEY` and click **Seed Hindsight memory**.

## GitHub
Create a public repository named `compmind-hackathon`, upload all files, and never upload `.env` or API keys.

## Render
This repo includes `render.yaml`. Create a Render Web Service from the GitHub repo, add the Hindsight API key (and optional Groq key) as environment variables, and deploy. Render provides a public `onrender.com` URL for a web service.

## 60-second demo
1. Show the problem: competitor signals are scattered.
2. Show NovaCloud's old pricing and deployment events.
3. Enter today's new inference tier.
4. Click **Analyze with memory**.
5. Point to the connection trail: pricing + deployment + product.
6. Say: "Without memory this is one announcement. With Hindsight it becomes part of a competitor timeline."
7. Add another signal and analyze again to show the memory growing.

## Submission checklist
- Public GitHub repo
- README with architecture and Hindsight explanation
- Live demo URL
- Demo video
- Article/social/video content deliverables
- Hindsight memory visibly demonstrated
