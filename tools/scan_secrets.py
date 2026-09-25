"""Offline publication gate. Prints locations/types only, never matched values."""
import argparse, json, re, sys
from pathlib import Path

RULES = {
 'private_key': r'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----',
 'github_token': r'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,})\b',
 'huggingface_token': r'\bhf_[A-Za-z0-9]{20,}\b',
 'openai_style_key': r'\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{20,}\b',
 'aws_access_id': r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b',
 'google_api_key': r'\bAIza[A-Za-z0-9_-]{30,}\b',
 'slack_token': r'\bxox[baprs]-[A-Za-z0-9-]{15,}\b',
 'jwt': r'\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b',
 'credential_in_url': r'https?://[^\s/:]+:[^\s/@]+@',
 'assigned_credential': r'''(?i)\b(?:api[_-]?key|access[_-]?token|auth[_-]?token|secret[_-]?key|password|passwd|client[_-]?secret)\b["']?\s*[:=]\s*["'][^"'\r\n]{8,}["']''',
 'bearer_credential': r'(?i)\bBearer\s+[A-Za-z0-9_.-]{20,}',
}

def scan(root):
 findings=[]; checked=0
 for p in sorted(root.rglob('*')):
  if not p.is_file() or '.git' in p.relative_to(root).parts: continue
  if p.suffix in ('.safetensors','.bin','.pt','.pth','.gguf'):continue
  try: text=p.read_text(encoding='utf-8-sig')
  except UnicodeError:
   findings.append({'path':p.relative_to(root).as_posix(),'type':'unscannable_non_utf8'});continue
  checked+=1
  if p.name=='.env' or p.name.startswith('.env.'):
   findings.append({'path':p.relative_to(root).as_posix(),'type':'environment_file'})
  for kind,pattern in RULES.items():
   for match in re.finditer(pattern,text):
    findings.append({'path':p.relative_to(root).as_posix(),'line':text.count('\n',0,match.start())+1,'type':kind})
 return {'files_scanned':checked,'findings':findings,'method':'offline regex signatures and assigned credentials; not a guarantee of absence'}

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);ap.add_argument('--report',type=Path);a=ap.parse_args()
 result=scan(a.root);body=json.dumps(result,ensure_ascii=False,indent=2)
 if a.report:a.report.write_text(body+'\n',encoding='utf-8')
 print(body);sys.exit(bool(result['findings']))
