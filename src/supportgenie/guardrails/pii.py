"""Detect and redact personally identifiable information (PII)."""

from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

_analyzer = AnalyzerEngine()
_anonymizer = AnonymizerEngine()


def redact_pii(text):
    findings = _analyzer.analyze(text=text, language="en")
    result = _anonymizer.anonymize(text=text, analyzer_results=findings)
    return result.text


def find_pii(text):
    findings = _analyzer.analyze(text=text, language="en")
    return [(f.entity_type, text[f.start:f.end]) for f in findings]