VERSION = "5.0.0-dev"
PROJECT_NAME = "capkpi-bench"
CAPKPI_VERSION = None
current_path = None
updated_path = None
LOG_BUFFER = []


def set_capkpi_version(bench_path="."):
	from .utils.app import get_current_capkpi_version

	global CAPKPI_VERSION
	if not CAPKPI_VERSION:
		CAPKPI_VERSION = get_current_capkpi_version(bench_path=bench_path)
