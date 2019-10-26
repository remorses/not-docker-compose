import asyncio
import sys

async def get_stdout(cmd, cwd=None, env=None,):
    proc: asyncio.Process = await asyncio.create_subprocess_shell(
        cmd,
        env=env,
        cwd=cwd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, _ = await proc.communicate()
    return stdout

async def exec(cmd, cwd=None, env=None, stdout=sys.stdout.write, stderr=sys.stderr.write, stdin=None):
    proc: asyncio.Process = await asyncio.create_subprocess_shell(
        cmd,
        env=env,
        cwd=cwd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.PIPE if stdin else None,
    )
    if stdin:
        proc.stdin.write(stdin.encode() + b'\n')
        proc.stdin.write_eof()
        await proc.stdin.drain()
        proc.stdin.close()
        

    await asyncio.gather(
        read_stream(proc.stdout, stdout), read_stream(proc.stderr, stderr)
    )
    # stdout, stderr = await proc.communicate()
    return proc


async def read_stream(stream, cb):
    while True:
        line = await stream.readline()
        if line:
            cb(line.decode())
        else:
            break




