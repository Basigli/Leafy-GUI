CREATE TABLE STAGES(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	presetId INTEGER NOT NULL,
	stageNumber INTEGER NOT NULL,
	isTemp INTEGER NOT NULL,
	startDate DATETIME NOT NULL,
	endDate DATETIME NOT NULL,
	parameterName TEXT NOT NULL,
	lowSetpoint INTEGER NOT NULL,
	highSetpoint INTEGER NOT NULL
)