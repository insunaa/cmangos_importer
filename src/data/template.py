"""Custom string.Template subclass for SQL generation."""

from __future__ import annotations

from string import Template as _Base

# Shared character GUID injected into every template fill call
char_guid = 500


class Template(_Base):
    """Template that auto-injects ``char_guid`` so callers don't need to pass it manually."""

    def fill(self, **kwds: object) -> str:
        if "no_char_guid" not in kwds:
            kwds["char_guid"] = char_guid

        for k, v in kwds.items():
            if isinstance(v, str):
                kwds[k] = v.rstrip("\n")

        return super().safe_substitute(**kwds)
