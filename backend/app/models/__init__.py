"""Models package initialization."""
from .requests import (
    GenerateTestsRequest,
    TestResult,
    MappingInfo,
    AISuggestion,
    MappingResult,
    CustomTestRequest
)
from .responses import (
    TestSummary,
    ConfigTableSummary,
    GenerateTestsResponse,
    ConfigTableResponse,
    HealthResponse
)

__all__ = [
    "GenerateTestsRequest",
    "TestResult",
    "MappingInfo",
    "AISuggestion",
    "MappingResult",
    "CustomTestRequest",
    "TestSummary",
    "ConfigTableSummary",
    "GenerateTestsResponse",
    "ConfigTableResponse",
    "HealthResponse"
]
