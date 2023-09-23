INSERT dbo.exercises (creator, name, description)
OUTPUT INSERTED.id
VALUES ('eduardferre', 'Dead Lift', '')

INSERT dbo.exercises (creator, name, description)
OUTPUT INSERTED.id
VALUES ('eduardferre', 'Bench Press', '')

INSERT dbo.exercises (creator, name, description)
OUTPUT INSERTED.id
VALUES ('eduardferre', 'Low-bar Squad', '')

SELECT * FROM dbo.exercises

SELECT * FROM dbo.relationRoutinesExercises