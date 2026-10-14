"""Hook PreToolUse: bloquea comandos de Bash que accedan a ficheros .env.

Las reglas `permissions.deny` cubren las herramientas Read y Edit, pero no Bash:
un `cat .env`, un `grep -r` o un `python -c "open('.env')"` las esquivan. Este
hook cierra esa via.

Deja pasar `.env.example` (plantilla publica, versionada) y `.envrc`.

Limitacion conocida: un comando que lea el fichero sin nombrarlo —por ejemplo un
`grep -r` recursivo sobre todo el repo— no se detecta aqui. Para eso haria falta
aislamiento a nivel de sistema de ficheros (sandbox.filesystem.denyRead).

Entrada: JSON del hook por stdin.
Salida : JSON con permissionDecision=deny si detecta acceso, nada si no.
"""

import json
import re
import sys

# `.env` seguido de algo que no sea punto ni alfanumerico, o fin de cadena.
# Asi `.env.example` y `.envrc` no coinciden.
ENV_PATTERN = re.compile(r"\.env([^.a-zA-Z0-9]|$)")

REASON = (
    "Acceso a .env bloqueado por la politica del proyecto (.claude/settings.json). "
    "Contiene credenciales. Si necesitas un valor, pideselo al usuario; para "
    "cambiar algo, indicale la linea exacta y que la edite el."
)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    command = payload.get("tool_input", {}).get("command", "") or ""

    if ENV_PATTERN.search(command):
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": REASON,
                    }
                }
            )
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
