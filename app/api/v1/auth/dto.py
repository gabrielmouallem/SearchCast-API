class UserDTO:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


class GoogleResponseDTO:
    def __init__(
        self,
        token_type,
        access_token,
        scope,
        login_hint,
        expires_in,
        id_token,
        session_state,
        first_issued_at,
        expires_at,
        idpId,
    ):
        self.token_type = token_type
        self.access_token = access_token
        self.scope = scope
        self.login_hint = login_hint
        self.expires_in = expires_in
        self.id_token = id_token
        self.session_state = session_state
        self.first_issued_at = first_issued_at
        self.expires_at = expires_at
        self.idpId = idpId


class PasswordLoginDTO:
    def __init__(self, email, password):
        self.email = email
        self.password = password


class GoogleLoginDTO:
    def __init__(
        self,
        google_id,
        image_url,
        email,
        name,
        given_name,
        family_name,
        google_response: GoogleResponseDTO,
    ):
        self.googleId = google_id
        self.imageUrl = image_url
        self.email = email
        self.name = name
        self.givenName = given_name
        self.familyName = family_name
        self.google_response = google_response
