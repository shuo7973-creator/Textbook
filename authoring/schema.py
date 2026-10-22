from dataclasses import dataclass


@dataclass
class Chapter:
    number: int
    title: str
    prerequisites: str
    goals: list[str]
    body: str
    reading: str
    lab: str
    exercises: list[tuple[str, str, str]]

    def validate(self):
        assert 2 <= self.number <= 40
        assert len(self.goals) >= 5
        assert len(self.exercises) == 8
        assert len(self.body) > 900, (self.number, "正文不足")
        assert all(all(x.strip() for x in item) for item in self.exercises)
        compile(self.lab, f"ch{self.number:02d}_lab", "exec")
