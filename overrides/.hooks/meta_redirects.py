"""MkDocs hook that fills out the redirection mapping based on the extra metadata of `.md` files.

Hook adapted based on this GitHub discussion answer:
https://github.com/squidfunk/mkdocs-material/discussions/3758#discussioncomment-4397373
Key difference is that instead of using Context IDs, this hook uses old paths defined in the page meta header.
"""
import logging
from typing import Optional, Dict

from mkdocs.config import Config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page


# region Core Logic

def on_config(config: MkDocsConfig) -> Optional[Config]:
    """Check the `redirects` plugin is present."""

    if "redirects" not in config["plugins"]:
        LOG.error(f"{HOOK_NAME}: The `redirects` plugin isn't in the config")
        return None

    if "redirect_maps" not in config["plugins"]["redirects"].config:
        LOG.error(f"{HOOK_NAME}: The `redirects` plugin isn't correctly configured")
        return None

    return None


def on_page_markdown(*_, page: Page, config: MkDocsConfig, files: Files) -> Optional[str]:
    """Main function. Fill out the redirect mapping."""

    if "old_nav" not in page.meta:
        return None

    src_uri: str = page.file.src_uri

    if len(src_uri.split(".")) > 2:
        LOG.warning(f"{HOOK_NAME}: old_nav in '{src_uri}' won't be processed")
        return None

    redirects: Dict[str, str] = config["plugins"]["redirects"].config["redirect_maps"]

    for nav_entry in page.meta["old_nav"]:
        nav_entry: str

        if not nav_entry.lower().endswith(".md"):
            nav_entry = f'{nav_entry.rstrip("/")}.md'

        if nav_entry in files or nav_entry.replace(".md", "/index.md") in files:
            LOG.error(f"{HOOK_NAME}: The old '{nav_entry}' collides with an existing file")
            continue

        if nav_entry not in redirects:
            redirects[nav_entry] = src_uri
            LOG.info(f"{HOOK_NAME}: Added redirection for '{nav_entry}' to '{redirects[nav_entry]}'")
        elif src_uri != redirects[nav_entry]:
            LOG.error(f"{HOOK_NAME}: The old '{nav_entry}' is already defined in {redirects[nav_entry]}")

    return None

# endregion


# region Constants

HOOK_NAME: str = "meta_redirects"
"""Name of this hook. Used in logging."""

LOG: logging.Logger = logging.getLogger(f"mkdocs.hooks.{HOOK_NAME}")
"""Logger instance for this hook."""

# endregion
