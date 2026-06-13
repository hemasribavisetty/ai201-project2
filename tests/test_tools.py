import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from tools import (
    search_listings,
    suggest_outfit,
    create_fit_card,
)
from utils.data_loader import (
    get_example_wardrobe,
    get_empty_wardrobe,
)


def test_search_returns_results():
    results = search_listings(
        "vintage graphic tee",
        size=None,
        max_price=50,
    )

    assert isinstance(results, list)
    assert len(results) > 0


def test_search_empty_results():
    results = search_listings(
        "designer ballgown",
        size="XXS",
        max_price=5,
    )

    assert results == []


def test_search_price_filter():
    results = search_listings(
        "tee",
        size=None,
        max_price=20,
    )

    assert all(item["price"] <= 20 for item in results)


def test_suggest_outfit_empty_wardrobe():
    item = search_listings(
        "vintage graphic tee",
        None,
        50,
    )[0]

    outfit = suggest_outfit(
        item,
        get_empty_wardrobe(),
    )

    assert isinstance(outfit, str)
    assert len(outfit) > 0


def test_fit_card_empty_outfit():
    item = search_listings(
        "vintage graphic tee",
        None,
        50,
    )[0]

    result = create_fit_card("", item)

    assert "outfit" in result.lower()