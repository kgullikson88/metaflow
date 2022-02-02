import json
import os

from metaflow.decorators import StepDecorator
from metaflow.metadata import MetaDatum


class ArgoWorkflowsInternalDecorator(StepDecorator):
    name = "argo_workflows_internal"

    def task_pre_step(
        self,
        step_name,
        task_datastore,
        metadata,
        run_id,
        task_id,
        flow,
        graph,
        retry_count,
        max_user_code_retries,
        ubf_context,
        inputs,
    ):
        meta = {}
        meta["argo-workflow-template"] = os.environ["ARGO_WORKFLOW_TEMPLATE"]
        meta["argo-workflow-name"] = os.environ["ARGO_WORKFLOW_NAME"]
        meta["argo-workflow-namespace"] = os.environ["ARGO_WORKFLOW_NAMESPACE"]
        entries = [
            MetaDatum(
                field=k, value=v, type=k, tags=["attempt_id:{0}".format(retry_count)]
            )
            for k, v in meta.items()
        ]
        # Register book-keeping metadata for debugging.
        metadata.register_metadata(run_id, step_name, task_id, entries)

    def task_finished(
        self, step_name, flow, graph, is_task_ok, retry_count, max_user_code_retries
    ):
        if not is_task_ok:
            # The task finished with an exception - execution won't
            # continue so no need to do anything here.
            return

        # For foreaches, we need to dump the cardinality of the fanout
        # into a file so that Argo Workflows can properly configure
        # the subsequent fanout task via an Output parameter
        # This assumes that /tmp is writable - which may not always be the case.
        # TODO: Rely on emptyDir for this behavior - 
        #       https://argoproj.github.io/argo-workflows/empty-dir/
        if graph[step_name].type == "foreach":
            with open("/tmp/splits", "w") as file:
                json.dump(list(range(flow._foreach_num_splits)), file)
