#!/usr/bin/env python3
"""
Sanitize the pull_request event and fetch a limited amount of patch data for changed files.
Produces:
 - sanitized.json (file)
 - prints a compact JSON to GITHUB_OUTPUT as `sanitized`
Notes:
 - redact URLs and emails
 - truncate long texts
 - limit number of files and length per patch
"""

import json
import os
import re
import sys

GITHUB_EVENT_PATH = os.environ.get("GITHUB_EVENT_PATH")

if not GITHUB_EVENT_PATH:
  print("GITHUB_EVENT_PATH not set", flush=True)
  raise SystemExit(1)

with open(GITHUB_EVENT_PATH, 'r', encoding='utf-8') as f:
    p = json.load(f)

# Helper: truncate long strings and redact emails/urls
def clean_str(s, max_len=1000):
  if s is None: return None
  # redact emails and tokens-looking strings
  s = re.sub(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', '[REDACTED_EMAIL]', s)
  s = re.sub(r'https?://[^\s]+', '[REDACTED_URL]', s)
  return s if len(s) <= max_len else f"{s[:max_len]}...[TRUNCATED]"

wf = p.get('workflow_run', {})
repo = p.get('repository', {})
actor = wf.get('actor') or p.get('sender') or {}

sanitized = {
  "workflow_run": {
      "id": wf.get("id"),
      "name": wf.get("name"),
      "conclusion": wf.get("conclusion"),
      "html_url": wf.get("html_url"),
      "head_branch": clean_str(wf.get("head_branch"), 200),
      "head_sha": clean_str(wf.get("head_sha"), 200),
      "run_started_at": wf.get("run_started_at")
  },
  "repository": {
      "full_name": repo.get("full_name"),
      "private": repo.get("private", False)
  },
  "actor": {
      "login": actor.get("login") if isinstance(actor, dict) else clean_str(actor, 200)
  }
}

# Convert to single-line compact JSON for safe passing
compact = json.dumps(sanitized, ensure_ascii=False)

# Write to file for debugging/inspection
with open('sanitized.json','w', encoding='utf-8') as f:
  json.dump(sanitized, f, ensure_ascii=False, indent=2)

# Emit as output for GitHub Actions
github_output = os.environ.get('GITHUB_OUTPUT')
if not github_output:
  print("GITHUB_OUTPUT not found", file=sys.stderr)
  print(compact)
  sys.exit(1)

with open(github_output, 'a', encoding='utf-8') as ghout:
  ghout.write("sanitized<<EOF\n")
  ghout.write(compact + "\n")
  ghout.write("EOF\n")
