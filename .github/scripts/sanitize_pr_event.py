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
import urllib.request
import urllib.error

GITHUB_EVENT_PATH = os.environ.get("GITHUB_EVENT_PATH")
REPO = os.environ.get("GITHUB_REPOSITORY")
TOKEN = os.environ.get("GITHUB_TOKEN")
PR_NUMBER = os.environ.get("PR_NUMBER")

if not GITHUB_EVENT_PATH or not REPO or not TOKEN or not PR_NUMBER:
    print("Missing env vars", file=sys.stderr)
    sys.exit(1)

with open(GITHUB_EVENT_PATH, 'r', encoding='utf-8') as f:
    event = json.load(f)

pr = event.get('pull_request', {})

def redact(s):
    if s is None:
        return None
    s = re.sub(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', '[REDACTED_EMAIL]', s)
    s = re.sub(r'https?://[^\s]+', '[REDACTED_URL]', s)
    # remove long sequences of whitespace
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def trunc(s, n=1000):
    if s is None:
        return None
    return s if len(s) <= n else f"{s[:n]}...[TRUNCATED]"

# Basic sanitized object
sanitized = {
    "pr_number": pr.get("number"),
    "title": trunc(redact(pr.get("title")), 400),
    "body": trunc(redact(pr.get("body")), 1200),
    "author": pr.get("user", {}).get("login"),
    "head_sha": pr.get("head", {}).get("sha"),
    "head_ref": pr.get("head", {}).get("ref"),
    "base_ref": pr.get("base", {}).get("ref"),
    "html_url": pr.get("html_url"),
    "repository": REPO,
    "files": []
}

# Fetch PR files via GitHub API (limited)
api_url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/files"
headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "sanitizer-script"
}

files = []
try:
    req = urllib.request.Request(api_url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        files = json.load(resp)
except urllib.error.HTTPError as e:
    # HTTP errors (401, 403, 404, etc.)
    files = []
    sanitized["files_fetch_error"] = f"HTTP {e.code}: {str(e)[:200]}"
except urllib.error.URLError as e:
    # Network errors
    files = []
    sanitized["files_fetch_error"] = f"Network error: {str(e)[:200]}"
except json.JSONDecodeError as e:
    # JSON parsing errors
    files = []
    sanitized["files_fetch_error"] = f"JSON error: {str(e)[:200]}"

MAX_FILES = 8
MAX_PATCH_LEN = 2000  # chars per file
included = 0
for f in files:
    if included >= MAX_FILES:
        break
    filename = f.get('filename')
    patch = f.get('patch') or ''
    # Keep only added/removed lines to reduce user-controlled content
    only_changes = '\n'.join([ln for ln in patch.splitlines() if ln and (ln.startswith('+') or ln.startswith('-'))])
    only_changes = redact(only_changes)
    if len(only_changes) > MAX_PATCH_LEN:
        only_changes = only_changes[:MAX_PATCH_LEN] + '\n...[TRUNCATED]'
    sanitized["files"].append({
        "filename": filename,
        "status": f.get('status'),
        "changes": min(f.get('changes', 0), 9999),
        "patch_excerpt": only_changes
    })
    included += 1

# Convert to compact JSON
compact = json.dumps(sanitized, ensure_ascii=False)

# Write artifact file for audit
with open('sanitized.json', 'w', encoding='utf-8') as out:
    json.dump(sanitized, out, ensure_ascii=False, indent=2)

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
