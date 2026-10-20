"""Tests for BaseBuilder's abstract fallback contract."""

import pytest

from sae.kernel.builders.base_builder import BaseBuilder


class DelegatingBuilder(BaseBuilder[int]):
    """Concrete test builder that delegates to abstract fallbacks."""

    def build(self) -> int:
        return super().build()

    def reset(self) -> None:
        super().reset()


def test_base_builder_build_fallback_raises_not_implemented() -> None:
    """The abstract build fallback must never provide a result."""
    with pytest.raises(NotImplementedError):
        DelegatingBuilder().build()


def test_base_builder_reset_fallback_raises_not_implemented() -> None:
    """The abstract reset fallback must not silently do nothing."""
    with pytest.raises(NotImplementedError):
        DelegatingBuilder().reset()
