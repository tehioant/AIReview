from dataclasses import dataclass

@dataclass
class ReviewComment:
    file_path: str
    line: int
    content: str
    type: str  # 'naming', 'style', 'indentation', 'documentation', 'test_coverage'