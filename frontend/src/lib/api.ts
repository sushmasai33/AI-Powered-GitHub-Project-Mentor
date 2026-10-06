import { AnalysisResponse, SampleRepo, MentorMessage } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export async function fetchSampleRepos(): Promise<SampleRepo[]> {
  const res = await fetch(`${API_BASE_URL}/analysis/sample-repos`);
  if (!res.ok) {
    throw new Error('Failed to load sample repositories');
  }
  return res.json();
}

export async function runAnalysis(
  githubUrl: string,
  githubToken?: string,
  branch?: string
): Promise<AnalysisResponse> {
  const res = await fetch(`${API_BASE_URL}/analysis/run`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      github_url: githubUrl,
      github_token: githubToken || undefined,
      branch: branch || undefined,
    }),
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: 'Analysis failed' }));
    throw new Error(errorData.detail || `Server responded with ${res.status}`);
  }

  return res.json();
}

export async function fetchAnalysis(analysisId: string): Promise<AnalysisResponse> {
  const res = await fetch(`${API_BASE_URL}/analysis/${analysisId}`);
  if (!res.ok) {
    throw new Error('Failed to fetch analysis details');
  }
  return res.json();
}

export async function sendMentorMessage(
  repositoryId: string,
  message: string
): Promise<MentorMessage> {
  const res = await fetch(`${API_BASE_URL}/mentor/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      repository_id: repositoryId,
      message,
    }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Mentor chat failed' }));
    throw new Error(err.detail || 'Failed to converse with AI mentor');
  }

  return res.json();
}

export async function fetchChatHistory(repositoryId: string): Promise<MentorMessage[]> {
  const res = await fetch(`${API_BASE_URL}/mentor/history/${repositoryId}`);
  if (!res.ok) {
    return [];
  }
  return res.json();
}

export async function toggleRoadmapItem(itemId: string): Promise<{ id: string; completed: boolean }> {
  const res = await fetch(`${API_BASE_URL}/roadmap/item/${itemId}/toggle`, {
    method: 'POST',
  });
  if (!res.ok) {
    throw new Error('Failed to update roadmap item');
  }
  return res.json();
}
