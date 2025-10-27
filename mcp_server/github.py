"""
Helpers for GitHub webhook handling for the PromptToProduct repository.
This module intentionally avoids external dependencies so the MCP server can run with only the Python standard library.
"""
import hmac
import hashlib
import json
import datetime
from .config import is_valid_repo, get_config


def verify_signature(secret: bytes, signature_header: str, body: bytes) -> bool:
    """Verify GitHub HMAC-SHA256 signature (X-Hub-Signature-256).
    If no signature_header provided, returns False.
   """
    if not signature_header or not secret:
        return False
    if signature_header.startswith('sha256='):
        sig = signature_header.split('=', 1)[1]
    else:
        return False
    mac = hmac.new(secret, msg=body, digestmod=hashlib.sha256)
    expected = mac.hexdigest()
    return hmac.compare_digest(expected, sig)


def handle_github_event(headers: dict, payload: dict, raw_body: bytes) -> dict:
    """Process the incoming GitHub webhook for PromptToProduct repository.
    Returns a detailed dict describing what was received and processed.
    Verification is optional; provide GITHUB_WEBHOOK_SECRET env var for strict checking.
   """
    event = headers.get('X-GitHub-Event') or headers.get('x-github-event')
    delivery = headers.get('X-GitHub-Delivery') or headers.get('x-github-delivery')
    sig = headers.get('X-Hub-Signature-256') or headers.get('x-hub-signature-256')

    # Parse repository information
    repo = None
    action = None
    sender = None
    try:
        if isinstance(payload, dict):
            repo_data = payload.get('repository', {})
            repo = repo_data.get('full_name')
            action = payload.get('action')
            sender_data = payload.get('sender', {})
            sender = sender_data.get('login')
    except Exception:
        pass

    # Validate this is for our expected repository
    repo_valid = is_valid_repo(repo) if repo else False
    
    config = get_config()
    
    result = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'event': event,
        'delivery': delivery,
        'repo': repo,
        'repo_valid': repo_valid,
        'action': action,
        'sender': sender,
        'signature_present': bool(sig),
        'processed': False,
        'error': None
    }

    # Repository validation
    if not repo_valid:
        result['error'] = f'Invalid repository: {repo}. Expected: {config["repo"]["full_name"]}'
        return result

    # Signature verification
    secret_value = config.get('github_webhook_secret')
    if secret_value:
        sig_ok = verify_signature(secret_value.encode('utf-8'), sig or '', raw_body or b'')
        result['signature_verified'] = bool(sig_ok)
        if not sig_ok:
            result['error'] = 'Invalid webhook signature'
            return result
    else:
        result['signature_verified'] = 'no-secret-configured'

    # Process specific events for PromptToProduct
    try:
        if event == 'push':
            result.update(handle_push_event(payload))
        elif event == 'pull_request':
            result.update(handle_pull_request_event(payload))
        elif event == 'issues':
            result.update(handle_issues_event(payload))
        elif event == 'issue_comment':
            result.update(handle_issue_comment_event(payload))
        else:
            result['info'] = f'Event {event} received but not specifically handled'
        
        result['processed'] = True
    except Exception as e:
        result['error'] = f'Error processing {event} event: {str(e)}'

    return result


def handle_push_event(payload: dict) -> dict:
    """Handle push events to the PromptToProduct repository."""
    branch = payload.get('ref', '').replace('refs/heads/', '')
    commits = payload.get('commits', [])
    pusher = payload.get('pusher', {}).get('name')
    
    return {
        'event_data': {
            'branch': branch,
            'commit_count': len(commits),
            'pusher': pusher,
            'head_commit': payload.get('head_commit', {}).get('id', '')[:8] if payload.get('head_commit') else None
        }
    }


def handle_pull_request_event(payload: dict) -> dict:
    """Handle pull request events."""
    pr = payload.get('pull_request', {})
    return {
        'event_data': {
            'pr_number': pr.get('number'),
            'pr_title': pr.get('title'),
            'pr_state': pr.get('state'),
            'pr_author': pr.get('user', {}).get('login'),
            'base_branch': pr.get('base', {}).get('ref'),
            'head_branch': pr.get('head', {}).get('ref')
        }
    }


def handle_issues_event(payload: dict) -> dict:
    """Handle issues events."""
    issue = payload.get('issue', {})
    return {
        'event_data': {
            'issue_number': issue.get('number'),
            'issue_title': issue.get('title'),
            'issue_state': issue.get('state'),
            'issue_author': issue.get('user', {}).get('login'),
            'labels': [label.get('name') for label in issue.get('labels', [])]
        }
    }


def handle_issue_comment_event(payload: dict) -> dict:
    """Handle issue comment events."""
    issue = payload.get('issue', {})
    comment = payload.get('comment', {})
    return {
        'event_data': {
            'issue_number': issue.get('number'),
            'comment_author': comment.get('user', {}).get('login'),
            'comment_id': comment.get('id'),
            'comment_body_length': len(comment.get('body', ''))
        }
    }
