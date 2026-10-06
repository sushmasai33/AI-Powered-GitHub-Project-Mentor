from typing import Dict, List, Any

class InterviewGeneratorService:
    @staticmethod
    def generate_interview_questions(
        analysis_result: Dict[str, Any],
        security_findings: List[Dict[str, Any]],
        file_contents: Dict[str, str]
    ) -> List[Dict[str, Any]]:
        primary_lang = analysis_result.get("primary_language", "Python")
        frameworks = ", ".join(analysis_result.get("detected_frameworks", ["REST framework"]))
        databases = ", ".join(analysis_result.get("detected_databases", ["Relational database"]))
        auth_tech = ", ".join(analysis_result.get("detected_auth", ["Token-based authentication"]))
        arch_type = analysis_result.get("architecture_type", "Layered Architecture")
        
        # Sample files from repo
        main_files = [path for path in file_contents.keys() if not path.lower().endswith(('.md', '.txt'))]
        sample_file_1 = main_files[0] if len(main_files) > 0 else "app/main.py"
        sample_file_2 = main_files[1] if len(main_files) > 1 else "app/database.py"

        questions = [
            # 1. Basic Questions
            {
                "category": "Basic",
                "difficulty": "Beginner",
                "question": f"Can you give an executive summary of this project and explain why you chose {primary_lang} and {frameworks} over alternatives?",
                "expected_answer": f"The project is designed to deliver reliable web services using {primary_lang}. We chose {frameworks} because of its asynchronous capabilities, type annotations, high performance, and rapid prototyping advantages compared to heavier legacy alternatives.",
                "relevant_file": sample_file_1,
                "follow_up_question": f"If you had to rewrite this project in another language (e.g. Go or TypeScript), what trade-offs would you encounter?"
            },
            {
                "category": "Basic",
                "difficulty": "Beginner",
                "question": "Walk me through how dependencies are declared and resolved in this repository.",
                "expected_answer": "Dependencies are pinned in the package manifest (e.g. requirements.txt or package.json). This ensures reproducible local development and production container builds.",
                "relevant_file": "requirements.txt" if "Python" in primary_lang else "package.json",
                "follow_up_question": "How do you detect and mitigate outdated or vulnerable transitive third-party dependencies?"
            },

            # 2. Architecture Questions
            {
                "category": "Architecture",
                "difficulty": "Intermediate",
                "question": f"How is the system architected according to {arch_type}? Why was this structural separation chosen?",
                "expected_answer": f"The codebase adopts {arch_type}. This separates routing/presentation concerns from business logic and database interactions, making the application easier to test, maintain, and refactor independently.",
                "relevant_file": sample_file_1,
                "follow_up_question": "How would you decompose this monolith into microservices or serverless functions if traffic increased by 100x?"
            },
            {
                "category": "Architecture",
                "difficulty": "Intermediate",
                "question": "What happens when an incoming HTTP request hits your server? Trace the full request lifecycle.",
                "expected_answer": f"The request passes through {analysis_result.get('request_workflow', 'the router, middleware, business controller, and database ORM before serializing a JSON response back to the client')}.",
                "relevant_file": sample_file_1,
                "follow_up_question": "Where does connection pooling take place, and how do you prevent thread starvation under heavy load?"
            },

            # 3. Code Questions
            {
                "category": "Code",
                "difficulty": "Intermediate",
                "question": f"Inspect `{sample_file_1}`. What is the role of this module, and how does it ensure error resilience?",
                "expected_answer": f"`{sample_file_1}` acts as a core entry point or router. It defines endpoint signatures, validates inputs, and delegates processing to downstream services.",
                "relevant_file": sample_file_1,
                "follow_up_question": "How do you handle unhandled exceptions here to prevent internal server details or stack traces leaking to users?"
            },
            {
                "category": "Code",
                "difficulty": "Advanced",
                "question": "Explain your approach to input validation and schema serialization in this codebase.",
                "expected_answer": "We enforce strict validation schemas (such as Pydantic models or Zod types) to validate incoming JSON payloads before executing any business logic or database queries.",
                "relevant_file": sample_file_1,
                "follow_up_question": "How do you handle custom sanitization for malicious payloads like XSS or nested object prototype pollution?"
            },

            # 4. Database Questions
            {
                "category": "Database",
                "difficulty": "Intermediate",
                "question": f"Explain the database layer and how ORM models are managed with {databases}.",
                "expected_answer": f"The database uses {databases} to map object models to relational tables. This abstracts raw SQL queries, provides type hinting, and helps prevent injection when using bind parameters.",
                "relevant_file": sample_file_2,
                "follow_up_question": "What is the N+1 query problem, and how do you prevent it in your ORM queries (e.g. joinedload or eager fetching)?"
            },
            {
                "category": "Database",
                "difficulty": "Advanced",
                "question": "How are database migrations and schema changes managed when rolling out updates without downtime?",
                "expected_answer": "Schema changes should be version-controlled using migration tools (such as Alembic or Prisma). Zero-downtime migrations follow the expand-contract pattern: adding columns first, deploying code, and dropping deprecated columns in a subsequent release.",
                "relevant_file": sample_file_2,
                "follow_up_question": "How do you handle database transaction rollbacks if a multi-step operation fails midway?"
            },

            # 5. Security Questions
            {
                "category": "Security",
                "difficulty": "Advanced",
                "question": f"How is user authentication and session verification enforced in this project using {auth_tech}?",
                "expected_answer": f"We utilize {auth_tech}. Requests include bearer tokens signed with a secret key. Middleware decodes the token, checks expiration, and retrieves user context.",
                "relevant_file": "app/auth.py" if "app/auth.py" in file_contents else sample_file_1,
                "follow_up_question": "What is the vulnerability if your JWT secret key is hardcoded or weak, and how do you implement token revocation?"
            },
            {
                "category": "Security",
                "difficulty": "Advanced",
                "question": f"Our automated audit detected {len(security_findings)} security findings in this repository. How do you defend against SQL injection and command injection?",
                "expected_answer": "Never concatenate user input directly into SQL strings or system shells. Always use parameterized queries, ORM expressions, and strict input validation schemas with allowlists.",
                "relevant_file": security_findings[0]["file_path"] if security_findings else sample_file_1,
                "follow_up_question": "What role does Cross-Origin Resource Sharing (CORS) play, and why is wildcard `*` with credentials dangerous?"
            },

            # 6. Advanced Scalability Questions
            {
                "category": "Advanced",
                "difficulty": "Advanced",
                "question": "How would you handle concurrent writes to the same database resource in this system?",
                "expected_answer": "We would use optimistic locking with version fields, or pessimistic database row-level locks (`SELECT FOR UPDATE`), or distributed locks in Redis depending on conflict frequency.",
                "relevant_file": sample_file_2,
                "follow_up_question": "What happens if a deadlock occurs, and how should your application retry the transaction?"
            },
            {
                "category": "Advanced",
                "difficulty": "Advanced",
                "question": "What are the single points of failure (SPOF) in your current architecture, and how would you eliminate them in production?",
                "expected_answer": "Currently, running a single backend instance and a single database node creates single points of failure. In production, we would deploy multiple replicas behind an application load balancer with database read-replicas and multi-AZ failover.",
                "relevant_file": "Dockerfile" if "Dockerfile" in file_contents else sample_file_1,
                "follow_up_question": "How would you implement health checks and graceful shutdown to ensure zero-downtime rolling deployments?"
            }
        ]

        return questions
