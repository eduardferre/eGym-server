INSERT dbo.exercises (exerciseName, exerciseDescription)
OUTPUT INSERTED.exerciseId
VALUES ('Dead Lift', 'blablabla')

SELECT * FROM dbo.exercises

BEGIN TRANSACTION;
CREATE TABLE #DeletedExerciseIds (exerciseId INT);

DELETE FROM exercises
OUTPUT DELETED.exerciseId INTO #DeletedExerciseIds
WHERE exerciseName='Dead Lift';

SELECT exerciseId FROM #DeletedExerciseIds;
DROP TABLE #DeletedExerciseIds
COMMIT TRANSACTION;

SELECT * FROM dbo.exercises
