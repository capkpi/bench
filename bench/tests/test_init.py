# imports - standard imports
import json
import os
import subprocess
import unittest

# imports - third paty imports
import git

# imports - module imports
from bench.utils import exec_cmd
from bench.app import App
from bench.tests.test_base import CAPKPI_BRANCH, TestBenchBase
from bench.bench import Bench


# changed from capkpi_theme because it wasn't maintained and incompatible,
# chat app & wiki was breaking too. hopefully capkpi_docs will be maintained
# for longer since docs.capkpi.com is powered by it ;)
TEST_CAPKPI_APP = "capkpi_docs"


class TestBenchInit(TestBenchBase):
	def test_utils(self):
		self.assertEqual(subprocess.call("bench"), 0)

	def test_init(self, bench_name="test-bench", **kwargs):
		self.init_bench(bench_name, **kwargs)
		app = App("file:///tmp/capkpi")
		self.assertTupleEqual(
			(app.mount_path, app.url, app.repo, app.org),
			("/tmp/capkpi", "file:///tmp/capkpi", "capkpi", "capkpi"),
		)
		self.assert_folders(bench_name)
		self.assert_virtual_env(bench_name)
		self.assert_config(bench_name)
		test_bench = Bench(bench_name)
		app = App("capkpi", bench=test_bench)
		self.assertEqual(app.from_apps, True)

	def basic(self):
		try:
			self.test_init()
		except Exception:
			print(self.get_traceback())

	def test_multiple_benches(self):
		for bench_name in ("test-bench-1", "test-bench-2"):
			self.init_bench(bench_name)

		self.assert_common_site_config(
			"test-bench-1",
			{
				"webserver_port": 8000,
				"socketio_port": 9000,
				"file_watcher_port": 6787,
				"redis_queue": "redis://localhost:11000",
				"redis_socketio": "redis://localhost:12000",
				"redis_cache": "redis://localhost:13000",
			},
		)

		self.assert_common_site_config(
			"test-bench-2",
			{
				"webserver_port": 8001,
				"socketio_port": 9001,
				"file_watcher_port": 6788,
				"redis_queue": "redis://localhost:11001",
				"redis_socketio": "redis://localhost:12001",
				"redis_cache": "redis://localhost:13001",
			},
		)

	def test_new_site(self):
		bench_name = "test-bench"
		site_name = "test-site.local"
		bench_path = os.path.join(self.benches_path, bench_name)
		site_path = os.path.join(bench_path, "sites", site_name)
		site_config_path = os.path.join(site_path, "site_config.json")

		self.init_bench(bench_name)
		self.new_site(site_name, bench_name)

		self.assertTrue(os.path.exists(site_path))
		self.assertTrue(os.path.exists(os.path.join(site_path, "private", "backups")))
		self.assertTrue(os.path.exists(os.path.join(site_path, "private", "files")))
		self.assertTrue(os.path.exists(os.path.join(site_path, "public", "files")))
		self.assertTrue(os.path.exists(site_config_path))

		with open(site_config_path) as f:
			site_config = json.loads(f.read())

			for key in ("db_name", "db_password"):
				self.assertTrue(key in site_config)
				self.assertTrue(site_config[key])

	def test_get_app(self):
		self.init_bench("test-bench")
		bench_path = os.path.join(self.benches_path, "test-bench")
		exec_cmd(f"bench get-app {TEST_CAPKPI_APP} --skip-assets", cwd=bench_path)
		self.assertTrue(os.path.exists(os.path.join(bench_path, "apps", TEST_CAPKPI_APP)))
		app_installed_in_env = TEST_CAPKPI_APP in subprocess.check_output(
			["bench", "pip", "freeze"], cwd=bench_path
		).decode("utf8")
		self.assertTrue(app_installed_in_env)

	@unittest.skipIf(CAPKPI_BRANCH != "develop", "only for develop branch")
	def test_get_app_resolve_deps(self):
		CAPKPI_APP = "healthcare"
		self.init_bench("test-bench")
		bench_path = os.path.join(self.benches_path, "test-bench")
		exec_cmd(f"bench get-app {CAPKPI_APP} --resolve-deps --skip-assets", cwd=bench_path)
		self.assertTrue(os.path.exists(os.path.join(bench_path, "apps", CAPKPI_APP)))

		states_path = os.path.join(bench_path, "sites", "apps.json")
		self.assertTrue(os.path.exists(states_path))

		with open(states_path) as f:
			states = json.load(f)

		self.assertTrue(CAPKPI_APP in states)

	def test_install_app(self):
		bench_name = "test-bench"
		site_name = "install-app.test"
		bench_path = os.path.join(self.benches_path, "test-bench")

		self.init_bench(bench_name)
		exec_cmd(
			f"bench get-app {TEST_CAPKPI_APP} --branch master --skip-assets", cwd=bench_path
		)

		self.assertTrue(os.path.exists(os.path.join(bench_path, "apps", TEST_CAPKPI_APP)))

		# check if app is installed
		app_installed_in_env = TEST_CAPKPI_APP in subprocess.check_output(
			["bench", "pip", "freeze"], cwd=bench_path
		).decode("utf8")
		self.assertTrue(app_installed_in_env)

		# create and install app on site
		self.new_site(site_name, bench_name)
		installed_app = not exec_cmd(
			f"bench --site {site_name} install-app {TEST_CAPKPI_APP}",
			cwd=bench_path,
			_raise=False,
		)

		if installed_app:
			app_installed_on_site = subprocess.check_output(
				["bench", "--site", site_name, "list-apps"], cwd=bench_path
			).decode("utf8")
			self.assertTrue(TEST_CAPKPI_APP in app_installed_on_site)

	def test_remove_app(self):
		self.init_bench("test-bench")
		bench_path = os.path.join(self.benches_path, "test-bench")

		exec_cmd(
			f"bench get-app {TEST_CAPKPI_APP} --branch master --overwrite --skip-assets",
			cwd=bench_path,
		)
		exec_cmd(f"bench remove-app {TEST_CAPKPI_APP}", cwd=bench_path)

		with open(os.path.join(bench_path, "sites", "apps.txt")) as f:
			self.assertFalse(TEST_CAPKPI_APP in f.read())
		self.assertFalse(
			TEST_CAPKPI_APP
			in subprocess.check_output(["bench", "pip", "freeze"], cwd=bench_path).decode("utf8")
		)
		self.assertFalse(os.path.exists(os.path.join(bench_path, "apps", TEST_CAPKPI_APP)))

	def test_switch_to_branch(self):
		self.init_bench("test-bench")
		bench_path = os.path.join(self.benches_path, "test-bench")
		app_path = os.path.join(bench_path, "apps", "capkpi")

		# * chore: change to 14 when avalible
		prevoius_branch = "version-13"
		if CAPKPI_BRANCH != "develop":
			# assuming we follow `version-#`
			prevoius_branch = f"version-{int(CAPKPI_BRANCH.split('-')[1]) - 1}"

		successful_switch = not exec_cmd(
			f"bench switch-to-branch {prevoius_branch} capkpi --upgrade",
			cwd=bench_path,
			_raise=False,
		)
		if successful_switch:
			app_branch_after_switch = str(git.Repo(path=app_path).active_branch)
			self.assertEqual(prevoius_branch, app_branch_after_switch)

		successful_switch = not exec_cmd(
			f"bench switch-to-branch {CAPKPI_BRANCH} capkpi --upgrade",
			cwd=bench_path,
			_raise=False,
		)
		if successful_switch:
			app_branch_after_second_switch = str(git.Repo(path=app_path).active_branch)
			self.assertEqual(CAPKPI_BRANCH, app_branch_after_second_switch)


if __name__ == "__main__":
	unittest.main()
