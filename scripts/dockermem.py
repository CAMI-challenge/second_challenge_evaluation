#!/usr/bin/env python3

# Copyright 2020 Department of Computational Biology for Infection Research - Helmholtz Centre for Infection Research
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import docker
import time
import argparse


def run_docker(image, volumes, command, remove, workdir, environment):
    # print(volumes)
    client = docker.from_env()
    container = client.containers.run(image, command, volumes=volumes, detach=True, working_dir=workdir, environment=environment, entrypoint="")
    stats = container.stats(stream=True, decode=True)
    # max_usage = .0
    # max_usage_test = .0
    max_total_rss = .0

    while not container.status.startswith("e"):
        container.reload()
        next_stats = next(stats)
        # print json.dumps(next_stats, sort_keys=True, indent=4, separators=(',', ': '))
        time.sleep(1)
        try:
            # max_usage = next_stats["memory_stats"]["max_usage"]
            # usage = next_stats["memory_stats"]["usage"]
            # if usage > max_usage_test:
            #     max_usage_test = usage
            total_rss = next_stats["memory_stats"]["stats"]["total_rss"]
            if total_rss > max_total_rss:
                max_total_rss = total_rss
        except KeyError:
            pass
    # print("%f MB\t%f MB\t%f MB" % (max_usage / 1048576.0, max_usage_test / 1048576.0, max_total_rss / 1048576.0))
    if remove:
        container.remove()
    return max_total_rss


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--image", required=True)
parser.add_argument("-v", "--volume", type=lambda x: x.split(":"), action="append")
parser.add_argument("-c", "--command", required=True)
parser.add_argument("-w", "--workdir", required=False)
parser.add_argument("--rm", action="store_true")
parser.add_argument("--path", required=False)
#parser.add_argument("-e", "--environment", action="append")
args = parser.parse_args()

volumes = dict()
if args.volume:
    for i in range(0, len(args.volume)):
        # print "%s %s %s" % (args.volume[i][0], args.volume[i][1], args.volume[i][2])
        volumes[args.volume[i][0]] = {'bind': args.volume[i][1], 'mode': args.volume[i][2]}
if args.path:
    # environment = {'PATH': args.path}
    environment = ['PATH=' + args.path]
else:
    environment = None

# environment = None
# if args.environment:
#     environment = {'YAML': args.environment}

start_time = time.time()
max_total_rss = run_docker(args.image, volumes, args.command, args.rm, args.workdir, environment)
elapsed_time = time.time() - start_time
# print("%.2fs or %.2fm or %.2fh" % (elapsed_time, elapsed_time/60, elapsed_time/3600))
memory = max_total_rss / 1048576.0
print('{:.2f} seconds ({:.2f} hours)\n{} MB ({} GB)'.format(elapsed_time, elapsed_time/3600, memory, memory/1024))
