import argparse
import importlib.metadata
import json
from pathlib import Path
from typing import Any, Dict, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


def get_version() -> str:
    """Dynamically reads the version from pyproject.toml via package metadata."""
    try:
        return importlib.metadata.version("pokemon-engine")
    except importlib.metadata.PackageNotFoundError:
        # Fallback for development if the package isn't pip installed yet
        return "0.0.0-dev"


def json_config_settings_source() -> Dict[str, Any]:
    """Reads the production baseline config.json."""
    config_file = Path("config.json")
    if config_file.exists():
        with open(config_file, "r") as f:
            return json.load(f)
    return {}


class AppConfig(BaseSettings):
    """
    Strictly-typed application configuration.
    Hierarchy of Truth: CLI Args > .env > config.json > defaults
    """
    # From config.json (Production Baseline)
    initial_state: str = "MainMenuState"
    target_fps: int = 60
    log_level: str = "INFO"

    # From .env (Developer Overrides)
    debug_mode: bool = False
    override_log_level: Optional[str] = None
    override_initial_state: Optional[str] = None

    # Dynamic from pyproject.toml
    version: str = get_version()

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        # Insert the JSON configuration source at the lowest priority (below .env)
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            json_config_settings_source,
            file_secret_settings,
        )


def load_environment() -> AppConfig:
    """
    Parses CLI arguments via argparse and passes them directly to AppConfig.
    These explicit CLI arguments have the absolute highest priority.
    """
    parser = argparse.ArgumentParser(description="Pokemon Engine Bootstrapper")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--state", type=str, help="Override initial state (e.g. BattleState)")
    parser.add_argument("--log-level", type=str, help="Override default logging verbosity")
    
    args, unknown = parser.parse_known_args()

    # We only pass values to Pydantic if the user actually supplied them via CLI.
    # Otherwise, Pydantic will fall back to .env or config.json.
    cli_overrides = {}
    if args.debug:
        cli_overrides["debug_mode"] = True
    if args.state:
        cli_overrides["override_initial_state"] = args.state
    if args.log_level:
        cli_overrides["override_log_level"] = args.log_level

    return AppConfig(**cli_overrides)
