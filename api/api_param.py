class API_Param():
    _apiHost = 'https://api.tilko.net/'
    _apiKey = 'a379ba7545364b1a8e5b4c4ee040aef7'

    myUsername = None
    myBirthdate = None
    myCellphoneNumber = None
    myIdentityNumber = None

    def __init__(self, username, birthdate, cellphone, identity):
        self.myUsername = username
        self.myBirthdate = birthdate
        self.myCellphoneNumber = cellphone
        self.myIdentityNumber = identity
