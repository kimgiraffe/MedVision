class API_Param():
    _apiHost = 'https://api.tilko.net/'
    _apiKey = 'd826bc51673f456c960e4b30e2ef08f8'

    myUsername = None
    myBirthdate = None
    myCellphoneNumber = None
    myIdentityNumber = None

    def __init__(self, username, birthdate, cellphone, identity):
        self.myUsername = username
        self.myBirthdate = birthdate
        self.myCellphoneNumber = cellphone
        self.myIdentityNumber = identity
