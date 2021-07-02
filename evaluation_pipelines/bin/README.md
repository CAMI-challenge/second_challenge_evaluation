The programs here are included in the profiling and assembly pipelines but can also be used independently. 

### Convert the Bracken and mOTUs profiling output format into CAMI profiling format

```
Usage: tocami.py [OPTIONS] PROFILE

Options:
  -f, --format [bracken|motus]  The input profile format  [required]
  -o, --output TEXT             output CAMI profile file.
  --help                        Show this message and exit.

```

```shell
python3 tocami.py -f bracken <(cat sample1.*.bracken.profile) [-o output.cami.profile]
```

### Validate the CAMI profiling file, and remove invalid taxid from the file according to the specified nodes.dmp file

```
Usage: rm_invalid_taxa.py [OPTIONS] CAMIPROFILES...

Options:
  -n, --nodedmp FILENAME  The nodes.dmp file to check the validity of
                          profiling file  [required]
  --help                  Show this message and exit.
```

```shell
python3 rm_invalid_taxa.py -n <ncbi taxonomy nodes.dmp file> \
    <CAMI profiling files> [> invalod.taxid.log]
```
