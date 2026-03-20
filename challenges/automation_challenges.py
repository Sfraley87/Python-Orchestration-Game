"""Automation & scripting challenges."""

AUTOMATION_CHALLENGES = [
    {
        "id": "auto-001",
        "category": "automation",
        "difficulty": "easy",
        "title": "Find Files by Extension",
        "description": (
            "Write a function `find_files(directory, extension)` that returns a\n"
            "sorted list of all file paths in `directory` (recursively) that match\n"
            "the given extension (e.g. '.py', '.log').\n\n"
            "Use pathlib. Return absolute string paths, sorted alphabetically."
        ),
        "starter_code": (
            "from pathlib import Path\n\n"
            "def find_files(directory: str, extension: str) -> list[str]:\n"
            "    # TODO: recursively find all files with given extension\n"
            "    # Return sorted list of absolute string paths\n"
            "    pass\n"
        ),
        "setup_code": (
            "import tempfile, os\n"
            "from pathlib import Path\n\n"
            "_tmp = tempfile.mkdtemp()\n"
            "Path(_tmp, 'a.py').write_text('x')\n"
            "Path(_tmp, 'b.py').write_text('x')\n"
            "Path(_tmp, 'c.txt').write_text('x')\n"
            "sub = Path(_tmp, 'sub')\n"
            "sub.mkdir()\n"
            "(sub / 'd.py').write_text('x')\n"
        ),
        "tests": [
            {
                "description": "Finds all .py files recursively",
                "assert_code": (
                    "result = find_files(_tmp, '.py')\n"
                    "assert len(result) == 3, f'Expected 3 .py files, got {len(result)}: {result}'\n"
                    "assert all(r.endswith('.py') for r in result), f'Non-.py in results: {result}'"
                ),
            },
            {
                "description": "Returns sorted list",
                "assert_code": (
                    "result = find_files(_tmp, '.py')\n"
                    "assert result == sorted(result), f'Not sorted: {result}'"
                ),
            },
            {
                "description": "Returns empty list when no matches",
                "assert_code": (
                    "result = find_files(_tmp, '.csv')\n"
                    "assert result == [], f'Expected [], got {result}'"
                ),
            },
        ],
        "hints": [
            "Use Path(directory).rglob(f'*{extension}') to find files recursively.",
            "Use sorted() and str() to return sorted string paths.",
        ],
        "solution": (
            "from pathlib import Path\n\n"
            "def find_files(directory: str, extension: str) -> list[str]:\n"
            "    return sorted(str(p) for p in Path(directory).rglob(f'*{extension}'))\n"
        ),
    },
    {
        "id": "auto-002",
        "category": "automation",
        "difficulty": "easy",
        "title": "Parse a Config File",
        "description": (
            "Write a function `load_config(text)` that parses a simple INI-style\n"
            "config string and returns a nested dict.\n\n"
            "Format:\n"
            "  [section]\n"
            "  key = value\n\n"
            "Example input:\n"
            "  '[server]\\nhost = localhost\\nport = 8080\\n[db]\\nname = mydb'\n"
            "Expected output:\n"
            "  {'server': {'host': 'localhost', 'port': '8080'}, 'db': {'name': 'mydb'}}"
        ),
        "starter_code": (
            "def load_config(text: str) -> dict:\n"
            "    # TODO: parse INI-style config text into nested dict\n"
            "    # Sections are [name], keys are 'key = value'\n"
            "    # Values are always strings\n"
            "    pass\n"
        ),
        "tests": [
            {
                "description": "Parses sections and key-value pairs",
                "assert_code": (
                    "text = '[server]\\nhost = localhost\\nport = 8080\\n[db]\\nname = mydb'\n"
                    "result = load_config(text)\n"
                    "expected = {'server': {'host': 'localhost', 'port': '8080'}, 'db': {'name': 'mydb'}}\n"
                    "assert result == expected, f'Got {result}'"
                ),
            },
            {
                "description": "Handles extra whitespace",
                "assert_code": (
                    "text = '[app]\\n  debug = true  \\n  version = 1.2  '\n"
                    "result = load_config(text)\n"
                    "assert result == {'app': {'debug': 'true', 'version': '1.2'}}, f'Got {result}'"
                ),
            },
        ],
        "hints": [
            "Iterate line by line. Use line.startswith('[') to detect sections.",
            "Use line.split('=', 1) to split key-value pairs. Strip whitespace from both sides.",
        ],
        "solution": (
            "def load_config(text: str) -> dict:\n"
            "    config = {}\n"
            "    current = None\n"
            "    for line in text.splitlines():\n"
            "        line = line.strip()\n"
            "        if not line:\n"
            "            continue\n"
            "        if line.startswith('[') and line.endswith(']'):\n"
            "            current = line[1:-1]\n"
            "            config[current] = {}\n"
            "        elif '=' in line and current:\n"
            "            k, v = line.split('=', 1)\n"
            "            config[current][k.strip()] = v.strip()\n"
            "    return config\n"
        ),
    },
    {
        "id": "auto-003",
        "category": "automation",
        "difficulty": "medium",
        "title": "Batch Rename Files",
        "description": (
            "Write a function `batch_rename(directory, pattern, replacement)` that\n"
            "renames all files in `directory` (non-recursive) by replacing `pattern`\n"
            "in the filename with `replacement`. Return a list of (old_name, new_name)\n"
            "tuples for files that were actually renamed.\n\n"
            "Example: batch_rename('/logs', 'error_', 'err_')\n"
            "  'error_2024.log' → 'err_2024.log'"
        ),
        "setup_code": (
            "import tempfile\n"
            "from pathlib import Path\n\n"
            "_tmp = tempfile.mkdtemp()\n"
            "for name in ['error_01.log', 'error_02.log', 'info_03.log']:\n"
            "    Path(_tmp, name).write_text('x')\n"
        ),
        "starter_code": (
            "from pathlib import Path\n\n"
            "def batch_rename(directory: str, pattern: str, replacement: str) -> list[tuple]:\n"
            "    # TODO: rename files containing `pattern` in their name\n"
            "    # Return list of (old_name, new_name) for renamed files only\n"
            "    pass\n"
        ),
        "tests": [
            {
                "description": "Renames matching files",
                "assert_code": (
                    "result = batch_rename(_tmp, 'error_', 'err_')\n"
                    "names = sorted(result)\n"
                    "assert len(names) == 2, f'Expected 2 renames, got {names}'\n"
                    "assert all('error_' in old and 'err_' in new for old, new in names)\n"
                    "result = names"
                ),
            },
            {
                "description": "Non-matching files are untouched",
                "assert_code": (
                    "files = [f.name for f in Path(_tmp).iterdir()]\n"
                    "assert 'info_03.log' in files, f'info_03.log was renamed: {files}'\n"
                    "result = files"
                ),
            },
        ],
        "hints": [
            "Iterate Path(directory).iterdir() for only top-level files.",
            "Check if pattern is in f.name before renaming. Use f.rename(f.parent / new_name).",
        ],
        "solution": (
            "from pathlib import Path\n\n"
            "def batch_rename(directory: str, pattern: str, replacement: str) -> list[tuple]:\n"
            "    renamed = []\n"
            "    for f in Path(directory).iterdir():\n"
            "        if f.is_file() and pattern in f.name:\n"
            "            new_name = f.name.replace(pattern, replacement)\n"
            "            f.rename(f.parent / new_name)\n"
            "            renamed.append((f.name, new_name))\n"
            "    return renamed\n"
        ),
    },
    {
        "id": "auto-004",
        "category": "automation",
        "difficulty": "medium",
        "title": "Parse Log File for Errors",
        "description": (
            "Write a function `extract_errors(log_text)` that parses a log file\n"
            "string and returns a list of dicts for each ERROR line.\n\n"
            "Log format: 'YYYY-MM-DD HH:MM:SS [LEVEL] message'\n"
            "Example line: '2024-01-15 10:23:45 [ERROR] Connection timeout'\n\n"
            "Return: [{'timestamp': '2024-01-15 10:23:45', 'message': 'Connection timeout'}]\n"
            "Only include ERROR lines."
        ),
        "starter_code": (
            "import re\n\n"
            "def extract_errors(log_text: str) -> list[dict]:\n"
            "    # TODO: parse log text and return ERROR entries\n"
            "    # Each entry: {'timestamp': '...', 'message': '...'}\n"
            "    pass\n"
        ),
        "tests": [
            {
                "description": "Extracts only ERROR lines",
                "assert_code": (
                    "log = ('2024-01-15 10:23:45 [INFO] Server started\\n'\n"
                    "       '2024-01-15 10:23:46 [ERROR] Connection timeout\\n'\n"
                    "       '2024-01-15 10:23:47 [WARNING] Slow query\\n'\n"
                    "       '2024-01-15 10:23:48 [ERROR] DB connection failed')\n"
                    "result = extract_errors(log)\n"
                    "assert len(result) == 2, f'Expected 2, got {len(result)}'\n"
                    "assert result[0]['message'] == 'Connection timeout'\n"
                    "assert result[1]['timestamp'] == '2024-01-15 10:23:48'"
                ),
            },
            {
                "description": "Returns empty list when no errors",
                "assert_code": (
                    "result = extract_errors('2024-01-15 10:00:00 [INFO] All good')\n"
                    "assert result == [], f'Got {result}'"
                ),
            },
        ],
        "hints": [
            "Use re.findall() with a pattern like r'(\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}) \\[ERROR\\] (.+)'",
        ],
        "solution": (
            "import re\n\n"
            "def extract_errors(log_text: str) -> list[dict]:\n"
            "    pattern = r'(\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}) \\[ERROR\\] (.+)'\n"
            "    return [\n"
            "        {'timestamp': ts, 'message': msg}\n"
            "        for ts, msg in re.findall(pattern, log_text)\n"
            "    ]\n"
        ),
    },
    {
        "id": "auto-005",
        "category": "automation",
        "difficulty": "hard",
        "title": "Build a Simple Task Runner",
        "description": (
            "Build a `TaskRunner` class that runs tasks in dependency order.\n\n"
            "  - add_task(name, fn, depends_on=[]) — register a task\n"
            "  - run(name) — run a task and all its dependencies first\n"
            "    (each task runs exactly once, even if depended on multiple times)\n\n"
            "Tasks should execute in dependency order (deps before dependents).\n"
            "Return a list of task names in the order they were executed."
        ),
        "starter_code": (
            "class TaskRunner:\n"
            "    def __init__(self):\n"
            "        self.tasks = {}\n"
            "        self.deps = {}\n"
            "        self.executed = []\n\n"
            "    def add_task(self, name: str, fn, depends_on: list = None):\n"
            "        # TODO: register task with its dependencies\n"
            "        pass\n\n"
            "    def run(self, name: str) -> list[str]:\n"
            "        # TODO: run task and all its dependencies\n"
            "        # Each task runs exactly once\n"
            "        # Return list of names in execution order\n"
            "        pass\n"
        ),
        "tests": [
            {
                "description": "Runs tasks in dependency order",
                "assert_code": (
                    "log = []\n"
                    "runner = TaskRunner()\n"
                    "runner.add_task('setup', lambda: log.append('setup'))\n"
                    "runner.add_task('build', lambda: log.append('build'), depends_on=['setup'])\n"
                    "runner.add_task('test', lambda: log.append('test'), depends_on=['build'])\n"
                    "result = runner.run('test')\n"
                    "assert log == ['setup', 'build', 'test'], f'Got {log}'\n"
                    "assert result == ['setup', 'build', 'test'], f'Got {result}'"
                ),
            },
            {
                "description": "Each task executes only once",
                "assert_code": (
                    "log2 = []\n"
                    "runner2 = TaskRunner()\n"
                    "runner2.add_task('a', lambda: log2.append('a'))\n"
                    "runner2.add_task('b', lambda: log2.append('b'), depends_on=['a'])\n"
                    "runner2.add_task('c', lambda: log2.append('c'), depends_on=['a'])\n"
                    "runner2.add_task('d', lambda: log2.append('d'), depends_on=['b', 'c'])\n"
                    "result2 = runner2.run('d')\n"
                    "assert log2.count('a') == 1, f'a ran {log2.count(\"a\")} times'\n"
                    "assert log2[-1] == 'd', f'd should run last: {log2}'\n"
                    "result = result2"
                ),
            },
        ],
        "hints": [
            "Use a set to track already-executed task names.",
            "Implement as recursive DFS: resolve deps first, then run the task.",
        ],
        "solution": (
            "class TaskRunner:\n"
            "    def __init__(self):\n"
            "        self.tasks = {}\n"
            "        self.deps = {}\n"
            "        self.executed = []\n\n"
            "    def add_task(self, name, fn, depends_on=None):\n"
            "        self.tasks[name] = fn\n"
            "        self.deps[name] = depends_on or []\n\n"
            "    def run(self, name):\n"
            "        self.executed = []\n"
            "        seen = set()\n"
            "        self._run(name, seen)\n"
            "        return self.executed\n\n"
            "    def _run(self, name, seen):\n"
            "        if name in seen:\n"
            "            return\n"
            "        for dep in self.deps.get(name, []):\n"
            "            self._run(dep, seen)\n"
            "        if name not in seen:\n"
            "            seen.add(name)\n"
            "            self.tasks[name]()\n"
            "            self.executed.append(name)\n"
        ),
    },
]
