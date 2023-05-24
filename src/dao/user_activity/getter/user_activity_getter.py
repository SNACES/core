from typing import List

class ActivityGetter:

    def get_user_activities(self, user_id: str) -> List[str]:
        raise NotImplementedError("Subclasses should implement this")
