
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks, Header
from config import settings
from utils.security import verify_github_signature
from services.ai_service import inspect_code_diff
from services.github_service import fetch_pr_diff, post_github_comment


app = FastAPI(
    title="AI Code Inspector API",
    description="Automated AI PR Code Reviewer built with FastAPI and Gemini 1.5 Flash",
    version="1.0.0"
)

def process_pull_request_event(repo_full_name: str, pr_number: int, diff_url: str):
    """
    Background worker function that fetches PR diff, runs Gemini AI inspection,
    and posts the result as a comment on GitHub.
    """
    # 1. Fetch raw diff from GitHub
    diff_text = fetch_pr_diff(diff_url)
    if not diff_text.strip():
        print(f"Skipping PR #{pr_number}: Empty or inaccessible diff.")
        return

    # 2. Perform AI Inspection via Gemini 1.5 Flash
    review_result = inspect_code_diff(diff_text)

    # 3. Post review feedback as a PR comment
    post_github_comment(repo_full_name, pr_number, review_result)


from fastapi import FastAPI, Request, BackgroundTasks, Header, HTTPException

@app.post("/webhook")
async def handle_github_webhook(
    request: Request, 
    background_tasks: BackgroundTasks,
    x_hub_signature_256: str = Header(None)
):
    try:
        body = await request.body()
        
        
        if x_hub_signature_256:
            verify_github_signature(body, x_hub_signature_256)
            
        payload = await request.json()
        
        
        event_type = request.headers.get("X-GitHub-Event", "unknown")
        if event_type == "ping":
            return {"status": "success", "message": "Pong! Webhook is active."}
        
        
        if event_type == "pull_request" and payload.get("action") in ["opened", "synchronize"]:
            pr_number = payload["pull_request"]["number"]
            repo_full_name = payload["repository"]["full_name"]
            
            
            background_tasks.add_task(run_ai_code_review, repo_full_name, pr_number)

        return {"status": "success", "message": f"Event {event_type} received successfully"}

    except Exception as e:
        print(f"Webhook Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))




@app.get("/health")
def health_check():
    """
    Health check endpoint for cloud hosting monitoring (Render/UptimeRobot).
    """
    return {"status": "healthy", "service": "AI Code Inspector"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
@app.get("/")
def read_root():
    return {
        "status": "active",
        "message": "AI GitHub PR Code Inspector Bot is live and running successfully!"
    }    