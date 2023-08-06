<a name=".climadjust.client"></a>
## climadjust.client

<a name=".climadjust.client.Client.authenticate"></a>
#### authenticate

```python
 | authenticate()
```

API authentication. Needed to connect to the API

<a name=".climadjust.clientMethods.dataset_mixin"></a>
## Datasets

<a name=".climadjust.clientMethods.dataset_mixin.DatasetMixin"></a>
### Observation datasets
<a name=".climadjust.clientMethods.dataset_mixin.DatasetMixin.get_observation_datasets"></a>
#### get\_observation\_datasets

```python
 | get_observation_datasets(name=None, page=None, size=None, sort_field=None, sort_direction=None)
```

Get a paginated list of observation datasets

**Arguments**:

- `name`: (optional) str dataset name
- `page`: (optional) int page number
- `size`: (optional) int number of results per page
- `sort_field`: (optional) str field to sort results by (either "type" or "name")
- `sort_direction`: (optional) str sort direction (either "ASC" or "DESC")

**Returns**:

list of observation datasets

<a name=".climadjust.clientMethods.dataset_mixin.DatasetMixin.get_observation_dataset_by_id"></a>
#### get\_observation\_dataset\_by\_id

```python
 | get_observation_dataset_by_id(ds_id: int)
```

Get an observation dataset. In case the dataset is being uploaded the uploaded state will also
appear.

**Arguments**:

- `ds_id`: int id of the observation dataset

**Returns**:

the selected dataset information

<a name=".climadjust.clientMethods.dataset_mixin.DatasetMixin.post_observation_dataset"></a>
#### post\_observation\_dataset

```python
 | post_observation_dataset(file, name, ds_format, variables)
```

Uploads an observation dataset

**Arguments**:

- `file`: str path to the dataset to be uploaded
- `name`: str dataset name
- `ds_format`: str dataset format (either "NETCDF" or "VALUE_TEXT")
- `variables`: list[dict] list of variables. Variable format should be:
{"standardName": "tas", "customName": "tas", "standardUnit": "Celsius", "customUnit": "Celsius"}

**Returns**:

id of the uploaded dataset

<a name=".climadjust.clientMethods.dataset_mixin.DatasetMixin.get_validation"></a>
#### get\_validation

```python
 | get_validation(ds_id)
```

Gets validation warning/errors and GEOJSON info from an uploaded dataset

**Arguments**:

- `ds_id`: int id of the uploaded dataset

**Returns**:

dict of validation warning/errors and a GEOJSON with info from the dataset

<a name=".climadjust.clientMethods.dataset_mixin.DatasetMixin.delete_observation_dataset"></a>
#### delete\_observation\_dataset

```python
 | delete_observation_dataset(id: int)
```

Delete existing observation dataset

**Arguments**:

- `id`: int id of the dataset

**Returns**:

### Projection datasets

<a name=".climadjust.clientMethods.dataset_mixin.DatasetMixin.get_projection_datasets"></a>
#### get\_projection\_datasets

```python
 | get_projection_datasets(type=None, name=None, page=None, size=None, sort_field=None, sort_direction=None)
```

Get a paginated list of projection datasets

**Arguments**:

- `name`: (optional) str dataset name
- `page`: (optional) int page number
- `size`: (optional) int number of results per page
- `sort_field`: (optional) str field to sort results by (either "type" or "name")
- `sort_direction`: (optional) str sort direction (either "ASC" or "DESC")

**Returns**:

list of projection datasets

<a name=".climadjust.clientMethods.dataset_mixin.DatasetMixin.get_projection_datasets_by_id"></a>
#### get\_projection\_datasets\_by\_id

```python
 | get_projection_datasets_by_id(id: int)
```

Get a projection dataset info

**Arguments**:

- `id`: int id of the projection dataset

**Returns**:

dict with dataset info


<a name=".climadjust.clientMethods.experiment_mixin"></a>
## climadjust.clientMethods.experiment\_mixin

<a name=".climadjust.clientMethods.experiment_mixin.ExperimentMixin.get_experiments"></a>
#### get\_experiments

```python
 | get_experiments(page=None, size=None, sort_field=None, sort_direction=None)
```

Get a paginated list of experiments

**Arguments**:

- `page`: (optional) int page number
- `size`: (optional) int number of results per page
- `sort_field`: (optional) str field to sort results by (either "id" or "name")
- `sort_direction`: (optional) str sort direction (either "ASC" or "DESC")

**Returns**:

list of experiments

<a name=".climadjust.clientMethods.experiment_mixin.ExperimentMixin.get_experiments_by_id"></a>
#### get\_experiments\_by\_id

```python
 | get_experiments_by_id(exp_id)
```

Get a specific experiment. In case the experiment is being uploaded the uploaded state will also
appear.

**Arguments**:

- `exp_id`: int id of the experiment

**Returns**:

the selected experiment information

<a name=".climadjust.clientMethods.experiment_mixin.ExperimentMixin.post_experiment"></a>
#### post\_experiment

```python
 | post_experiment(name, temporalResolution, variables, scenarios, models, baconfiguration, spatialResolution, datasetProjection, datasetReference, spatialCoverage, outputFormat, validation, mask)
```

**Arguments**:

- `name`: str experiment name
- `temporalResolution`: str temporal resolution for the experiment (only "DAILY")
- `variables`: list list of variables to perform the bias adjustment on
- `scenarios`: list list of dictionaries, each dictionary contains the scenario name as well as the startDate
and the endDate
- `models`: list list of models / members to use
- `baconfiguration`: list list of bias adjustment configurations for each variable
(variable, method, and parameters)
- `spatialResolution`: str spatial resolution for the experiment ("NATIVE")
- `datasetProjection`: dict dictionary with the IDs of the projections datasets that will be used for the
experiment
- `datasetReference`: dict dictionary with the IDs of the reference datasets that will be used for the
experiment
- `spatialCoverage`: shapely.geometry.Polygon() Polygon with the spatial coverage over which to execute the
experiment
- `outputFormat`: str output format (for example "NETCDF", "GRIB", ...)
- `validation`: str validation activity to perform (for example "NONE")
- `mask`: str a string explaining if land-mask needs to be used (for example "none")

**Returns**:

id of the uploaded experiment

<a name=".climadjust.clientMethods.experiment_mixin.ExperimentMixin.delete_experiment"></a>
#### delete\_experiment

```python
 | delete_experiment(exp_id)
```

Delete existing experiment

**Arguments**:

- `id`: int id of the expoeriment to be deleted

**Returns**:


