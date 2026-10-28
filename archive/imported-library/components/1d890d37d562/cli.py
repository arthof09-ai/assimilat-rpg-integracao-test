"""Offline CLI: python cli.py snapshot.json pedido.json --safe|--master."""
import json
import sys
from pathlib import Path
from levelup_engine import InvalidPlan, plan_level_up, player_safe_report


def main():
    if len(sys.argv) not in (3, 4) or (len(sys.argv) == 4 and sys.argv[3] not in ('--safe', '--master')):
        raise SystemExit('Uso: python cli.py snapshot.json pedido.json [--safe|--master]')
    try:
        snapshot = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
        request = json.loads(Path(sys.argv[2]).read_text(encoding='utf-8'))
        preview = plan_level_up(snapshot, request)
        out = player_safe_report(preview) if len(sys.argv) == 4 and sys.argv[3] == '--safe' else preview
    except (InvalidPlan, ValueError) as exc:
        print(json.dumps({'status': 'BLOCKED_NO_WRITE', 'reason': str(exc)}, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
