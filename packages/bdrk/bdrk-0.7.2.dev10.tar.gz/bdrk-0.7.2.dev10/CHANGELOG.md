# Changelog

## v0.7.1 (2021-03-10)

### bdrk.model_analyzer

- Support custom fairness metrics logging.

## v0.7.0 (2021-03-09)

- Support starting a training run locally.
- Breaking: deprecated labrun

## v0.6.0

### bedrock_client.bedrock.analyzer.model_analyzer

- Breaking: model analyzer dependencies are now installed separately using `bdrk[xafai]`

## v0.5.0

### bdrk.v1.api

- Breaking: pipeline name and config_file_path have been remove dfrom pipeline response objects
- Breaking: config_file_path is now nested under source field for model server deployment and pipeline run APIs
- Breaking: model name has been removed from model collection and artefact response objects

## v0.4.2

### bedrock_client.bedrock.analyzer.model_analyzer

- Doc: Add more detailed docstrings for ModelAnalyzer class
- Fix: Make ModelAnalyzer work offline when no Bedrock key is available

## v0.4.1

### bdrk.v1.ModelApi

- New: Added `get_model_version_details` to get model version information
- new: Added `get_model_version_download_url` to get model version download url

## v0.4.0

### bedrock_client.bedrock.analyzer.model_analyzer

- Improve: Make XAI metric capturing (via SHAP) opt-in. By default only `log_model_info`

## v0.3.2 (2020-08-25)

### bedrock_client.bedrock.metrics

- Fix: inference metric collector exporting duplicate categorical data
- Improve: ignore unsupported value types when tracking metrics

## v0.3.1 (2020-08-12)

### bedrock_client.bedrock.analyzer.model_analyzer

- New: Added `ModelAnalyzer._log_model_info` to capture some information of the generated model

## v0.3.0 (2020-07-28)

### bedrock_client.bedrock.analyzer.model_analyzer

- New: Added `ModelAnalyzer` to generate and store xafai metrics

### bedrock_client.bedrock.metrics

- New: `ModelMonitoringService.export_http` now exports metadata about the baseline metrics (feature name, metric name, and metric type)

## v0.2.2 (2020-06-05)

### bedrock_client.bedrock.metrics

- New: return prediction id from `log_prediction` call
- Improve: error handling on missing baseline metrics

## v0.2.1 (2020-05-06)

### bedrock_client.bedrock.metrics

- Fix: handle nans when classifying features as discrete variable
- New: allow `str` type as prediction output for multi-class classification

## v0.2.0 (2020-04-09)

### bedrock_client.bedrock

- Deprecated `bdrk[prediction-store]` component
- Added `bdrk[model-monitoring]` component to capture both logging and metrics

### bedrock_client.bedrock.metrics

- Added `ModelMonitoringService.export_text` method for computing feature metrics on training data and exporting to a text file
- Added `ModelMonitoringService` class for initialising model server metrics based on baseline metrics exported from training
- Added `ModelMonitoringService.export_http` method for exposing current metrics in Prometheus registry to the scraper

## v0.1.6 (2020-01-29)

### bedrock_client.bedrock

- Added `bdrk[prediction-store]` optional component for logging of predictions at serving time

### bdrk.v1

- Removed `TrainingPipelineSchema.pipeline_source`.
- Fixed type of `ModelArtefactSchema.environment_id` from object to string.
- Removed unused schemas.
- Added `entity_number` to `ModelArtefactSchema`, `TrainingPipelineRunSchema` and `BatchScoringPipelineRunSchema`.
- Added `pipeline_name` to `TrainingPipelineRunSchema` and `BatchScoringPipelineRunSchema`.

## v0.1.5 (2019-11-13)

### bdrk.v1

- Added `kwargs` to models to allow backward compatibility.
- Changed response schema for `ModelApi.get_artefact_details` from `ModelArtefactDetails` to `ModelArtefactSchema`.
- Removed unused schemas.

## v0.1.4 (2019-10-09)

### bdrk.v1

- Added `get_training_pipeline_runs` function to retrieve all runs from a pipeline

## v0.1.3 (2019-10-01)

### bdrk.v1

- Added `bdrk.v1.ModelApi` with function `get_artefact_details`.
  ```python
  from bdrk.v1 import ModelApi
  model_api = ModelApi(api_client)
  artefact = model_api.get_artefact_details(public_id=pipeline.model_id, artefact_id=run.artefact_id)
  ```
- `bdrk.v1.models.UserSchema.email_address` made required.

### bdrk.v1_utils

- Added utility functions for downloading and unzipping artefacts

  ```py
  from bdrk.v1 import ApiClient, Configuration
  from bdrk.v1_util import download_and_unzip_artefact

  configuration = Configuration()
  configuration.api_key["X-Bedrock-Access-Token"] = "YOUR-TOKEN-HERE"
  configuration.host = "https://api.bdrk.ai"
  api_client = ApiClient(configuration)

  # There are other utility methods as well
  # `get_artefact_stream`, `download_stream`, `unzip_file_to_dir`
  download_and_unzip_artefact(
      api_client=api_client,
      model_id="model-repository-id",
      model_artefact_id="model-version-id",
      output_dir="/tmp/artefact",
  )
  ```
