import yaml
from crewai import Crew, Task
from config.agent_factory import get_agent
from config.tool_factory import get_tools
from logger.output_logger import log_to_json
from utils.es_logger import log_to_elasticsearch

class ThreatAICrew:
    def __init__(self):
        with open("config/agents.yaml", "r") as f:
            self.agent_configs = yaml.safe_load(f)

        with open("config/tasks.yaml", "r") as f:
            self.task_configs = yaml.safe_load(f)

    def get_crew(self, inputs: dict = None):
        if inputs is None:
            inputs = {}

        # Build agents from config
        agent_map = {
            name: get_agent(name, config)
            for name, config in self.agent_configs.items()
        }

        # Tool mapping
        tools_map = {
            name: get_tools(name)
            for name in self.task_configs.keys()
        }

        # Tasks list
        tasks = []

        # 🔁 Loop through task definitions and build Task objects
        for task_name, task_config in self.task_configs.items():
            input_variables = task_config.get("input_variables", [])
            task_inputs = {var: inputs.get(var) for var in input_variables if var in inputs}

            if task_name == "log_ingestion_task" and tools_map.get(task_name):
                tool = tools_map[task_name][0]
                print(f"\n🔧 Using Tool: {tool.name}")
                parsed_logs = tool._run(logs=inputs["logs"])
                print(f"✅ Output of {task_name} Tool:", parsed_logs)
                log_to_elasticsearch(index="log_ingestion", stage=task_name, data=parsed_logs)
                log_to_json(task_name, parsed_logs)
                inputs["structured_logs"] = parsed_logs
                task_inputs["logs"] = inputs["logs"]
                assigned_tools = []

            elif task_name == "vector_store_task" and tools_map.get(task_name):
                tool = tools_map[task_name][0]
                print(f"\n📦 Using Tool: {tool.name} for Vector Store")
                result = tool._run(logs=inputs["structured_logs"])
                print(f"✅ Output of {task_name} Tool:", result)
                log_to_elasticsearch(index="vector_store", stage=task_name, data=result)
                log_to_json(task_name, result)
                task_inputs["structured_logs"] = inputs["structured_logs"]
                assigned_tools = []

            else:
                assigned_tools = tools_map.get(task_name, [])

            task = Task(
                description=task_config["description"],
                expected_output=task_config["expected_output"],
                agent=agent_map[task_config["agent"]],
                tools=assigned_tools,
                input=task_inputs,
                async_execution=task_config.get("async_execution", False)
            )
            tasks.append(task)

        log_to_json(task_name, parsed_logs)  # e.g., after log_parser_tool

        # Create and return crew
        crew = Crew(
            agents=list(agent_map.values()),
            tasks=tasks,
            verbose=True
        )
        return crew