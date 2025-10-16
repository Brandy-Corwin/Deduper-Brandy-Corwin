# Test cases in input.sam

By line:
- first read: good
- duplicate of first: remove
- different UMI: good
- different chromosome: good
- different start(no soft clipping): good
- different start(soft clipping): good
- duplicate of first(different col 4, but soft clipping makes the start the same): remove
- UMI not in UMI file: remove
- different strand: good