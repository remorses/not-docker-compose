import random
import time
import fire
import sys
import asyncio
from typing import Iterable, List, Coroutine
from funcy import merge, lmap
import os
from prtty import pretty
from .logger import logger
from .exec import get_stdout, exec
from dotenv.main import DotEnv
from colorama import init, Fore, Back, Style
from .constants import colors

from dotenv.parser import parse_binding
import yaml


async def get_config(f=None):
    cmd = "docker-compose"
    if f:
        cmd += f" -f {f}"
    cmd += " config"
    return await get_stdout(cmd, env=os.environ)


def get_processes(services) -> Iterable[Coroutine]:
    for name, service in services.items():
        env: dict = {}
        if "env_file" in service:
            env_file = service["env_file"]
            if not isinstance(env_file, list):
                env_file = [env_file]
            env.update(merge(*[DotEnv(path) for path in env_file]))
        if "environment" in service:
            environment = service['environment']
            if isinstance(environment, list):
                env.update({b.key: b.value for b in lmap(parse_binding, environment)})
            else:
                env.update(environment)
        cmd = service.get('entrypoint', '') + ' ' + service.get('command')
        if not cmd:
            raise Exception('cannot run without commands on the config')
        build = service['build']
        if isinstance(build, str):
            cwd = build
        else:
            cwd = build.get('context', '.')
        async def f(name, cmd, env, cwd):
            print('Attaching to ' + name)
            color = random.choice(colors)
            log = lambda x: sys.stdout.write(getattr(Fore, color) + f'{name}_1 | ' + x)
            await exec(cmd, env=env, cwd=cwd, stdout=log, stderr=log)
        yield f(name, cmd, env, cwd)


async def async_up(service=None, f=None):
    conf = await get_config(f)
    conf = yaml.safe_load(conf)
    unchanged_services = {
        k: v for k, v in conf["services"].items() if "image" in v and not "build" in v
    }
    unchanged_conf = yaml.safe_dump({**conf, "services": unchanged_services})
    services = {k: v for k, v in conf["services"].items() if "build" in v}
    # run the commands concurrently
    # - docker-compose
    # - run the images commands concurrently with their env_file and environment, grab the logs, color them, add the name prefix, print he logs
    processes = get_processes(services)
    group = asyncio.gather(
        exec('docker-compose -f - up', stdin=unchanged_conf, env=os.environ, stderr=None),
        *processes,
    )
    try:
        logger.debug('awaiting g')
        await group
    except KeyboardInterrupt:
        group.cancel()

def up(service=None, f=None):
    s = time.time()
    try:
        init(autoreset=True)
        asyncio.run(async_up(f=f), debug=False)
    except KeyboardInterrupt:
        print("Caught keyboard interrupt..")
    e = time.time()
    print(f'{e - s} secs')

    