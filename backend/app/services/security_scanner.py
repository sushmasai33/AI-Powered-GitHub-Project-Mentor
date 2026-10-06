import re
from typing import Dict, List, Any

# Security patterns with regex, category, severity, CWE, explanation, impact, and fix
SECURITY_RULES = [
    {
        "id": "SEC-001",
        "title": "Hardcoded Secret / API Key / Credential Detected",
        "regex": r'(?i)(secret[_-]?key|api[_-]?key|password|jwt[_-]?secret|private[_-]?key)\s*=\s*[\'"][A-Za-z0-9_\-!@#$%^&*]{10,}[\'"]',
        "severity": "critical",
        "cwe_id": "CWE-798: Use of Hard-coded Credentials",
        "explanation": "Sensitive credentials or secret keys are committed directly inside source code.",
        "impact": "Anyone with repository access can extract these credentials to impersonate users, tamper with JWTs, or access private databases.",
        "fix": "Move all secrets into an environment file (.env) and access them using os.getenv() or process.env. Ensure .env is added to .gitignore."
    },
    {
        "id": "SEC-002",
        "title": "Potential SQL Injection via Raw String Formatting",
        "regex": r'(?i)(f[\'"].*?(SELECT|INSERT|UPDATE|DELETE|FROM|WHERE).*?\{|(execute|query|raw)\s*\(\s*(f[\'"].*?SELECT.*?[{]|[\'"].*?SELECT.*?[\'"]\s*%))',
        "severity": "critical",
        "cwe_id": "CWE-89: Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')",
        "explanation": "SQL query uses direct string interpolation or f-strings instead of parameterized queries.",
        "impact": "Attackers can manipulate the query structure to bypass authentication, exfiltrate the entire database, or delete tables.",
        "fix": "Use parameterized queries or ORM query builders (e.g. `db.execute(text('SELECT * FROM items WHERE id = :id'), {'id': user_id})`)."
    },
    {
        "id": "SEC-003",
        "title": "Arbitrary Command Execution / Unsafe Eval",
        "regex": r'(?i)(os\.system|subprocess\.(call|Popen|run)\(.*shell\s*=\s*True|eval\(|exec\(|child_process\.exec\()',
        "severity": "critical",
        "cwe_id": "CWE-78: Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection')",
        "explanation": "Direct invocation of system shell or dynamic code evaluation functions.",
        "impact": "If user-controlled input reaches these functions, an attacker can execute arbitrary operating system commands on the host server.",
        "fix": "Avoid shell=True and dynamic eval. Use safe library APIs or pass arguments as discrete lists to subprocess without a shell."
    },
    {
        "id": "SEC-004",
        "title": "Cross-Site Scripting (XSS) via Unsafe HTML Injection",
        "regex": r'(?i)(dangerouslySetInnerHTML|\.innerHTML\s*=)',
        "severity": "high",
        "cwe_id": "CWE-79: Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')",
        "explanation": "Injecting unsanitized HTML directly into the DOM allows malicious scripts to execute in the browser.",
        "impact": "Attackers can steal session cookies, hijack user sessions, or execute actions on behalf of the victim.",
        "fix": "Rely on React's automatic string escaping or sanitize untrusted HTML using libraries such as DOMPurify."
    },
    {
        "id": "SEC-005",
        "title": "Wildcard Permissive CORS Configuration with Credentials",
        "regex": r'(?i)allow_origins\s*=\s*\[\s*[\'"]\*[\'"]\s*\].*?allow_credentials\s*=\s*True',
        "severity": "medium",
        "cwe_id": "CWE-942: Permissive Cross-domain Policy with Untrusted Domains",
        "explanation": "CORS policy allows all origins while permitting cookie/credential transmission.",
        "impact": "Malicious websites can make cross-origin requests to your API and read sensitive responses using the victim's session.",
        "fix": "Specify explicit trusted domains in `allow_origins` instead of wildcard `['*']`."
    },
    {
        "id": "SEC-006",
        "title": "Debug Mode Enabled in Configuration",
        "regex": r'(?i)(DEBUG\s*=\s*True|app\.debug\s*=\s*True)',
        "severity": "medium",
        "cwe_id": "CWE-489: Active Debug Code in Production",
        "explanation": "Debug mode is hardcoded to True.",
        "impact": "Debug mode can leak full application stack traces, environment variables, and interactive consoles to end users.",
        "fix": "Set DEBUG to False in production or bind it to environment variable `DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'`."
    },
    {
        "id": "SEC-007",
        "title": "Insecure Deserialization via Python Pickle",
        "regex": r'(?i)pickle\.(loads|load)\(',
        "severity": "high",
        "cwe_id": "CWE-502: Deserialization of Untrusted Data",
        "explanation": "Using Python's pickle library on external data can result in remote code execution.",
        "impact": "An attacker can craft a serialized payload that executes malicious instructions when unpickled.",
        "fix": "Use safe data formats such as JSON or Protocol Buffers for untrusted client communication."
    },
    {
        "id": "SEC-008",
        "title": "Exposed Supabase Service Role Key on Client",
        "regex": r'(?i)(SUPABASE_SERVICE_ROLE_KEY|service_role_key)',
        "severity": "critical",
        "cwe_id": "CWE-285: Improper Authorization",
        "explanation": "Supabase Service Role Key grants unrestricted database superuser access bypassing Row Level Security (RLS).",
        "impact": "If exposed to the frontend, any user can read, modify, or delete every table in the database.",
        "fix": "Only use the public `anon` key on the client. Keep the `service_role` key strictly on secure backend servers."
    }
]

class SecurityScannerService:
    @staticmethod
    def scan_repository(file_contents: Dict[str, str]) -> List[Dict[str, Any]]:
        findings = []
        
        for file_path, content in file_contents.items():
            lines = content.split('\n')
            for line_idx, line in enumerate(lines, start=1):
                for rule in SECURITY_RULES:
                    if re.search(rule["regex"], line):
                        # Extract clean snippet
                        snippet = line.strip()
                        if len(snippet) > 120:
                            snippet = snippet[:117] + "..."
                        
                        findings.append({
                            "title": rule["title"],
                            "category": "security",
                            "severity": rule["severity"],
                            "file_path": file_path,
                            "line_number": line_idx,
                            "snippet": snippet,
                            "explanation": rule["explanation"],
                            "recommendation": rule["fix"],
                            "cwe_id": rule["cwe_id"]
                        })
                        break # Prevent duplicate rules firing on same line
        
        return findings
