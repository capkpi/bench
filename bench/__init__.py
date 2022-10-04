VERSION = "5.14.3"
PROJECT_NAME = "capkpi-bench"
FRAPPE_VERSION = None
current_path = None
updated_path = None
LOG_BUFFER = []


def set_capkpi_version(bench_path="."):
	from .utils.app import get_current_capkpi_version

	global FRAPPE_VERSION
	if not FRAPPE_VERSION:
		FRAPPE_VERSION = get_current_capkpi_version(bench_path=bench_path)
