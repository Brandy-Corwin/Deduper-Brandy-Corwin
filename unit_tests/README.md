# Test cases in input.sam

By line:
- first read: good
- different start(no soft clipping): good
- duplicate of second: remove
- different UMI: good
- different start(soft clipping): good
- UMI not in UMI file: remove
- different strand: good
- duplicate of first(different col 4, but soft clipping makes the start the same): remove
- different chromosome: good