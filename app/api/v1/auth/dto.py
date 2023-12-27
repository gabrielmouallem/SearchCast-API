class UserDTO:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


class GoogleResponseDTO:
    def __init__(
        self,
        access_token,
        token_type,
        expires_in,
        scope,
        authuser,
        prompt,
    ):
        self.access_token = access_token
        self.token_type = token_type
        self.expires_in = expires_in
        self.scope = scope
        self.authuser = authuser
        self.prompt = prompt


class PasswordLoginDTO:
    def __init__(self, email, password):
        self.email = email
        self.password = password


class GoogleLoginDTO:
    def __init__(self, name, picture, family_name, given_name, email, id_token):
        self.name = name
        self.picture = picture
        self.family_name = family_name
        self.given_name = given_name
        self.email = email
        self.id_token = id_token
