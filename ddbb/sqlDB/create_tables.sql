USE TestDB
GO

IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' and xtype='U')
    CREATE TABLE dbo.users (
        id INT PRIMARY KEY IDENTITY(1,1),
        username VARCHAR(255) NOT NULL UNIQUE,
        firstName VARCHAR(255) NOT NULL,
        lastName VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        birthDate DATE NOT NULL
    )
GO

IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='exercises' and xtype='U')
    CREATE TABLE dbo.exercises (
        id INT PRIMARY KEY IDENTITY(1,1),
        creator VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL UNIQUE,
        description VARCHAR(255)
    )
GO

IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='routines' and xtype='U')
    CREATE TABLE dbo.routines (
        id INT PRIMARY KEY IDENTITY(1,1),
        creator VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        description VARCHAR(255)
    )
GO

IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='relationRoutinesExercises' and xtype='U')
    CREATE TABLE dbo.relationRoutinesExercises (
        routineId INT NOT NULL,
        exerciseId INT NOT NULL,

        FOREIGN KEY (routineId) REFERENCES dbo.routines(id),
        FOREIGN KEY (exerciseId) REFERENCES dbo.exercises(id),
        UNIQUE (routineId, exerciseId)
    )