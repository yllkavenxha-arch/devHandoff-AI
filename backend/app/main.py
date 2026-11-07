from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI(title="DevHandoff AI Backend")

@app.get("/")
def root():
    return {"message": "DevHandoff AI API is running!"}

@app.get("/api/github/repo/{owner}/{repo}")
async def get_github_repo(owner: str, repo: str):
    """
    Merr informacionin bazë për një repozitor nga GitHub API.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, 
                detail="Repozitori nuk u gjet ose GitHub API dështoi."
            )
            
        data = response.json()
        return {
            "name": data.get("name"),
            "full_name": data.get("full_name"),
            "description": data.get("description"),
            "stars": data.get("stargazers_count"),
            "forks": data.get("forks_count"),
            "open_issues": data.get("open_issues_count"),
            "default_branch": data.get("default_branch"),
        }

@app.get("/api/github/contents/{owner}/{repo}")
async def get_repo_contents(owner: str, repo: str, path: str = ""):
    """
    Merr listën e skedarëve dhe dosjeve brenda një repozitori.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, 
                detail="Nuk u mundësua leximi i përmbajtjes së repozitorit."
            )
            
        contents = response.json()
        items = []
        for item in contents:
            items.append({
                "name": item.get("name"),
                "path": item.get("path"),
                "type": item.get("type"), # 'file' ose 'dir'
                "size": item.get("size")
            })
            
        return {"items": items}
        