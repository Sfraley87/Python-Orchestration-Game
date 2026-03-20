"""Async & orchestration challenges."""

ASYNC_CHALLENGES = [
    {
        "id": "async-001",
        "category": "async",
        "difficulty": "easy",
        "title": "Your First Async Function",
        "description": (
            "Write an async function `fetch_data(url: str) -> dict` that:\n"
            "  1. Awaits `async_get(url)` which returns a JSON string\n"
            "  2. Parses the JSON string and returns the dict\n\n"
            "`async_get` is already defined and available.\n"
            "Run it with: asyncio.run(fetch_data(url))"
        ),
        "setup_code": (
            "import asyncio\n"
            "import json\n\n"
            "async def async_get(url: str) -> str:\n"
            "    return json.dumps({'url': url, 'status': 200, 'data': 'hello'})\n"
        ),
        "starter_code": (
            "import asyncio\n"
            "import json\n\n"
            "async def fetch_data(url: str) -> dict:\n"
            "    # TODO: await async_get(url) and return parsed JSON dict\n"
            "    pass\n"
        ),
        "tests": [
            {
                "description": "Returns parsed dict from async response",
                "assert_code": (
                    "result = asyncio.run(fetch_data('https://api.example.com/data'))\n"
                    "assert isinstance(result, dict), f'Expected dict, got {type(result)}'\n"
                    "assert result.get('status') == 200, f'Got {result}'"
                ),
            },
            {
                "description": "URL is preserved in response",
                "assert_code": (
                    "result = asyncio.run(fetch_data('https://api.example.com/users'))\n"
                    "assert result.get('url') == 'https://api.example.com/users', f'Got {result}'"
                ),
            },
        ],
        "hints": [
            "Use `response = await async_get(url)` then `return json.loads(response)`.",
        ],
        "solution": (
            "import asyncio\n"
            "import json\n\n"
            "async def fetch_data(url: str) -> dict:\n"
            "    response = await async_get(url)\n"
            "    return json.loads(response)\n"
        ),
    },
    {
        "id": "async-002",
        "category": "async",
        "difficulty": "easy",
        "title": "Run Tasks Concurrently",
        "description": (
            "Write an async function `fetch_all(urls: list) -> list` that fetches\n"
            "all URLs concurrently (not sequentially) and returns a list of results.\n\n"
            "Use asyncio.gather() to run all fetches at the same time.\n"
            "`async_get(url)` returns a string response for each URL."
        ),
        "setup_code": (
            "import asyncio\n\n"
            "async def async_get(url: str) -> str:\n"
            "    return f'response:{url}'\n"
        ),
        "starter_code": (
            "import asyncio\n\n"
            "async def fetch_all(urls: list) -> list:\n"
            "    # TODO: fetch all URLs concurrently with asyncio.gather\n"
            "    # Return list of responses in same order as input URLs\n"
            "    pass\n"
        ),
        "tests": [
            {
                "description": "Returns all responses",
                "assert_code": (
                    "urls = ['https://a.com', 'https://b.com', 'https://c.com']\n"
                    "result = asyncio.run(fetch_all(urls))\n"
                    "assert len(result) == 3, f'Expected 3 results, got {len(result)}'\n"
                    "assert result[0] == 'response:https://a.com', f'Got {result}'"
                ),
            },
            {
                "description": "Preserves order of responses",
                "assert_code": (
                    "urls = ['https://x.com', 'https://y.com']\n"
                    "result = asyncio.run(fetch_all(urls))\n"
                    "assert result == ['response:https://x.com', 'response:https://y.com'], f'Got {result}'"
                ),
            },
        ],
        "hints": [
            "Use asyncio.gather(*[async_get(url) for url in urls]) to run concurrently.",
        ],
        "solution": (
            "import asyncio\n\n"
            "async def fetch_all(urls: list) -> list:\n"
            "    return list(await asyncio.gather(*[async_get(url) for url in urls]))\n"
        ),
    },
    {
        "id": "async-003",
        "category": "async",
        "difficulty": "medium",
        "title": "Async Queue Worker",
        "description": (
            "Write an async function `process_queue(items, worker, n_workers=3)` that:\n"
            "  - Puts all items into an asyncio.Queue\n"
            "  - Spawns `n_workers` worker coroutines that each pull from the queue\n"
            "  - Each worker calls `await worker(item)` and collects the result\n"
            "  - Returns all results as a list (order may vary)\n\n"
            "`worker` is an async function that takes one item and returns a value."
        ),
        "setup_code": (
            "import asyncio\n\n"
            "async def double(x):\n"
            "    return x * 2\n"
        ),
        "starter_code": (
            "import asyncio\n\n"
            "async def process_queue(items: list, worker, n_workers: int = 3) -> list:\n"
            "    # TODO: use asyncio.Queue to distribute work across n_workers coroutines\n"
            "    # Return all results\n"
            "    pass\n"
        ),
        "tests": [
            {
                "description": "Processes all items and returns results",
                "assert_code": (
                    "result = asyncio.run(process_queue([1, 2, 3, 4, 5], double))\n"
                    "assert sorted(result) == [2, 4, 6, 8, 10], f'Got {sorted(result)}'"
                ),
            },
            {
                "description": "Works with 1 worker",
                "assert_code": (
                    "result = asyncio.run(process_queue([10, 20], double, n_workers=1))\n"
                    "assert sorted(result) == [20, 40], f'Got {result}'"
                ),
            },
        ],
        "hints": [
            "Create a Queue and put all items in it before starting workers.",
            "Each worker: while not queue.empty(): item = await queue.get(); result = await worker(item); results.append(result); queue.task_done()",
            "Use asyncio.gather(*[worker_loop() for _ in range(n_workers)]) to run all workers.",
        ],
        "solution": (
            "import asyncio\n\n"
            "async def process_queue(items, worker, n_workers=3):\n"
            "    queue = asyncio.Queue()\n"
            "    results = []\n"
            "    for item in items:\n"
            "        await queue.put(item)\n\n"
            "    async def worker_loop():\n"
            "        while not queue.empty():\n"
            "            try:\n"
            "                item = queue.get_nowait()\n"
            "            except asyncio.QueueEmpty:\n"
            "                break\n"
            "            result = await worker(item)\n"
            "            results.append(result)\n"
            "            queue.task_done()\n\n"
            "    await asyncio.gather(*[worker_loop() for _ in range(n_workers)])\n"
            "    return results\n"
        ),
    },
    {
        "id": "async-004",
        "category": "async",
        "difficulty": "medium",
        "title": "Async Timeout Wrapper",
        "description": (
            "Write an async function `with_timeout(coro, timeout_sec, default=None)`\n"
            "that runs a coroutine with a timeout.\n\n"
            "  - If it completes in time, return its result\n"
            "  - If it times out, return `default` instead of raising\n\n"
            "Use asyncio.wait_for() and handle asyncio.TimeoutError."
        ),
        "setup_code": (
            "import asyncio\n\n"
            "async def fast_task():\n"
            "    return 'done'\n\n"
            "async def slow_task():\n"
            "    await asyncio.sleep(10)\n"
            "    return 'too late'\n"
        ),
        "starter_code": (
            "import asyncio\n\n"
            "async def with_timeout(coro, timeout_sec: float, default=None):\n"
            "    # TODO: run coro with timeout, return default if it times out\n"
            "    pass\n"
        ),
        "tests": [
            {
                "description": "Returns result when task completes in time",
                "assert_code": (
                    "result = asyncio.run(with_timeout(fast_task(), 5.0, default='timeout'))\n"
                    "assert result == 'done', f'Got {result}'"
                ),
            },
            {
                "description": "Returns default when task times out",
                "assert_code": (
                    "result = asyncio.run(with_timeout(slow_task(), 0.01, default='timed_out'))\n"
                    "assert result == 'timed_out', f'Got {result}'"
                ),
            },
        ],
        "hints": [
            "Use: try: return await asyncio.wait_for(coro, timeout=timeout_sec)",
            "Catch asyncio.TimeoutError and return the default value.",
        ],
        "solution": (
            "import asyncio\n\n"
            "async def with_timeout(coro, timeout_sec, default=None):\n"
            "    try:\n"
            "        return await asyncio.wait_for(coro, timeout=timeout_sec)\n"
            "    except asyncio.TimeoutError:\n"
            "        return default\n"
        ),
    },
    {
        "id": "async-005",
        "category": "async",
        "difficulty": "hard",
        "title": "Async Pipeline Orchestrator",
        "description": (
            "Build an async `Pipeline` class that chains async processing stages.\n\n"
            "  - add_stage(name, fn)  — adds an async function as a stage\n"
            "  - run(input_data) -> dict — runs input through all stages in order,\n"
            "    passing the output of each stage as input to the next.\n"
            "    Returns: {'result': final_output, 'stages': [stage_names_run]}\n\n"
            "Each stage fn is: async def stage(data) -> data"
        ),
        "setup_code": (
            "import asyncio\n\n"
            "async def clean(text): return text.strip().lower()\n"
            "async def tokenize(text): return text.split()\n"
            "async def count(tokens): return {'count': len(tokens), 'tokens': tokens}\n"
        ),
        "starter_code": (
            "import asyncio\n\n"
            "class Pipeline:\n"
            "    def __init__(self):\n"
            "        self.stages = []\n\n"
            "    def add_stage(self, name: str, fn):\n"
            "        # TODO: register a named async stage\n"
            "        pass\n\n"
            "    async def run(self, input_data) -> dict:\n"
            "        # TODO: run input through all stages in order\n"
            "        # Return {'result': final_output, 'stages': [names]}\n"
            "        pass\n"
        ),
        "tests": [
            {
                "description": "Chains stages in order",
                "assert_code": (
                    "p = Pipeline()\n"
                    "p.add_stage('clean', clean)\n"
                    "p.add_stage('tokenize', tokenize)\n"
                    "p.add_stage('count', count)\n"
                    "result = asyncio.run(p.run('  Hello World  '))\n"
                    "assert result['result']['count'] == 2, f'Got {result}'\n"
                    "assert result['stages'] == ['clean', 'tokenize', 'count'], f'Got {result}'"
                ),
            },
            {
                "description": "Works with single stage",
                "assert_code": (
                    "p2 = Pipeline()\n"
                    "p2.add_stage('clean', clean)\n"
                    "result2 = asyncio.run(p2.run('  HI  '))\n"
                    "assert result2['result'] == 'hi', f'Got {result2}'\n"
                    "assert result2['stages'] == ['clean']\n"
                    "result = result2"
                ),
            },
        ],
        "hints": [
            "Store stages as a list of (name, fn) tuples.",
            "In run(), iterate through stages, awaiting each fn with the current data.",
        ],
        "solution": (
            "import asyncio\n\n"
            "class Pipeline:\n"
            "    def __init__(self):\n"
            "        self.stages = []\n\n"
            "    def add_stage(self, name, fn):\n"
            "        self.stages.append((name, fn))\n\n"
            "    async def run(self, input_data):\n"
            "        data = input_data\n"
            "        names = []\n"
            "        for name, fn in self.stages:\n"
            "            data = await fn(data)\n"
            "            names.append(name)\n"
            "        return {'result': data, 'stages': names}\n"
        ),
    },
]
