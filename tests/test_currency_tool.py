import pytest

import app.tools.currency_tool as currency_tool_module


class FakeResponse:
    def raise_for_status(self):
        pass

    def json(self):
        return {
            "date": "2026-10-07",
            "base": "INR",
            "quote": "USD",
            "rate": 0.01038,
        }


def test_convert_currency_with_mocked_api(
    monkeypatch,
):
    def fake_get(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr(
        currency_tool_module.httpx,
        "get",
        fake_get,
    )

    result = currency_tool_module.convert_currency(
        30000,
        "INR",
        "USD",
    )

    assert result["original_amount"] == 30000
    assert result["original_currency"] == "INR"
    assert result["converted_currency"] == "USD"
    assert result["converted_amount"] == 311.40
    assert result["rate"] == 0.01038
    assert result["provider"] == "frankfurter"


def test_same_currency_does_not_need_api(
    monkeypatch,
):
    def fail_if_called(*args, **kwargs):
        raise AssertionError(
            "HTTP request should not be made."
        )

    monkeypatch.setattr(
        currency_tool_module.httpx,
        "get",
        fail_if_called,
    )

    result = currency_tool_module.convert_currency(
        30000,
        "INR",
        "INR",
    )

    assert result["converted_amount"] == 30000
    assert result["rate"] == 1.0
    assert result["converted_currency"] == "INR"


def test_currency_codes_are_normalized(
    monkeypatch,
):
    def fake_get(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr(
        currency_tool_module.httpx,
        "get",
        fake_get,
    )

    result = currency_tool_module.convert_currency(
        1000,
        "inr",
        "usd",
    )

    assert result["original_currency"] == "INR"
    assert result["converted_currency"] == "USD"


def test_negative_amount_is_rejected():
    with pytest.raises(
        ValueError,
        match="Amount cannot be negative",
    ):
        currency_tool_module.convert_currency(
            -100,
            "INR",
            "USD",
        )