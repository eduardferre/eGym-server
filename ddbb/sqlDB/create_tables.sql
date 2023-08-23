USE TestDB
GO

IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' and xtype='U')
    CREATE TABLE dbo.users (
        userId INT PRIMARY KEY IDENTITY(1,1),
        username VARCHAR(255) NOT NULL UNIQUE,
        lastName VARCHAR(255) NOT NULL,
        firstName VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        birthDate DATE NOT NULL
    )
GO

IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='exercises' and xtype='U')
    CREATE TABLE dbo.exercises (
        exerciseId INT PRIMARY KEY IDENTITY(1,1),
        exerciseName VARCHAR(255) NOT NULL UNIQUE,
        exerciseDescription VARCHAR(255)
    )
GO

IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='routines' and xtype='U')
    CREATE TABLE dbo.routines (
        routineId INT PRIMARY KEY IDENTITY(1,1),
        creatorName VARCHAR(255) NOT NULL,
        routineName VARCHAR(255) NOT NULL,
        routineDescription VARCHAR(255),
        routineExerciseId INT FOREIGN KEY REFERENCES exercises(exerciseId)
    )
GO