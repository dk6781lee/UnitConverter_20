import sys
from pathlib import Path

from boundary.cli_app import CliApp
from control.convert_use_case import ConvertUseCase
from control.registry_bootstrap import load_registry_from_config
from entity.conversion_service import ConversionService


def main() -> None:
    stdin = sys.stdin.read()
    config_path = Path(__file__).resolve().parents[2] / "config" / "units.json"
    registry = load_registry_from_config(config_path)
    conversion_service = ConversionService(registry)
    use_case = ConvertUseCase(registry, conversion_service)
    app = CliApp(convert_use_case=use_case, registry=registry)
    stdout, stderr, exit_code = app.run(stdin)
    if stdout:
        print(stdout, end="")
    if stderr:
        print(stderr, end="", file=sys.stderr)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
