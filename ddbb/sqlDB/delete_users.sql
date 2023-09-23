DELETE FROM dbo.users
OUTPUT DELETED.*
WHERE username='ddd'