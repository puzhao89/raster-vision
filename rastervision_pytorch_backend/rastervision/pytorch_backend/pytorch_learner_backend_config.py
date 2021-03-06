from typing import List, Optional

from rastervision.pipeline.config import (register_config, Field, validator)
from rastervision.core.backend import BackendConfig
from rastervision.pytorch_learner.learner_config import (
    SolverConfig, ModelConfig, default_augmentors, augmentors as
    augmentor_list, PlotOptions)
from rastervision.pytorch_learner.utils import validate_albumentation_transform


@register_config('pytorch_learner_backend')
class PyTorchLearnerBackendConfig(BackendConfig):
    model: ModelConfig
    solver: SolverConfig
    log_tensorboard: bool = Field(
        True, description='If True, log events to Tensorboard log files.')
    run_tensorboard: bool = Field(
        False,
        description='If True, run Tensorboard server pointing at log files.')
    augmentors: List[str] = Field(
        default_augmentors,
        description='Names of albumentations augmentors to use for training '
        f'batches. Choices include: {augmentor_list}. Alternatively, a custom '
        'transform can be provided via the aug_transform option.')
    base_transform: Optional[dict] = Field(
        None,
        description='An Albumentations transform serialized as a dict that '
        'will be applied to all datasets: training, validation, and test. '
        'This transformation is in addition to the resizing due to img_sz. '
        'This is useful for, for example, applying the same normalization to '
        'all datasets.')
    aug_transform: Optional[dict] = Field(
        None,
        description='An Albumentations transform serialized as a dict that '
        'will be applied as data augmentation to the training dataset. This '
        'transform is applied before base_transform. If provided, the '
        'augmentors option is ignored.')
    test_mode: bool = Field(
        False,
        description=
        ('This field is passed along to the LearnerConfig which is returned by '
         'get_learner_config(). For more info, see the docs for'
         'pytorch_learner.learner_config.LearnerConfig.test_mode.'))
    plot_options: Optional[PlotOptions] = Field(
        PlotOptions(), description='Options to control plotting.')

    # validators
    _base_tf = validator(
        'base_transform', allow_reuse=True)(validate_albumentation_transform)
    _aug_tf = validator(
        'aug_transform', allow_reuse=True)(validate_albumentation_transform)

    def get_bundle_filenames(self):
        return ['model-bundle.zip']

    def get_learner_config(self, pipeline):
        raise NotImplementedError()

    def build(self, pipeline, tmp_dir):
        raise NotImplementedError()
