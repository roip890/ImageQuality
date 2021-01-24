from enum import Enum


class Experts(Enum):
    All = -2
    Random = -1
    Beginner = 0
    Medium = 1
    Expert = 2

    @staticmethod
    def expert_value_to_enum(value):
        if value == 0:
            return Experts.Beginner
        elif value == 1:
            return Experts.Medium
        elif value == 2:
            return Experts.Expert
        return None

    @staticmethod
    def expert_price(expert):
        if expert == Experts.Beginner:
            return 2
        elif expert == Experts.Medium:
            return 6
        elif expert == Experts.Expert:
            return 12
        return 1
