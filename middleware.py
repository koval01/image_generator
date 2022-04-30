class Validator(object):
    @staticmethod
    def validate_profile(profile: dict) -> str or None:
        response = "%s field is incorrect"
        if 2 > len(profile["name"]) > 26:
            return response % "name"
        if 12 > profile["age"] > 100:
            return response % "age"
        if 2 > len(profile["city"]) >= 32:
            return response % "city"
        if len(profile["description"]) >= 2048:
            return response % "description"
        return

    @staticmethod
    def fix_desc(profile: dict) -> dict:
        try:
            profile["description"]
        except:
            profile["description"] = ""
        return profile
