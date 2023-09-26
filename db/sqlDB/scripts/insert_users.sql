-- DELETE FROM dbo.users

INSERT dbo.users (username, firstName, lastName, email, password, birthDate)
OUTPUT INSERTED.*
VALUES ('eduardferreee', 'Eduard', 'Ferre', 'eduard@gmail.com', 'edu', '2000-04-07')

SELECT * FROM dbo.users