import re
from typing import Any

from app.modules.evaluations.domain.enums import EvaluationStrategyType
from app.modules.evaluations.domain.exceptions import (
    EvaluationConfigurationError,
    StrategyResult,
    UnsupportedEvaluationStrategyError,
)


class EvaluationStrategyRegistry:
    def evaluate(
        self, strategy_type: EvaluationStrategyType, answer: str, config: dict[str, Any], base_score: int
    ) -> StrategyResult:
        handlers = {
            EvaluationStrategyType.EXACT_MATCH: self._exact_match,
            EvaluationStrategyType.REGEX: self._regex,
            EvaluationStrategyType.NUMERIC_RANGE: self._numeric_range,
        }
        handler = handlers.get(strategy_type)
        if handler is None:
            raise UnsupportedEvaluationStrategyError(strategy_type.value)
        return handler(answer, config, base_score)

    @staticmethod
    def _exact_match(answer: str, config: dict[str, Any], base_score: int) -> StrategyResult:
        expected = config.get("expectedAnswer") or config.get("answer")
        if not expected:
            raise EvaluationConfigurationError("expectedAnswer is required for exact_match")
        submitted = answer
        candidate = str(expected)
        if config.get("trimWhitespace", True):
            submitted = submitted.strip()
            candidate = candidate.strip()
        if not config.get("caseSensitive", False):
            submitted = submitted.lower()
            candidate = candidate.lower()
        passed = submitted == candidate
        return StrategyResult(
            passed=passed,
            score=base_score if passed else 0,
            feedback="Correct!" if passed else "Incorrect. Review the challenge and try again.",
        )

    @staticmethod
    def _regex(answer: str, config: dict[str, Any], base_score: int) -> StrategyResult:
        pattern = config.get("pattern")
        if not pattern:
            raise EvaluationConfigurationError("pattern is required for regex strategy")
        flags = 0
        if config.get("ignoreCase", True):
            flags |= re.IGNORECASE
        passed = re.fullmatch(pattern, answer.strip(), flags) is not None
        return StrategyResult(
            passed=passed,
            score=base_score if passed else 0,
            feedback="Correct!" if passed else "Answer format does not match the expected pattern.",
        )

    @staticmethod
    def _numeric_range(answer: str, config: dict[str, Any], base_score: int) -> StrategyResult:
        try:
            value = float(answer.strip())
        except ValueError as exc:
            raise EvaluationConfigurationError("Answer must be numeric") from exc
        minimum = config.get("min")
        maximum = config.get("max")
        if minimum is None or maximum is None:
            raise EvaluationConfigurationError("min and max are required for numeric_range")
        passed = float(minimum) <= value <= float(maximum)
        return StrategyResult(
            passed=passed,
            score=base_score if passed else 0,
            feedback="Correct!" if passed else "Value is outside the expected range.",
        )
