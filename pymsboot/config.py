from oslo_config import cfg

from pymsboot import version

CONF = cfg.CONF

default_opts = [
    cfg.StrOpt('db_engine', default='sqlite:////tmp/pymsboot.db', help='DB Engine'),
    cfg.StrOpt('conf_test_01', default='conf_test_01_default', help='Pymsboot test 01 config.'),
    cfg.StrOpt('conf_test_02', default='conf_test_02_default', help='Pymsboot test 02 config.'),
]

launch_opt = cfg.IntOpt(
    'launch_opt_test',
    default=1,
    help='Launch Opt Test.'
)

API_GROUP = 'api'
api_opts = [
    cfg.StrOpt('host', default='0.0.0.0', help='Pymsboot API server host.'),
    cfg.PortOpt('port', default=9666, help='Pymsboot API server port.'),
    cfg.IntOpt(
        'api_workers',
        default=0,
        help='Number of workers for Pymsboot API service '
             'default 0 means number of CPUs available'
    ),
    cfg.BoolOpt(
        'enable_periodic_task_01',
        default=False,
        help='Enable periodic task 01.'
    ),
    cfg.BoolOpt(
        'enable_periodic_task_02',
        default=False,
        help='Enable periodic task 02.'
    ),
]

PECAN_GROUP = 'pecan'
pecan_opts = [
    cfg.StrOpt(
        'root',
        default='pymsboot.api.controllers.root.RootController',
        help='Pecan root controller'
    ),
    cfg.ListOpt(
        'modules',
        default=["pymsboot.api"],
        help='A list of modules where pecan will search for applications.'
    ),
    cfg.BoolOpt(
        'debug',
        default=False,
        help='Enables the ability to display tracebacks in the browser and'
             ' interactively debug during development.'
    ),
    cfg.BoolOpt(
        'auth_enable',
        default=True,
        help='Enables user authentication in pecan.'
    )
]

ENGINE_GROUP = 'engine'
engine_opts = [
    cfg.StrOpt(
        'host',
        default='0.0.0.0',
        help='Name of the engine node. This can be an opaque '
             'identifier. It is not necessarily a hostname, '
             'FQDN, or IP address.'
    ),
    cfg.StrOpt(
        'topic',
        default='pymsboot_engine',
        help='The message topic that the engine listens on.'
    ),
    cfg.IntOpt(
        'engine_workers',
        default=0,
        help='Number of workers for Pymsboot engine service '
             'default 0 means number of CPUs available'
    ),
    cfg.BoolOpt(
        'enable_periodic_task_01',
        default=False,
        help='Enable periodic task 01.'
    ),
    cfg.BoolOpt(
        'enable_periodic_task_02',
        default=False,
        help='Enable periodic task 02.'
    ),
]


def list_opts():
    pymsboot_opts = [
        (API_GROUP, api_opts),
        (PECAN_GROUP, pecan_opts),
        (ENGINE_GROUP, engine_opts),
        (None, [launch_opt]),
        (None, default_opts),
    ]

    return pymsboot_opts


def parse_args(args=None, usage=None, default_config_files=None):
    CLI_OPTS = [launch_opt]
    CONF.register_cli_opts(CLI_OPTS)

    for group, options in list_opts():
        CONF.register_opts(list(options), group)

    CONF(
        args=args,
        project='pymsboot',
        version=version.version,
        usage=usage,
        default_config_files=default_config_files
    )
