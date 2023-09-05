from frwk.framework.configurations.base import TagConfig

VERSION = '2.0.7'

# Tables
LOG_TABLE = 'frwk_Log'

DEFAULTS = {
	# Db
	'dataConnection': 'IgnitionDATA',
	# Perspective
	'rightDockName': 'rightDock',
	'rightDockHistoryName': 'rightDockHistory',
	# Version
	'version': VERSION,
	# Gateway
	'auditProfile': 'AuditLog',
	'alarmJournal': 'AlarmJournal',
	'cpuAlarmThresholdTag': '[default]DiagnosticConfig/Performance/CPU/MaxValue',
	'cpuAlarmDelayTag': '[default]DiagnosticConfig/Performance/CPU/Delay',
	'memoryAlarmThresholdTag': '[default]DiagnosticConfig/Performance/Memory/MaxValue',
	'memoryAlarmDelayTag': '[default]DiagnosticConfig/Performance/Memory/Delay',
}
BASE_PATH = '[default]FRWK/Framework/Config'

CONFIG = TagConfig(DEFAULTS, BASE_PATH)