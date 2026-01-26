import json
import time
from typing import Optional
import anthropic

from ..config import get_settings
from ..models.schemas import ClaudeAnalysisResult, ClaudeIssue
from ..utils.prompts import ANALYSIS_SYSTEM_PROMPT, build_analysis_prompt

settings = get_settings()


class AnalyzerService:
    def __init__(self):
        self.client = None
        if settings.anthropic_api_key:
            self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    async def analyze_diff(
        self,
        repo: str,
        pr_title: str,
        author: str,
        diff: str
    ) -> tuple[ClaudeAnalysisResult, int, int]:
        """
        Analyze a PR diff using Claude.

        Returns:
            tuple: (analysis_result, analysis_time_ms, tokens_used)
        """
        if not self.client:
            # Return empty result if no API key configured
            return ClaudeAnalysisResult(issues=[], summary="API key not configured"), 0, 0

        start_time = time.time()

        user_prompt = build_analysis_prompt(repo, pr_title, author, diff)

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                system=ANALYSIS_SYSTEM_PROMPT,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            analysis_time_ms = int((time.time() - start_time) * 1000)
            tokens_used = message.usage.input_tokens + message.usage.output_tokens

            # Parse response
            response_text = message.content[0].text
            result = self._parse_response(response_text)

            return result, analysis_time_ms, tokens_used

        except anthropic.APIError as e:
            print(f"Claude API error: {e}")
            return ClaudeAnalysisResult(
                issues=[],
                summary=f"Analysis failed: {str(e)}"
            ), 0, 0

    def _parse_response(self, response_text: str) -> ClaudeAnalysisResult:
        """Parse Claude's JSON response into structured result."""
        try:
            # Try to extract JSON from response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1

            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                data = json.loads(json_str)

                issues = []
                for issue_data in data.get("issues", []):
                    try:
                        issue = ClaudeIssue(
                            category=issue_data.get("category", "quality"),
                            severity=issue_data.get("severity", "suggestion"),
                            file_path=issue_data.get("file_path", "unknown"),
                            line_number=issue_data.get("line_number"),
                            title=issue_data.get("title", "Issue found"),
                            message=issue_data.get("message", ""),
                            explanation=issue_data.get("explanation"),
                            suggestion=issue_data.get("suggestion"),
                        )
                        issues.append(issue)
                    except Exception as e:
                        print(f"Error parsing issue: {e}")
                        continue

                return ClaudeAnalysisResult(
                    issues=issues,
                    summary=data.get("summary"),
                    has_tests=data.get("has_tests", False),
                    overall_quality=data.get("overall_quality"),
                )

            return ClaudeAnalysisResult(issues=[], summary="Could not parse response")

        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
            return ClaudeAnalysisResult(issues=[], summary="Invalid JSON response")


# Singleton instance
analyzer_service = AnalyzerService()


def get_analyzer_service() -> AnalyzerService:
    return analyzer_service
