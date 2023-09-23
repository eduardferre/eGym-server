SELECT * FROM dbo.users
WHERE username='eduardferre'

UPDATE dbo.users
SET username = 'eduardferre', firstName = 'edu', lastName = 'ferre', email = 'edu', password = 'edu', birthDate = '2000-07-04'
OUTPUT INSERTED.*
WHERE userId=8