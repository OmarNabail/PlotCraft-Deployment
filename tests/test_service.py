import pytest

from src.plotcraft.service import (
    _remove_markdown_fences,
    generate_plot_code,
)


def test_generate_plot_code_returns_python_code():
    result = generate_plot_code("Create a bar chart")

    assert isinstance(result, str)
    assert "matplotlib" in result
    assert "plt.bar" in result


def test_generate_plot_code_rejects_empty_prompt():
    with pytest.raises(
        ValueError,
        match="Please enter a plotting request",
    ):
        generate_plot_code("   ")


def test_remove_markdown_fences():
    result = _remove_markdown_fences("```python\nprint('plot')\n```")

    assert result == "print('plot')"
