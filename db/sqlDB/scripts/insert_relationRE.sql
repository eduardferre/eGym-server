BEGIN TRANSACTION
INSERT dbo.relationRoutinesExercises (routineId, exerciseId)
VALUES (N'c425bb78-65a4-4e4e-85bb-cea34e7f5587', N'56f01d29-167c-4589-9694-7e5e9c96802e')

INSERT dbo.relationRoutinesExercises (routineId, exerciseId)
VALUES (1, 2)

INSERT dbo.relationRoutinesExercises (routineId, exerciseId)
VALUES (1, 4)
SELECT * FROM dbo.relationRoutinesExercises

COMMIT TRANSACTION