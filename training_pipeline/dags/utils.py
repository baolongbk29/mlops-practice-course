from pathlib import Path

import pendulum
from airflow.models import Variable
from docker.types import Mount


class AppConst:
    DOCKER_USER = Variable.get("DOCKER_USER", "longlam071")


class AppPath:
    MLOPS_CRASH_COURSE_CODE_DIR = Path(
        Variable.get("MLOPS_CRASH_COURSE_CODE_DIR")
    )
    TRAINING_PIPELINE_DIR = MLOPS_CRASH_COURSE_CODE_DIR / "training_pipeline"
    FEATURE_REPO = TRAINING_PIPELINE_DIR / "feature_repo"
    ARTIFACTS = TRAINING_PIPELINE_DIR / "artifacts"


class DefaultConfig:
    DEFAULT_DAG_ARGS = {
        "owner": "longlam071",
        "retries": 0,
        "retry_delay": pendulum.duration(seconds=20),
    }

    DEFAULT_DOCKER_OPERATOR_ARGS = {
        "image": "longlam071/training_pipeline:latest",
        "api_version": "auto",
        "auto_remove": True,
        "mounts": [
            # feature repo
            Mount(
                source="/d/Main/mlops-practice-course/training_pipeline/feature_repo",
                target="/training_pipeline/feature_repo",
                type="bind",
            ),

            Mount(
                source="/d/Main/mlops-practice-course/training_pipeline/artifacts",
                target="/training_pipeline/artifacts",
                type="bind",
            ),
        ],
        # Fix a permission denied when using DockerOperator in Airflow
        # Ref: https://stackoverflow.com/a/70100729
        "docker_url": "tcp://docker-proxy:2375",
    }
