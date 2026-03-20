"""LangChain / LangGraph conceptual challenges.

These challenges focus on patterns used in LangChain/LangGraph apps
without requiring actual API keys — they use mocked LLM calls so you
can practice the patterns purely in Python.
"""

LANGCHAIN_CHALLENGES = [
    {
        "id": "lc-001",
        "category": "langchain",
        "difficulty": "easy",
        "title": "Build a Prompt Template",
        "description": (
            "Implement a simple prompt template system used in LangChain.\n\n"
            "Write a class `PromptTemplate` with:\n"
            "  - __init__(self, template: str)  — stores the template\n"
            "  - format(self, **kwargs) -> str   — fills in {variable} placeholders\n\n"
            "Example:\n"
            "  t = PromptTemplate('Hello {name}, you are a {role}.')\n"
            "  t.format(name='Ada', role='developer')\n"
            "  → 'Hello Ada, you are a developer.'"
        ),
        "starter_code": (
            "class PromptTemplate:\n"
            "    def __init__(self, template: str):\n"
            "        # TODO: store the template\n"
            "        pass\n\n"
            "    def format(self, **kwargs) -> str:\n"
            "        # TODO: fill in {variable} placeholders with kwargs\n"
            "        pass\n"
        ),
        "tests": [
            {
                "description": "Formats template with variables",
                "assert_code": (
                    "t = PromptTemplate('Hello {name}, you are a {role}.')\n"
                    "result = t.format(name='Ada', role='developer')\n"
                    "expected = 'Hello Ada, you are a developer.'\n"
                    "assert result == expected, f'Got {result}'"
                ),
            },
            {
                "description": "Works with single variable",
                "assert_code": (
                    "t = PromptTemplate('Summarize: {text}')\n"
                    "result = t.format(text='The quick brown fox')\n"
                    "assert result == 'Summarize: The quick brown fox', f'Got {result}'"
                ),
            },
            {
                "description": "Handles no variables (static template)",
                "assert_code": (
                    "t = PromptTemplate('You are a helpful assistant.')\n"
                    "result = t.format()\n"
                    "assert result == 'You are a helpful assistant.', f'Got {result}'"
                ),
            },
        ],
        "hints": [
            "Use Python's built-in str.format_map() or str.format(**kwargs).",
        ],
        "solution": (
            "class PromptTemplate:\n"
            "    def __init__(self, template: str):\n"
            "        self.template = template\n\n"
            "    def format(self, **kwargs) -> str:\n"
            "        return self.template.format(**kwargs)\n"
        ),
    },
    {
        "id": "lc-002",
        "category": "langchain",
        "difficulty": "easy",
        "title": "Chain Two Steps Together",
        "description": (
            "In LangChain, you chain operations with `|` (pipe). Implement that pattern.\n\n"
            "Write a `Chain` class where:\n"
            "  - __init__(self, *steps)  — accepts callable steps\n"
            "  - run(self, input) -> any  — passes input through each step in order\n"
            "  - __or__(self, other)      — returns a new Chain combining both\n\n"
            "Example:\n"
            "  chain = Chain(str.upper) | Chain(str.strip)\n"
            "  chain.run('  hello  ')  →  '  HELLO  '  (upper first, then strip)"
        ),
        "starter_code": (
            "class Chain:\n"
            "    def __init__(self, *steps):\n"
            "        # TODO: store steps\n"
            "        pass\n\n"
            "    def run(self, input):\n"
            "        # TODO: pass input through each step\n"
            "        pass\n\n"
            "    def __or__(self, other: 'Chain') -> 'Chain':\n"
            "        # TODO: combine self and other into a new Chain\n"
            "        pass\n"
        ),
        "tests": [
            {
                "description": "Runs single step",
                "assert_code": (
                    "chain = Chain(str.upper)\n"
                    "result = chain.run('hello')\n"
                    "assert result == 'HELLO', f'Got {result}'"
                ),
            },
            {
                "description": "Pipes two chains together",
                "assert_code": (
                    "chain = Chain(str.strip) | Chain(str.upper)\n"
                    "result = chain.run('  hello  ')\n"
                    "assert result == 'HELLO', f'Got {result}'"
                ),
            },
            {
                "description": "Chains three steps",
                "assert_code": (
                    "chain = Chain(str.strip) | Chain(str.upper) | Chain(lambda s: s + '!')\n"
                    "result = chain.run('  world  ')\n"
                    "assert result == 'WORLD!', f'Got {result}'"
                ),
            },
        ],
        "hints": [
            "Store steps as a list. In run(), loop through: data = step(data).",
            "In __or__, create a new Chain with combined steps: Chain(*self.steps, *other.steps).",
        ],
        "solution": (
            "class Chain:\n"
            "    def __init__(self, *steps):\n"
            "        self.steps = list(steps)\n\n"
            "    def run(self, input):\n"
            "        data = input\n"
            "        for step in self.steps:\n"
            "            data = step(data)\n"
            "        return data\n\n"
            "    def __or__(self, other):\n"
            "        return Chain(*self.steps, *other.steps)\n"
        ),
    },
    {
        "id": "lc-003",
        "category": "langchain",
        "difficulty": "medium",
        "title": "Build a Message History Manager",
        "description": (
            "LangChain chat models need a message history. Build a `MessageHistory`\n"
            "class that manages a conversation:\n\n"
            "  - add_user(text)      — adds {'role': 'user', 'content': text}\n"
            "  - add_assistant(text) — adds {'role': 'assistant', 'content': text}\n"
            "  - get_messages() -> list  — returns all messages in order\n"
            "  - get_last_k(k) -> list   — returns last k messages\n"
            "  - clear()              — clears history\n"
            "  - token_estimate() -> int — rough token count: sum(len(m['content'].split()) for m in messages)"
        ),
        "starter_code": (
            "class MessageHistory:\n"
            "    def __init__(self):\n"
            "        self.messages = []\n\n"
            "    def add_user(self, text: str):\n"
            "        pass\n\n"
            "    def add_assistant(self, text: str):\n"
            "        pass\n\n"
            "    def get_messages(self) -> list:\n"
            "        pass\n\n"
            "    def get_last_k(self, k: int) -> list:\n"
            "        pass\n\n"
            "    def clear(self):\n"
            "        pass\n\n"
            "    def token_estimate(self) -> int:\n"
            "        pass\n"
        ),
        "tests": [
            {
                "description": "Adds and retrieves messages in order",
                "assert_code": (
                    "h = MessageHistory()\n"
                    "h.add_user('Hello')\n"
                    "h.add_assistant('Hi there!')\n"
                    "h.add_user('How are you?')\n"
                    "msgs = h.get_messages()\n"
                    "assert len(msgs) == 3, f'Expected 3, got {len(msgs)}'\n"
                    "assert msgs[0] == {'role': 'user', 'content': 'Hello'}\n"
                    "assert msgs[1]['role'] == 'assistant'\n"
                    "result = msgs"
                ),
            },
            {
                "description": "get_last_k returns last k messages",
                "assert_code": (
                    "h2 = MessageHistory()\n"
                    "for i in range(5):\n"
                    "    h2.add_user(f'msg {i}')\n"
                    "last2 = h2.get_last_k(2)\n"
                    "assert len(last2) == 2, f'Expected 2, got {len(last2)}'\n"
                    "assert last2[-1]['content'] == 'msg 4', f'Got {last2}'\n"
                    "result = last2"
                ),
            },
            {
                "description": "token_estimate counts words",
                "assert_code": (
                    "h3 = MessageHistory()\n"
                    "h3.add_user('hello world')\n"
                    "h3.add_assistant('how are you doing')\n"
                    "result = h3.token_estimate()\n"
                    "assert result == 6, f'Expected 6, got {result}'"
                ),
            },
        ],
        "hints": [
            "Each add_* method appends {'role': ..., 'content': text} to self.messages.",
            "get_last_k: use self.messages[-k:]",
        ],
        "solution": (
            "class MessageHistory:\n"
            "    def __init__(self):\n"
            "        self.messages = []\n\n"
            "    def add_user(self, text):\n"
            "        self.messages.append({'role': 'user', 'content': text})\n\n"
            "    def add_assistant(self, text):\n"
            "        self.messages.append({'role': 'assistant', 'content': text})\n\n"
            "    def get_messages(self):\n"
            "        return list(self.messages)\n\n"
            "    def get_last_k(self, k):\n"
            "        return self.messages[-k:]\n\n"
            "    def clear(self):\n"
            "        self.messages = []\n\n"
            "    def token_estimate(self):\n"
            "        return sum(len(m['content'].split()) for m in self.messages)\n"
        ),
    },
    {
        "id": "lc-004",
        "category": "langchain",
        "difficulty": "medium",
        "title": "Tool Router (Agent Pattern)",
        "description": (
            "LangChain agents route requests to tools. Build a `ToolRouter` that:\n\n"
            "  - register(name, fn, description='') — register a tool function\n"
            "  - route(tool_name, **kwargs) -> any  — call the named tool with kwargs\n"
            "  - list_tools() -> list[dict]          — return [{name, description}]\n"
            "  - Raises ValueError if tool not found\n\n"
            "This mimics how LangChain agents select and call tools."
        ),
        "starter_code": (
            "class ToolRouter:\n"
            "    def __init__(self):\n"
            "        self._tools = {}\n\n"
            "    def register(self, name: str, fn, description: str = ''):\n"
            "        # TODO: store the tool\n"
            "        pass\n\n"
            "    def route(self, tool_name: str, **kwargs):\n"
            "        # TODO: call the tool, raise ValueError if not found\n"
            "        pass\n\n"
            "    def list_tools(self) -> list:\n"
            "        # TODO: return [{name, description}] for all tools\n"
            "        pass\n"
        ),
        "tests": [
            {
                "description": "Routes to correct tool",
                "assert_code": (
                    "router = ToolRouter()\n"
                    "router.register('add', lambda a, b: a + b, 'Adds two numbers')\n"
                    "result = router.route('add', a=3, b=4)\n"
                    "assert result == 7, f'Got {result}'"
                ),
            },
            {
                "description": "list_tools returns all registered tools",
                "assert_code": (
                    "router2 = ToolRouter()\n"
                    "router2.register('search', lambda q: f'results:{q}', 'Search the web')\n"
                    "router2.register('calc', lambda x: x * 2, 'Calculator')\n"
                    "tools = router2.list_tools()\n"
                    "names = [t['name'] for t in tools]\n"
                    "assert 'search' in names and 'calc' in names, f'Got {names}'\n"
                    "result = tools"
                ),
            },
            {
                "description": "Raises ValueError for unknown tool",
                "assert_code": (
                    "router3 = ToolRouter()\n"
                    "raised = False\n"
                    "try:\n"
                    "    router3.route('nonexistent')\n"
                    "except ValueError:\n"
                    "    raised = True\n"
                    "assert raised, 'Expected ValueError'\n"
                    "result = raised"
                ),
            },
        ],
        "hints": [
            "Store tools as dict: {name: {'fn': fn, 'description': desc}}",
            "In route(), check if tool_name in self._tools, else raise ValueError.",
        ],
        "solution": (
            "class ToolRouter:\n"
            "    def __init__(self):\n"
            "        self._tools = {}\n\n"
            "    def register(self, name, fn, description=''):\n"
            "        self._tools[name] = {'fn': fn, 'description': description}\n\n"
            "    def route(self, tool_name, **kwargs):\n"
            "        if tool_name not in self._tools:\n"
            "            raise ValueError(f'Tool not found: {tool_name}')\n"
            "        return self._tools[tool_name]['fn'](**kwargs)\n\n"
            "    def list_tools(self):\n"
            "        return [{'name': k, 'description': v['description']} for k, v in self._tools.items()]\n"
        ),
    },
    {
        "id": "lc-005",
        "category": "langchain",
        "difficulty": "hard",
        "title": "LangGraph-Style State Machine",
        "description": (
            "LangGraph uses a state machine with nodes and edges. Build one.\n\n"
            "  `StateGraph` class:\n"
            "    - add_node(name, fn)         — fn(state) -> state update dict\n"
            "    - add_edge(from_node, to_node)\n"
            "    - set_entry(node_name)        — starting node\n"
            "    - set_end(node_name)          — terminal node\n"
            "    - run(initial_state: dict) -> dict\n"
            "      Executes: entry → ... → end, merging state updates at each node.\n"
            "      Returns final state.\n\n"
            "Node fn receives current state dict and returns a partial update dict\n"
            "that gets merged into state. Edges are followed linearly (one next node)."
        ),
        "starter_code": (
            "class StateGraph:\n"
            "    def __init__(self):\n"
            "        self.nodes = {}\n"
            "        self.edges = {}\n"
            "        self.entry = None\n"
            "        self.end = None\n\n"
            "    def add_node(self, name: str, fn):\n"
            "        pass\n\n"
            "    def add_edge(self, from_node: str, to_node: str):\n"
            "        pass\n\n"
            "    def set_entry(self, node_name: str):\n"
            "        pass\n\n"
            "    def set_end(self, node_name: str):\n"
            "        pass\n\n"
            "    def run(self, initial_state: dict) -> dict:\n"
            "        # TODO: traverse nodes from entry to end\n"
            "        # At each node: update = fn(state); state.update(update)\n"
            "        # Follow edges until reaching end node\n"
            "        pass\n"
        ),
        "tests": [
            {
                "description": "Runs nodes in order and merges state",
                "assert_code": (
                    "def fetch(state): return {'data': 'raw_data', 'step': 'fetched'}\n"
                    "def process(state): return {'data': state['data'].upper(), 'step': 'processed'}\n"
                    "def save(state): return {'saved': True, 'step': 'done'}\n\n"
                    "g = StateGraph()\n"
                    "g.add_node('fetch', fetch)\n"
                    "g.add_node('process', process)\n"
                    "g.add_node('save', save)\n"
                    "g.add_edge('fetch', 'process')\n"
                    "g.add_edge('process', 'save')\n"
                    "g.set_entry('fetch')\n"
                    "g.set_end('save')\n"
                    "result = g.run({'input': 'hello'})\n"
                    "assert result.get('saved') is True, f'Got {result}'\n"
                    "assert result.get('data') == 'RAW_DATA', f'Got {result}'\n"
                    "assert result.get('step') == 'done', f'Got {result}'"
                ),
            },
            {
                "description": "Preserves initial state keys",
                "assert_code": (
                    "def noop(state): return {'processed': True}\n"
                    "g2 = StateGraph()\n"
                    "g2.add_node('only', noop)\n"
                    "g2.set_entry('only')\n"
                    "g2.set_end('only')\n"
                    "result = g2.run({'user_id': 42})\n"
                    "assert result.get('user_id') == 42, f'Initial state lost: {result}'\n"
                    "assert result.get('processed') is True"
                ),
            },
        ],
        "hints": [
            "Store nodes as {name: fn} and edges as {from: to}.",
            "In run(): current = self.entry; while True: run node, merge state; if current == self.end: break; current = self.edges[current]",
        ],
        "solution": (
            "class StateGraph:\n"
            "    def __init__(self):\n"
            "        self.nodes = {}\n"
            "        self.edges = {}\n"
            "        self.entry = None\n"
            "        self.end = None\n\n"
            "    def add_node(self, name, fn):\n"
            "        self.nodes[name] = fn\n\n"
            "    def add_edge(self, from_node, to_node):\n"
            "        self.edges[from_node] = to_node\n\n"
            "    def set_entry(self, node_name):\n"
            "        self.entry = node_name\n\n"
            "    def set_end(self, node_name):\n"
            "        self.end = node_name\n\n"
            "    def run(self, initial_state):\n"
            "        state = dict(initial_state)\n"
            "        current = self.entry\n"
            "        while True:\n"
            "            update = self.nodes[current](state)\n"
            "            state.update(update)\n"
            "            if current == self.end:\n"
            "                break\n"
            "            current = self.edges[current]\n"
            "        return state\n"
        ),
    },
]
