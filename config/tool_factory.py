from tools.log_parser_tool import LogParserTool
from tools.ioc_matcher_tool import IOCMatcherTool
from tools.endpoint_isolation_tool import EndpointIsolationTool
from tools.model_update_tool import ModelUpdateTool
from tools.vector_store_tool import VectorStoreTool
from tools.elastic_logger_tool import ElasticLoggerTool

def get_tools(task_name: str):
    if task_name == "log_ingestion_task":
        return [LogParserTool(), ElasticLoggerTool(), VectorStoreTool()]
    elif task_name == "ioc_matching_task":
        return [IOCMatcherTool()]
    elif task_name == "automated_response_task":
        return [EndpointIsolationTool()]
    elif task_name == "model_learning_task":
        return [ModelUpdateTool()]
    else:
        return []