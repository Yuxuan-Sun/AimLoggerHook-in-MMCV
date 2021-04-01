import os.path as osp

from ...dist_utils import master_only
from ..hook import HOOKS
from .base import LoggerHook

from collections import OrderedDict


@HOOKS.register_module()
class AimLoggerHook(LoggerHook):

    def __init__(self,
                 log_dir=None,
                 interval=10,
                 ignore_last=True,
                 reset_flag=True,
                 by_epoch=True):
        super(AimLoggerHook, self).__init__(interval, ignore_last,
                                                    reset_flag, by_epoch)
        self.log_dir = log_dir

    @master_only
    def before_run(self, runner):
        try:
            from aim import Session
        except ImportError:
            raise ImportError('Please install aim to use '
                                  'AimLoggerHook.')

        if self.log_dir is None:
            self.log_dir = osp.join(runner.work_dir, 'aim_logs')

        self.aim_sess = Session()
        self.aim_sess.set_params({
            'num_epochs': runner._max_epochs,
            'batch_size': 4 #set your own
        }, name='hparams')

    @master_only
    def log(self, runner):
        log_dict = OrderedDict(
            mode=self.get_mode(runner),
            epoch=self.get_epoch(runner))

        log_dict = dict(log_dict, **runner.log_buffer.output)

        for name, val in log_dict.items():
            # things that are unwanted in metric
            if name in [
                    'mode', 'Epoch', 'iter', 'lr', 'time', 'data_time',
                    'memory', 'epoch'
            ]:
                continue

            # will keep track of loss_cls, loss_bbox, loss, grad_norm
            # aim does not support iteration tracking yet, progress: https://github.com/aimhubio/aim/issues/288
            if isinstance(val, float):
                self.aim_sess.track(
                        val,
                        name = name,
                        epoch = log_dict['epoch'],
                        subset = log_dict['mode'])
