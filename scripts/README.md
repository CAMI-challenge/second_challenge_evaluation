##dockermem.py

Tool to measure maximum memory usage and runtime of docker containers.

**Example**

Running the `ls` command without dockermem.py:
~~~BASH
docker run --rm -v $PWD:/host ubuntu:18.04 ls /host
~~~

Running `ls` with `dockermem.py`:
~~~BASH
./dockermem.py --rm -v "$PWD:/host:ro" --image ubuntu:18.04 --command "ls /host"
~~~
