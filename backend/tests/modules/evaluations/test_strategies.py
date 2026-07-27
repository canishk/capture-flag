import pytest

from app.modules.evaluations.domain.strategies import EvaluationStrategyRegistry


def test_exact_match_strategy_passes() -> None:
    registry = EvaluationStrategyRegistry()
    result = registry.evaluate(
        strategy_type=__import__(
            "app.modules.evaluations.domain.enums", fromlist=["EvaluationStrategyType"]
        ).EvaluationStrategyType.EXACT_MATCH,
        answer="flag{test}",
        config={"type": "exact_match", "expectedAnswer": "flag{test}"},
        base_score=100,
    )
    assert result.passed is True
    assert result.score == 100


def test_exact_match_strategy_fails() -> None:
    registry = EvaluationStrategyRegistry()
    result = registry.evaluate(
        strategy_type=__import__(
            "app.modules.evaluations.domain.enums", fromlist=["EvaluationStrategyType"]
        ).EvaluationStrategyType.EXACT_MATCH,
        answer="wrong",
        config={"type": "exact_match", "expectedAnswer": "flag{test}"},
        base_score=100,
    )
    assert result.passed is False
    assert result.score == 0
