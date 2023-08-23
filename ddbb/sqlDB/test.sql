DELETE FROM dbo.exercises

INSERT dbo.exercises (exerciseName, exerciseDescription)
OUTPUT INSERTED.exerciseId
VALUES ('Dead Lift', 'blablabla')

SELECT * FROM dbo.exercises

DELETE FROM dbo.exercises
OUTPUT DELETED.exerciseId
WHERE exerciseName='DeadLift'

SELECT * FROM dbo.exercises
