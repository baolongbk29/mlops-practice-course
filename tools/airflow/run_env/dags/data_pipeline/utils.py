from pathlib import Path
import pendulum
from airflow.models import Variable
from docker.types import Mount


class AppConst:
    DOCKER_USER = Variable.get("DOCKER_USER", "longlam071")


class AppPath:
    MLOPS_CRASH_COURSE_CODE_DIR = Path(Variable.get("MLOPS_CRASH_COURSE_CODE_DIR"))
    DATA_PIPELINE_DIR = MLOPS_CRASH_COURSE_CODE_DIR / "data_pipeline"
    FEATURE_REPO = DATA_PIPELINE_DIR / "feature_repo"


class DefaultConfig:
    DEFAULT_DAG_ARGS = {
        "owner": "longlam071",
        "retries": 0,
        "retry_delay": pendulum.duration(seconds=20),
    }

    DEFAULT_DOCKER_OPERATOR_ARGS = {
        "image": f"{AppConst.DOCKER_USER}/data_pipeline:latest",
        "api_version": "auto",
        "auto_remove": True,
        "mounts": [
            # feature repo
            Mount(
                source="/d/Main/mlops-practice-course/data_pipeline/feature_repo",
                target="/data_pipeline/feature_repo",
                type="bind",
            ),
        ],
        # Fix a permission denied when using DockerOperator in Airflow
        # Ref: https://stackoverflow.com/a/70100729
        "docker_url": "tcp://docker-proxy:2375",
    }