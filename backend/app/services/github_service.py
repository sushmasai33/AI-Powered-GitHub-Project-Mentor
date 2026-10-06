import re
import base64
from typing import Dict, List, Optional, Tuple, Any
import httpx
from app.config import settings

IGNORED_PATTERNS = [
    r'^\.git/',
    r'^node_modules/',
    r'^vendor/',
    r'^\.next/',
    r'^dist/',
    r'^build/',
    r'^\.venv/',
    r'^venv/',
    r'^env/',
    r'__pycache__/',
    r'\.pyc$',
    r'\.png$',
    r'\.jpg$',
    r'\.jpeg$',
    r'\.gif$',
    r'\.svg$',
    r'\.ico$',
    r'\.woff2?$',
    r'\.ttf$',
    r'\.eot$',
    r'\.mp4$',
    r'\.zip$',
    r'\.tar\.gz$',
    r'\.pdf$',
    r'\.exe$',
    r'\.dll$',
    r'\.so$',
    r'package-lock\.json$',
    r'yarn\.lock$',
    r'pnpm-lock\.yaml$'
]

def is_ignored(path: str) -> bool:
    for pattern in IGNORED_PATTERNS:
        if re.search(pattern, path, re.IGNORECASE):
            return True
    return False

def parse_github_url(url: str) -> Tuple[str, str]:
    """Extract (owner, repo) from a GitHub repository URL or shorthand 'owner/repo'."""
    clean_url = url.strip().rstrip('/')
    if clean_url.endswith('.git'):
        clean_url = clean_url[:-4]
    
    # Match standard URLs: https://github.com/owner/repo or github.com/owner/repo
    match = re.search(r'(?:https?://)?(?:www\.)?github\.com/([^/]+)/([^/]+)', clean_url, re.IGNORECASE)
    if match:
        return match.group(1), match.group(2)
    
    # Match shorthand: owner/repo
    shorthand = re.search(r'^([a-zA-Z0-9_\-\.]+)/([a-zA-Z0-9_\-\.]+)$', clean_url)
    if shorthand:
        return shorthand.group(1), shorthand.group(2)

    raise ValueError(f"Invalid repository reference: '{url}'. Please provide either a GitHub URL (https://github.com/owner/repo) or shorthand 'owner/repo'.")

class GitHubService:
    def __init__(self, token: Optional[str] = None):
        self.token = token or settings.GITHUB_TOKEN
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "AI-GitHub-Project-Mentor"
        }
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"

    async def fetch_repo_metadata(self, owner: str, repo: str) -> Dict[str, Any]:
        """Fetch metadata about a repository."""
        url = f"https://api.github.com/repos/{owner}/{repo}"
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(url, headers=self.headers)
            if resp.status_code == 404:
                raise ValueError(f"Repository '{owner}/{repo}' not found on GitHub. If it is private, please provide a GitHub Personal Access Token in Advanced Options.")
            elif resp.status_code == 403:
                raise ValueError("GitHub API hourly rate limit reached for unauthenticated requests. Please provide a GitHub Personal Access Token under 'Advanced Options' for 5,000 req/hr, or click our 1-click sample repositories.")
            elif resp.status_code != 200:
                raise ValueError(f"GitHub API error: HTTP {resp.status_code}: {resp.text}")
            return resp.json()

    async def fetch_repo_tree(self, owner: str, repo: str, branch: str) -> List[Dict[str, Any]]:
        """Fetch recursive file tree of the repository with contents API fallback."""
        url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
        async with httpx.AsyncClient(timeout=20.0) as client:
            try:
                resp = await client.get(url, headers=self.headers)
                if resp.status_code == 200:
                    data = resp.json()
                    tree = data.get("tree", [])
                    return [item for item in tree if item.get("type") == "blob" and not is_ignored(item.get("path", ""))]
            except Exception:
                pass

            # Fallback to contents API
            try:
                contents_url = f"https://api.github.com/repos/{owner}/{repo}/contents?ref={branch}"
                c_resp = await client.get(contents_url, headers=self.headers)
                if c_resp.status_code == 200:
                    items = c_resp.json()
                    return [{"path": item["name"], "type": "blob"} for item in items if isinstance(item, dict) and "name" in item and not is_ignored(item["name"])]
            except Exception:
                pass
            return []

    async def fetch_file_content(self, owner: str, repo: str, path: str, branch: str = "main") -> str:
        """Fetch raw content of a specific file."""
        url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(url, headers=self.headers)
            if resp.status_code == 200:
                return resp.text
            
            # Fallback to API endpoint
            api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}"
            api_resp = await client.get(api_url, headers=self.headers)
            if api_resp.status_code == 200:
                content_b64 = api_resp.json().get("content", "")
                return base64.b64decode(content_b64).decode("utf-8", errors="replace")
            return ""

    async def ingest_repository(self, owner: str, repo: str, branch: Optional[str] = None) -> Dict[str, Any]:
        """Ingests repository structure and critical source files."""
        meta = await self.fetch_repo_metadata(owner, repo)
        default_branch = branch or meta.get("default_branch", "main")
        tree_items = await self.fetch_repo_tree(owner, repo, default_branch)
        
        file_paths = [item["path"] for item in tree_items]
        
        # Priority files to fetch contents for analysis
        priority_files = []
        for path in file_paths:
            path_lower = path.lower()
            if path_lower.endswith(('readme.md', 'readme.txt', 'readme')):
                priority_files.append(path)
            elif path_lower.endswith(('package.json', 'requirements.txt', 'pyproject.toml', 'cargo.toml', 'pom.xml', 'go.mod', 'dockerfile', 'docker-compose.yml')):
                priority_files.append(path)
            elif any(k in path_lower for k in ['auth', 'route', 'controller', 'model', 'api', 'main', 'app', 'server', 'index', 'schema', 'config']):
                if path_lower.endswith(('.py', '.ts', '.js', '.jsx', '.tsx', '.go', '.java', '.rb')):
                    priority_files.append(path)
            elif any(k in path_lower for k in ['test', 'spec']):
                priority_files.append(path)

        # Limit priority files to 25 to respect rate limits and latency
        priority_files = priority_files[:25]
        
        file_contents = {}
        for file_path in priority_files:
            try:
                content = await self.fetch_file_content(owner, repo, file_path, default_branch)
                if content:
                    file_contents[file_path] = content
            except Exception:
                continue

        return {
            "metadata": meta,
            "owner": owner,
            "repo": repo,
            "branch": default_branch,
            "tree": file_paths,
            "file_contents": file_contents
        }
